from flask import request
import boto3
import random
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
    
    def random_filename():
        filename = ''.join(random.choice(chars) for i in range(8))
        return filename

    def upload_file(self, route=''):
        if 'file' not in request.files:
            error = 'No file part'
            return error
        file = request.files['file']

        if file.filename == "":
            return
        elif file and self.allowed_files(file.filename):
            filename = self.random_filename()
            image = self.convert_to_thumbnail(file.stream) if route == 'profile' else self.convert_to_webp(file.stream)

            s3.put_object(Bucket='verba-post-images', Key=filename, Body=image, ContentType='image/webp')

            location = s3.get_bucket_location(Bucket='verba-post-images')['LocationConstraint']
            region = '' if location is None else f'{location}'
            image_url = f"https://verba-post-images.s3.{region}.amazonaws.com/{filename}"
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
    
    def convert_to_thumbnail(stream):
        image = Image.open(stream)
        image = ImageOps.exif_transpose(image)

        width, height = image.size

        image = image.convert('RGB')

        left = (width - (width * 0.7))/2
        right = (width + (width * 0.4))/2
        top = (height - (height * 0.3))/2
        down = (height + (height * 0.4))/2
        image = image.crop((left, top, right, down))
        
        image = image.resize((575, 695))
        image_byte = io.BytesIO()
        image.save(image_byte, 'webp')
        return image_byte.getvalue()