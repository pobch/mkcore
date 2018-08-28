FROM python:3.6-alpine as base
MAINTAINER Metz Charusasi "metz@studiotwist.co"

RUN apk add --no-cache --virtual .build-deps \
        build-base postgresql-dev libffi-dev linux-headers

RUN pip install uwsgi
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
WORKDIR /app/makrub
RUN pip install -r /app/requirements.txt

RUN addgroup -S uwsgi && adduser -S -G uwsgi uwsgi

EXPOSE 8000
CMD ["/app/start.sh"]
