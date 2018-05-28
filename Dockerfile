FROM python:3.6-alpine as base
MAINTAINER Metz Charusasi "metz@studiotwist.co"

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps \
        build-base postgresql-dev libffi-dev linux-headers

RUN pip install uwsgi pipenv

ADD Pipfile /app
ADD Pipfile.lock /app
RUN pipenv install --system

RUN find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del build-base && rm -rf /var/cache/apk/*

ADD . /app

EXPOSE 8000
# CMD ["python", "makrub/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["/usr/local/bin/uwsgi", "--http", ":8000", "--wsgi-file", "/app/makrub/config/wsgi.py", "--py-autoreload", "1"]
