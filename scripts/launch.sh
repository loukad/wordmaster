#!/bin/bash

set -euxo pipefail

cp /wm/etc/wordmaster.conf /etc/nginx/conf.d/

rm /etc/nginx/sites-enabled/default

nginx -t
nginx

cd /wm/app
gunicorn \
    --log-level DEBUG \
    --access-logfile - \
    --error-log - \
    --capture-output \
    --bind unix:/wordmaster-flask.sock \
    -g www-data \
    -m 007 \
    wm:app
