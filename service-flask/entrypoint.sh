#!/bin/bash 
cd /usr/src/app
exec /usr/bin/gunicorn $APP -b 0.0.0.0:$PORT