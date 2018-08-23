#!/bin/sh

echo "开始执行：$0"
echo "[`date`] $0 start to run!" >> /data2/hero_bi_data/log.txt

platform=$1
if [[ $platform == 'superhero2_release' ]];then
    echo '超级英雄2台湾平台'
    ip=`cat /data/deploy/pub_srv_list.txt | grep -vE '^#|^$'`
else
    echo 'platform 参数错误'
    exit 1
fi

date_y=$2
if [ ! ${date_y} ];then
    date_y=`date +%Y%m%d --date '1 days ago'`
fi

echo ${date_y}

dest_mid_dir=/data2/hero_bi_data/hdc_log_mid/${platform}/${date_y}
dest_dir=/data2/hero_bi_data/hdc_log/${platform}/${date_y}

mkdir -p ${dest_dir}

for i in ${ip}
do
    printf "\n正在传输：$i \n\n"
    mkdir -p ${dest_mid_dir}/${i}
    /usr/bin/rsync -zutrvP admin@${i}:/data/sites/superhero2_backend/logs/hero_log/*-${date_y}-* "${dest_mid_dir}/${i}/"
done

for i in ${ip}
do
	for filename in `ls ${dest_mid_dir}/${i}/`
	do
		if [ ! -f ${dest_dir}/${filename} ]; then
			cp ${dest_mid_dir}/${i}/${filename} ${dest_dir}/
		else
			cat ${dest_mid_dir}/${i}/${filename} >> ${dest_dir}/${filename}
		fi
	done
done

# rm -rf /data2/hero_bi_data/hdc_log_mid/${platform}/* && \
echo 'done'

# 同步到英雄互娱
/data2/hero_sdk_hdc_send_file.sh ${dest_dir} ${date_y}

echo "[`date`] $0 ends!" >> /data2/hero_bi_data/log.txt