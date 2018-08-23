#!/bin/bash

env=$1
cmd=$2
special_path=$3

echo $env, $cmd, $special_path

day=`date -d yesterday "+%Y-%m-%d"`
# path="/data/sites/genesis2_backend/logs/"
path="/data/bi_data/$env/bdc_snapshot/"


if [ "x$special_path" != "x" ]; then
    path=$special_path
    echo "path=special_path:", $path
fi


host=123.56.240.59
port=21212
user=chaojiyingxiong
pwd=TCcfh29F823BverfH


upload_realtime_log(){
ftp -n<<!
open $host $port
user $user $pwd
binary
lcd $path
cd realtime
prompt
mput *realtime*.log
ls
close
bye
!

}

upload_user_and_charge_info(){

ftp -n<<!
open $host $port
user $user $pwd
binary
lcd $path
cd /
prompt
mput *$day.zip
ls
close
bye
!

}

upload_event_info(){

ftp -n<<!
open $host $port
user $user $pwd
binary
lcd $path
cd /
prompt
mput *.zip
ls
close
bye
!

}

case $cmd in
    realtime)
        upload_realtime_log
    ;;
    user)
        upload_user_and_charge_info
    ;;
    eventinfo)
        upload_event_info
    ;;
esac