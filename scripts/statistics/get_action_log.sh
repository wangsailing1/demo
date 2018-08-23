#!/bin/sh

env=$1;

if [ ! $env ]; then
    exit;
fi

filepath=$(cd "$(dirname "$0")"; pwd)

echo "filepath: "$filepath

yesterday=$(date +"%Y-%m-%d 00:00:00" --date=1' days ago');
hjq_subfix=$(date +"%Y%m%d" --date=1' days ago');


cat $filepath/../../logs/action/$env_*_$hjq_subfix > $filepath/../../statistic/$env/action_log_$hjq_subfix