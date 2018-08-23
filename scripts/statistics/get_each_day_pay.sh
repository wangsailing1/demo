#!/bin/sh

env=$1;

filepath=$(cd "$(dirname "$0")"; pwd)

echo "filepath: "$filepath

params=$(python $filepath/tools/pay_config.py $env | tail -n1)
eval $params;

echo "mysql_host: "$mysql_host
echo "mysql_passwd: "$mysql_passwd
echo "mysql_db: "$mysql_db
echo "mysql_user: "$mysql_user
echo "mysql_tprefix: "$mysql_tprefix

if [ ! $mysql_host ]; then
    exit;
fi

for x in 0
do
    k=$(( x + 1 ))
    today=$(date +"%Y-%m-%d 00:00:00" --date=$x' days ago');
    yesterday=$(date +"%Y-%m-%d 00:00:00" --date=$k' days ago');
    hjq_subfix=$(date +"%Y%m%d" --date=$k' days ago');
    echo "$yesterday<=order_time<=$today";
    for j in {0..15};
    do
        mysql -h$mysql_host -u$mysql_user -p$mysql_passwd $mysql_db -N -e"select * from ${mysql_tprefix}_${j} where
        order_time >= '$yesterday' and order_time <= '$today' " >> $filepath/../../statistic/$env/paylog_$hjq_subfix;
    done

done
