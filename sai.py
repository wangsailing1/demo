#! --*-- encoding:utf-8 --*--
# n = int(input("请输入高度"))
# e = int(n/2+0.5)
# for i in range(1,e+1):
#     print((n-i)*' ',(i+i-1)*'*')
# for a in range(e,n):
#     print(a*' ',(n-a+n-a-1)*'*')

# n = int(input("请输入高度"))
# e = int(n/2+0.5)
# for i in range(n):
#     for c in range(1,n-1):
#         print(' ',end=' ')
#         c+=1
#     for  b in range(2*i-1):
#         if b==0 or  b==i+i-2:
#             print('*',end=' ')
#         else:
#             print(' ',end=' ')
#         b+=1
#     print('\n')
#     i+=1
# # 空菱形
n = int(input("请输入高度"))
d = int(n/2+0.5)
for a in range(1,d+1):
    b = ((d-a+1)*' ')+'*'+((a+a-1-2)*' ')+'*'
    if a ==1:
        print((d-a)*' ','*')
    else:  
        print(b)
if n%2==1:
    for i in range(1,d):
        c = (i+1)*' '+'*'+(d*2-i*2-3)*' '+'*'
        if i ==d-1:
            print((d-1)*' ','*')
        else:
            print(c)
else:
    for i in range(1,d+1):
        c = (i)*' '+'*'+(d*2-i*2-1)*' '+'*'
        if i ==d:
            print((d-1)*' ','*')
        else:
            print(c)











