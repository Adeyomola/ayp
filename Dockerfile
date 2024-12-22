FROM python:3.10-bullseye
EXPOSE 80

RUN mkdir -p /this/this && adduser adeyomola && apt update -y && apt install apache2 apache2-dev -y

COPY this /this/this
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /this

WORKDIR /this/this
RUN pip install -r requirements.txt && chmod +x /usr/local/bin/conf_editor.sh

WORKDIR /this
ENTRYPOINT conf_editor.sh && flask db-init \
    && mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null