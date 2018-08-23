#!/bin/sh

echo "开始执行：$0"
echo "[`date`] $0 start to run!" >> /data/bi_script/log.txt
platform=$1

if [[ $platform == 'tw_release_new' ]]; then
    echo '台湾平台'
else
    echo 'platform 参数错误'
    exit 1
fi

date_today=$2
if [ ! ${date_today} ];then
    date_today=`date -d yesterday +%Y%m%d`
fi

bi_snapshot() {
    # act
    /usr/local/bin/python2.7 /data/sites/superhero2_tw_backend_new/scripts/statistics/get_all_act.py  ${platform} ${date_today} && \
    # info
    /usr/local/bin/python2.7 /data/sites/superhero2_tw_backend_new/scripts/statistics/get_all_info.py ${platform} ${date_today} && \
    # reg
    /usr/local/bin/python2.7 /data/sites/superhero2_tw_backend_new/scripts/statistics/get_all_reg.py ${platform} ${date_today}

   # upload hero bdc zip file
   # /bin/sh /data/sites/superhero2_tw_backend_new/scripts/statistics/bdc_log_upload.sh ${platform} userinfo
   /bin/sh /data/bi_script/bdc_log_upload.sh ${platform} user
}

bi_snapshot && \
echo 'done' || \
curl 'https://hook.bearychat.com/=bw79O/incoming/0f79b0211fcffac6e577da80fbbe928a' -X POST -d "payload={\"text\":\"【`date +%Y-%m-%d:%H:%M:%S`】$0 @ $1 数据生成失败\"}"
rsync -avzP /data/bi_data/${platform}/redis_static/ admin@192.168.10.86:/data2/bi_data/superhero2_tw/redis_static
echo "[`date`] $0 ends!" >> /data/bi_script/log.txt
