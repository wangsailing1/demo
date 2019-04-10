# l = []
# a = 0
# b = 1   #b永远绑定当前一个ｆｅｉｂｏ数
# while len(l)<40:
#     l.append(b)   #把当前数加入ｌ中
#     #算出下个数，还用b绑定，ａ绑定当前
#     c = a+b       #算出下一个数
#     a = b           
#     b = c         #b绑定下一个数
# print(l)

# def myfun(a,b,c):
# 	'''这是一个位置传参的示例'''
# 	print('a值',a) 
# 	print('b值',b) 
# 	print('c值',c) 
# myfun(1,2,3)
# myfun(4,5,6)
# myfun("ABC",[1,2,3],(44,55,66))
# def myfun(a,b,c):
# 	'''这是一个序列传参的示例'''
# 	print('a值',a) 
# 	print('b值',b) 
# 	print('c值',c) 
# l = [11,22,33]
# myfun(l[0],l[1],l[2])
# myfun(*l)
# def myfun(a,b,c):
# 	'''这是一个关键字传参的示例'''
# 	print('a值',a) 
# 	print('b值',b) 
# 	print('c值',c)
# myfun(c=33,b=22,a=11)
# myfun(b=222,c=333,a=111)
# def myfun(a,b,c):
# 	'''这是一个字典关键字传参的示例'''
# 	print('a值',a) 
# 	print('b值',b) 
# 	print('c值',c)
# d = {'a':100,'c':300,'b':200}
# myfun(a=d['a'],c=d['c'],b=d['b'])
# myfun(**d)

#课堂练习)
# def minmax(a,b,c):
#     da = max(a,b,c)
#     xiao = min(a,b,c)
#     return (xiao,da)
# t = minmax(300,200,100)
# print(t)
# t2 = (1,3,2)
# t3 = (minmax(*t2))
# print(t3)

# def info(name,age=1,address='不详'):
# 	print(name,'今年',age,'岁,家庭住址:',address)
# info("魏明泽",35,"北京市朝阳区")
# info("tarena",15,)
# info("张飞")
# info()  #出错


# def myadd(a,b,c=0,d=0):
#     return(a+b+c+d)
# print(myadd(4,9,19,28))
# print(myadd(2,3,4))
# print(myadd(3,4))

# variadble_args.py
# l = [1,2,3]
# def f1(l):
# 	a = [4,5,6]
# 	print(l)
# f1(l)
# print(l)

# l = [1,2]
# def fn(a,lst=[]):
# 	lst.append(a)
# 	print(lst)
# fn(3,l)
# fn(4,l)
# fn(5)
# fn(6)
# fn(7)
# fn(8)


import threading

















