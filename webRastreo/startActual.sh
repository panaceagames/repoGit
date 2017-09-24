#!/bin/bash

source /home/broadbandgame/.virtualenvs/webRastreo/bin/activate

cd /home/web/repoGit/webRastreo/

exec gunicorn webRastreo.wsgi --bind 127.0.0.1:8000 -D --log-file /home/web/logs/webRastreo_gunicorn.log --workers 3

