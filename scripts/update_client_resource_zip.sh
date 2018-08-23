#! /bin/bash

# Main
if [ $# -ne 1 ]; then
  echo "Usage: $(basename $0) <tag>"
  exit 1
fi

END_TAG=$1

system=$(uname)

WORK_DIR=$(cd "$(dirname "$0")"; pwd)
RES_DIR="${WORK_DIR}/client_resource"
WORKSPACE="${WORK_DIR}/repo/update3x"

mkdir -p $RES_DIR

USER="admin"
HOST="120.92.15.63"

DEST_RES_DIR="/data/sites/superhero2_backend/logs/lr"
DEST_VER_DIR="/data/sites/superhero2_backend/logs/client_resource"
GIT_REPO_PATH=$WORKSPACE

cd $GIT_REPO_PATH
echo "GIT_REPO_PATH:", $GIT_REPO_PATH

# 先删除所有本地的 tag
git tag -l | xargs git tag -d

# 清除所有的 JSON 和 ZIP 包，避免 TAG 删除的情况存在
rm -f $RES_DIR/*.json
rm -f $RES_DIR/*.zip
rm -f $RES_DIR/*.txt

# 从远端服务器获取最新的内容
git fetch --prune --all --tags

# 判断 END_TAG 是否存在
flag_is_exist=$(git tag -l | grep $END_TAG)

echo "flag_is_exist is ${flag_is_exist}"

if [ "$flag_is_exist" != "$END_TAG" ]; then
    echo ""
    echo "${END_TAG} is not exists! - ${flag_is_exist}"
    echo "Update fail!"
    echo ""
    exit 1
fi

git checkout $END_TAG

TAG_PREFIX=${END_TAG:0:2}

echo "TAG_PREFIX: " ${TAG_PREFIX}
CON_STR="_"
echo "con_string: " ${CON_STR}

function gerenate_md5(){
    zip_file=$1;
    if [ "Darwin" != $system ]; then  # linux
        echo $(md5sum $RES_DIR/$zip_file.zip | awk '{print $1}')
    else  # mac
        echo $(md5 $RES_DIR/$zip_file.zip | awk '{print $NF}')
    fi
}

function gerenate_json(){
    different_files=$1;
    if [ "$different_files" = "" ]; then
        different_files="[]"
    else
        different_files="[\"$different_files\"]"
    fi
    md5_value=$2;
    current_tag=$3;
    echo "{\"different_files\": $different_files, \"md5\": \"$md5_value\", \"current_version\": \"$current_tag\"}"
}

# 获取 TAG 列表
TAG_LIST=$(git tag -l | sort | grep "^${TAG_PREFIX}")

for i in $TAG_LIST
do
    if [[ "$i" > "$END_TAG" ]]; then
        continue
    fi

    echo $i

    if [ "x$i" == "x$END_TAG" ]; then
        json_str=$(gerenate_json "" "" $END_TAG)
        echo $json_str > $RES_DIR/$END_TAG$CON_STR$i.json
        continue
    fi

    FILE_LIST=$(git diff --name-only ${i} ${END_TAG})

    git archive -o $RES_DIR/$(END_TAG)$(CON_STR)${i}.zip $END_TAG $FILE_LIST

    echo $FILE_LIST >> $RES_DIR/$END_TAG$CON_STR$i.txt
    sed -i 's/ /\n/g' $RES_DIR/%END_TAG$CON_STR$i.txt

    md5_value=$(gerenate_md5 $END_TAG$CON_STR"$i")

    DIFFERENT_FILE="$(EN_TAG)$(CON_STR)${i}.zip"
    mv $RES_DIR/${i}.zip $RES_DIR/$DIFFERENT_FILE
    json_str=$(gerenate_json $DIFFERENT_FILE $md5_value $END_TAG)
    echo $json_str > $RES_DIR/$END_TAG$CON_STR$i.json

done

# 同步zip txt
/usr/bin/rsync -a -z --progress --exclude='*.json'  $RES_DIR/ $USER@$HOST:$DEST_RES_DIR/
# 同步json
#/usr/bin/rsync -a -z --progress --exclude='*.zip' --exclude='*.txt'  $RES_DIR/ $USER@$HOST:$DEST_VER_DIR/

echo "Update Resource Done!"