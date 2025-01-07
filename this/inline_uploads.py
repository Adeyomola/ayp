from flask import request, Blueprint, redirect, url_for
import boto3
from datetime import date
import string
import io
from PIL import Image, ImageOps


s3 = boto3.client('s3')
chars = string.digits + string.ascii_letters

class Upload:
    def __init__(self) -> None:
        pass

    def allowed_files(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'webp']

    def upload_file(self, route=''):
        if 'file' not in request.files:
            error = 'No file part'
            return error
        file = request.files['file']

        if file.filename == "":
            return
        elif file and self.allowed_files(file.filename):
            print(file.filename)
            image = self.convert_to_webp(file.stream)

            s3.put_object(Bucket='verba-post-images', Key=file.filename, Body=image, ContentType='image/webp')

            location = s3.get_bucket_location(Bucket='verba-post-images')['LocationConstraint']
            region = '' if location is None else f'{location}'
            image_url = f"https://verba-post-images.s3.{region}.amazonaws.com/{file.filename}"
        return image_url
    
    def delete_file(image_url):
        image_url = image_url.split("://")[1].split("/")[1]
        s3.delete_object(Bucket='verba-post-images', Key=image_url)

    def convert_to_webp(stream):
        image = Image.open(stream)
        image = ImageOps.exif_transpose(image)
        
        image = image.convert('RGB')
        image = image.resize((1284, 717))
        image_byte = io.BytesIO()
        image.save(image_byte, 'webp')
        return image_byte.getvalue()
    


bp = Blueprint('uploads', __name__)
@bp.route('/meed')
def list_files():
    result = s3.list_objects_v2(Bucket='verba-post-images')['Contents']
    location = s3.get_bucket_location(Bucket='verba-post-images')['LocationConstraint']
    region = '' if location is None else f'{location}'
    return {"result": result, "region": region}

@bp.route('/uplds', methods=['POST'])
def upload_file():
    Upload.upload_file(Upload)
    return redirect(request.referrer)
