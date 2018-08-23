#!/bin/sh

WORK_DIR=$(cd "$(dirname "$0")"; pwd)

if [ -z $WORK_DIR ];then
    exit 1
fi

temp=$WORK_DIR"/client_resource"
version_path="/data/sites/superhero2_backend/logs/"

targets=(120.92.15.63)

for target in ${targets[*]};
do
    target_path=admin@$target:$version_path;
    echo $target_path;
    rsync -alrI --progress --recursive --exclude='*.zip' --exclude='*.txt' $temp $target_path && date && echo "client resource version file $target deployed";
done
