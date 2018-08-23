#!/bin/bash

# userinfo chargeinfo 在 get_all_info.py 脚本里跟着生成bi数据时生成并打包zip，减少数据库读取
# 管理机的 crontab 每日凌晨调用 get_bi_point.sh 用bdc_log_upload.sh 上传zip至互娱ftp
# /bin/sh bdc_log_upload.sh $env user
#
# realtime数据 crontab 每小时调用当前脚本生成并上传
# /bin/sh bdc_log_upload.sh $env realtime

env=$1
project_path=/data/sites/genesis2_dev
cur_path=$(cd $(dirname $0);pwd)

/usr/local/bin/python2.7 $project_path/scripts/statistics/bdc_snapshot.py $env  \
&& /bin/sh $project_path/scripts/statistics/bdc_log_upload.sh $env realtime \
&& echo $env, "realtime", `date` >> $cur_path/bdc_snapshot_log


