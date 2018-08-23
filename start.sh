#!/bin/bash

PROGDIR="$(cd "$(dirname "$0")" && pwd)"

if [ $# -ne 1 ]; then
    env='yyf'
    path='/Users/m0005/data/superhero2/backend2/'
else
    env=$1
    path=$PROGDIR/
fi

#/usr/local/bin/gunicorn -c "$path/gunicorn_config.py" --env game_env=$env -b 127.0.0.1:7001 -w 1 -t 0 -p $path/logs/gun.pid run_wsgi:app

python $path'run.py' --port=7001 --env=$env --server_name=all --numprocs=1
