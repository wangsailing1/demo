
# 一)
# def sum3(a,b,c):
#     return (a+b+c)
# print(sum3(1,2,3))
# print(sum3(5,6,7))
# def pow3(x):
#     return(x**3)
# print(pow3(9))
# s = sum3(pow3(1),pow3(2),pow3(3))
# print(s)
# a = pow3(sum3(1,2,3))
# print(a)

# 三)
# def Sn(n):
#     s = 0
#     for i in range(1,n+1):
#         s+=1/(i*(i+1))
#     return s
# b = int(input("请输入整数"))
# print(Sn(b))


# #二)
# def input_student():
#     l = []                                                   #定义一个列表
#     while True:                                              #进行死循环
#         d = {}                                               #定义一个空字典
#         a = input("请输入姓名")                                
#         if not a:                                            
#             break                                            #如果输入为空的话推出循环
#         b = int(input("请输入年龄"))
#         c = int(input("请输入成绩"))
#         d['name']=a                                          #在字典d创建键(name)组对
#         d['age']=b                                           #在字典d创建键(age)组对
#         d['cheng']=c                                         #在字典d创建键(cheng)组对
#         l.append(d)                                          #把字典放到列表
#     return l 
# infos = input_student()
# print(infos)
# def output_student(w):
#     s = []                                                  #定义列表
#     for i in w:
#         x=len(i['name'])                                    #定义'name'键的值的长度为x
#         s.append(x)                                         #把x追加到列表s里
#     v=max(s)                                                #定义s列表里的最大值为v
#     m = '+'+(v*'-')+'+'+(v*'-')+'+'+(v*'-')+'+'             #做表的第１行
#     h = '|'+'姓名'.center(v-2)+'|'+'年龄'.center(v-2)+'|'+'成绩'.center(v-2)+'|'   #做表的第2行
#     print(m)                                                #输出第1行
#     print(h)                                                #输出第2行
#     print(m)                                                #输出第3行
#     for i in w:                                             #l列表里的个数作为循环输出次数
#         a1=i['name']                                        #定义i字典'name'的值为a1
#         a2=str(i['age'])                                    #定义i字典'age'的值为a2
#         a3=str(i['cheng'])                                  #定义i字典'cheng'的值为a3
#         k=('|'+a1.center(v)+'|'+a2.center(v)+'|'+a3.center(v)+'|') #定义a1.a2.a3宽度为v进行居中为k
#         print(k)                                            #循环输出
#         print(m) 
#     return "开心就好"    
# print(output_student(infos))

# 1.写一个函数 get_chinese_char_count(s),此函数的功能是给一个字符串，返回这个字符串中中文字符的个数
# 如：
# def get_chinese_char_count(s):
#     count = 0
#     for ch in s:
#         if 0x4e00<=ord(ch)<=0x9fa5:
#             count += 1
#     return count
# n = input("请输入中英混合的字符串:")
# print('您输入的中文个数是:',get_chinese_char_count(n))
# 注：中文字符的编码在0x4E00-0x9FA5 之间


# 2.写一个函数isprime(x)判断x是否为素数，如果为素数返回Ture,否则返回False
# 如：
# def isprime(a):
#     for i in range(2,a):
#         if a%i==0:
#             return False
#     return True
# n = int(input("请输入整数"))
# print(isprime(n))    #Ture
# print(isprime(4))     #False

# # 3.写一个函数prime_m2m(m,n)返回从m开始，到n结束范围内的全部素数的列表，并打印对应的列表
# # 如：
# def print_m2n(m=0,n=0):
#     l = []
#     for i in range(m,n):
#         if isprime(i):
#             l.append(i)
#     return l
# a = int(input("请输入开始数"))
# b = int(input("请输入结束数"))
# l = print_m2n(a,b)
# print(l)  #[11,13,17,19]

# 4.写一个函数primes(n)返回指定范围内的全部素数(不包含n)的列表，打印印这些素数的列表，如：
# def primes(m=2,n=0):
#     l = []
#     for i in range(m,n):
#         if isprime(i):
#             l.append(i)
#     return l
# a = int(input("请输入结束数"))
# l = primes(n=a)
# print(l,sum(l))   #[2,3,5,7]
# 打印100以内
# 打印200以内


# def myrange(qi=0,n=0,bu=1):
#     l = []
#     l1=[]
#     a = qi
#     if n==0 or qi>n:
#         qi,n=n,qi
#         a = qi
#     while a<n:
#         l1.append(a)
#         a+=1
#     if bu>0:
#         l=l1[qi-1:n:bu]
#     else:
#         l1.append(n)
#         l=l1[n:qi-1:bu]
#     return l
# print(myrange(10,1,-1))
# l = list(myrange(1,20))
# print(l)
# l = list(myrange(20,1,-1))
# print(l)
# l = list(range(1,20))
# print(l)
# l = list(range(20,1,-2))
# print(l)

# 一)
# mysum = lambda n: sum(range(n+1))
# print(mysum(100))

# 二)
# def myfac(n):
#     s = 1
#     for i in range(1,n+1):
#         s *= i
#     return s
# print(myfac(5))

# 三)
# def he(n):
#     s = 0
#     for i in range(1,n+1):
#         s+=i**i
#     return s
# print(he(5))


def input_student():
    l = []                                                   #定义一个列表
    while True:                                              #进行死循环
        d = {}                                               #定义一个空字典
        a = input("请输入姓名")                                
        if not a:                                            
            break                                            #如果输入为空的话推出循环
        b = int(input("请输入年龄"))
        c = int(input("请输入成绩"))
        d['name']=a                                          #在字典d创建键(name)组对
        d['age']=b                                           #在字典d创建键(age)组对
        d['cheng']=c                                         #在字典d创建键(cheng)组对
        l.append(d)                                          #把字典放到列表
    return l 
def output_student(w):
    s = []                                                  #定义列表
    for i in w:
        x=len(i['name'])                                    #定义'name'键的值的长度为x
        s.append(x)                                         #把x追加到列表s里
    v=max(s)                                                #定义s列表里的最大值为v
    m = '+'+(v*'-')+'+'+(v*'-')+'+'+(v*'-')+'+'             #做表的第１行
    h = '|'+'姓名'.center(v-2)+'|'+'年龄'.center(v-2)+'|'+'成绩'.center(v-2)+'|'   #做表的第2行
    print(m)                                                #输出第1行
    print(h)                                                #输出第2行
    print(m)                                                #输出第3行
    for i in w:                                             #l列表里的个数作为循环输出次数
        a1=i['name']                                        #定义i字典'name'的值为a1
        a2=str(i['age'])                                    #定义i字典'age'的值为a2
        a3=str(i['cheng'])                                  #定义i字典'cheng'的值为a3
        k=('|'+a1.center(v)+'|'+a2.center(v)+'|'+a3.center(v)+'|') #定义a1.a2.a3宽度为v进行居中为k
        print(k)                                            #循环输出
        print(m) 
    return "开心就好"    
def chakan():
    print("+------------------------+")
    print("1.添加学生信息　　　　　|")
    print("2.查看学生信息　　　　　|")
    print("3.删除学生信息　　　　　|")
    print("4.修改学生信息　　　　　|")
    print("q.退出　　　　　　　　　|")
    print("5.按学生成绩高－低　　　|")
    print("6.按学生成绩低－高　　　|")
    print("7.按学生年龄高－低　　　|")
    print("8.按学生成绩低－高　　　|")
    print("+------------------------+")
def shanchu(l):
    s = input("请输入删除谁")
    n=0
    while n<len(l):
        if l[n]['name']==s:
            del l[n]
            print("删除成功")
        n+=1    
def xiugai(w):
    s = input("请输入要修改的学生名字")
    a = int(input("请输入新分数"))
    n=0
    while n<len(w):
        if w[n]['name']==s:
            w[n]['cheng']=a
        n+=1
def chenggao(l):
    l1=sorted(l,key=lambda x:x['cheng'],reverse=True)
    output_student(l)
def chengdi(q):
    l2=sorted(q,key=lambda x:x['cheng'])
    output_student(l)
def niangao(w):
    l3=sorted(w,key=lambda x:x['age'],reverse=True)
    output_student(l)
def niandi(e):
    l4=sorted(e,key=lambda x:x['age'])
    output_student(l)
def main():
    chakan()
    infos=[]
    while True:
        n=input("请输入")
        if n=='q':
            break
        elif n=='1':
            infos+=input_student()
        elif n=='2':
            output_student(infos)
        elif n=='3':
            shanchu(infos)
        elif n=='4':
            xiugai(infos)
        elif n=='5':
            chenggao(infos)
        elif n=='6':
            chengdi(infos)
        elif n=='7':
            niangao(infos)
        elif n=='8':
            niandi(infos)
main()