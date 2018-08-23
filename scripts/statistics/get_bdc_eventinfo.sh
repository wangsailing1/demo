#!/bin/sh

echo "开始执行：$0"
BASE_DIR=`cd $(dirname $0);pwd`

platform=$1
if [[ $platform == 'superhero2_tw' ]];then
    echo '超级英雄2台湾平台'
    ip=`cat /data/deploy_superhero2_tw/pub_new_list.txt |grep -v '^#'`
else
    echo 'platform 参数错误'
    exit 1
fi

date_y=$2
if [ ! ${date_y} ];then
    date_y=`date +%Y-%m-%d --date '1 days ago'`
fi

week_ago=`date +%Y-%m-%d --date '7 days ago'`

echo ${date_y}

dest_dir=/data/bdc_event_mid/${platform}/${date_y}

if [ ! -d $dest_dir ];then
   mkdir -p $dest_dir
fi


for i in ${ip}
do
    printf "\n正在传输：$i \n\n"
    mkdir -p ${dest_dir}/${i}
    /usr/bin/rsync -zutrvP admin@${i}:/data/sites/superhero2_tw_backend_new/logs/bdc_event/*_${date_y}.log "${dest_dir}/${i}/"
done


#event_dir=/data/bi_data/${platform}/bdc_event/${date_y}
event_zip_dir=${dest_dir}/zip

#if [ ! -d $event_dir ];then
#    mkdir -p $event_dir
#fi

if [ ! -d ${event_zip_dir} ];then
    mkdir -p ${event_zip_dir}
else
    rm ${event_zip_dir}/*
fi


game_id=''
# file=0172_130172010001_eventinfo-12177_2018-06-05.log
# 按服合并log
for i in ${ip}
do
    for file in `ls ${dest_dir}/$i`
    do
        game_id=${file%%_*}
        prefix=${file%%-*}
        suffix=${file##*_}
        merge_file=$prefix"_"$suffix
        cat ${dest_dir}/${i}/$file >> ${event_zip_dir}/$merge_file
        rm ${dest_dir}/${i}/$file
    done
done

cd ${event_zip_dir}

/usr/bin/zip -j $game_id"_"eventinfo_${date_y}.zip *.log

# 上传至互娱 ftp
/bin/sh  $BASE_DIR/bdc_log_upload.sh ${platform} eventinfo ${event_zip_dir}


#cat ${dest_dir}/*/*_${date_y}.log > /data/bi_data/${platform}/bdc_event/bdc_event_${date_y}_tmp && \
#mv /data/bi_data/${platform}/bdc_event/bdc_event_${date_y}_tmp /data/bi_data/${platform}/bdc_event/bdc_event_${date_y} && \

if [ -d /data/bdc_event_mid/${platform}/${week_ago} ]; then
    rm -rf /data/bdc_event_mid/${platform}/${week_ago}
fi

echo 'done'

