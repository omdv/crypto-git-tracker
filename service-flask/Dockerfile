FROM alpine:3.7

# set working directory
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install python and everything for postgres
RUN apk update && \
 apk add python3 postgresql-libs && \
 apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# add app
COPY . /usr/src/app

# set environment for entrypoint
env APP=manage:app
env PORT=5000

# set port
EXPOSE 5000/tcp

# run gunicorn
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
# CMD python3 manage.py runserver -h 0.0.0.0 -p 5000