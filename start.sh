#!/bin/bash

NAME="webRastreo"
DJANGODIR=/home/web/repoGit/webRastreo/
LOGFILE=/home/web/logs/gunicorn.log
LOGDIR=($dirname $LOGFILE)
USER=broadbandgame
GROUP=broadbandgame
ADDRESS=127.0.0.1:8000
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=webRastreo.settings
DJANGO_WSGI_MODULE=webRastreo.wsgi

echo "Starting $NAME as 'whoami'

cd $DJANGODIR
source /home/broadbandgame/.virtualenvs/default/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTING_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
	--workers $NUM_WORKES \
	--bind=$ADDRESS \
	--user=$USER --group=$GROUP \
	--log-level=debug \
	--log-file=$LOGFILE 2>>$LOGFILE

