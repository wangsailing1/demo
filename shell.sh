#!/usr/bin/env bash

# default root dir
CUR_PATH=$(cd "$(dirname "$0")"; pwd)

#if [ $# -ne 1 ]; then
#    echo "Usage: `basename $0` <env>"
#    exit 1
#fi

env=$1

ipython -i $CUR_PATH/shell.py $env $CUR_PATH
