#! /bin/bash

touch .env

echo "export DB_PASSWORD=$DB_PASSWORD" >> .env
echo "export DB_USER=$DB_USER" >> .env
echo "export DATABASE=$DATABASE" >> .env
echo "export HOST=$HOST" >> .env
echo "export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')" >> .env
echo "export TOTP_SECRET=$(python -c 'import secrets; import base64; print(base64.b32encode(secrets.token_bytes(5)).decode("utf-8"))')" >> .env