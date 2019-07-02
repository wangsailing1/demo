# --*-- encode:utf-8 --*--
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import process

def run(port):
    os.system('/Users/kaiqigu/anaconda2/bin/python2.7 /Users/kaiqigu/Desktop/wang/mychatroom/run.py ' + str(port))

L1 = []
L2 = []
for i in [8000, 8001, 8002, 8003]:
    print i
    p = process.Process(target=run, args=(i, ))
    L1.append(p)
    p.start()

for i in L1:
    print i
    i.join()

