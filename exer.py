import re
f1 = open('/home/tarena/test/xiao.py', 'w')
with open('/home/tarena/test/test.py','r') as f:
    s = f.readlines()
    print(s)
    a = re.findall('[^\u4e00-\u9fa5]', s)
    # f1.write(a)

f1.close()

