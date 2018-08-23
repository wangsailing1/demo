#!/usr/bin/env bash

# default root dir
_ROOT_PATH='/data/sites/genesis2_dev/'

CUR_PATH=$(cd "$(dirname "$0")"; pwd)

#if [ $# -ne 1 ]; then
#    echo "Usage: `basename $0` <env>"
#    exit 1
#fi

env=$1

ipython -i $CUR_PATH/shell.py $env $_ROOT_PATH
