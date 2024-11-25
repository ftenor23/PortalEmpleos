FROM python:3.9.1-alpine3.13

WORKDIR /usr/src/app

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && apk add jpeg-dev zlib-dev libjpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del build-deps

COPY . .

RUN find /usr/src/app -type f -print0 | xargs -0 dos2unix

# Crear el directorio de logs y darle permisos
RUN mkdir -p /usr/src/app/logs && chown -R nobody:nogroup /usr/src/app/logs

CMD ["gunicorn", "-b", "0.0.0.0:5000", "gunicorn-launch:app"]

#CMD ["gunicorn" , "-b", "0.0.0.0:5000", "--workers", "4", "--timeout", "1000", "--log-level", "debug", "--access-logfile", "/usr/src/app/logs/access_gunicorn.log", "--error-logfile", "/usr/src/app/logs/access_gunicorn.log", "gunicorn-launch:app"]

EXPOSE 5000
