#!/bin/sh

rsync --progress -alrI ./* 'admin@192.168.1.9:/data/sites/genesis2_dev/'
ssh admin@192.168.1.9 'supervisorctl -u user -p 123 restart genesis2_dev_long_connection'

# genesis2_dev
