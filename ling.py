# for i in range(1,20):
#     if i==10:
#         print("*")
#     else:
#         print(" ",end='')
for j in range(9,4,-1):
    for i in range(1,20):
        if i==j:
            print('*',end='')
        elif i==20-j:
            print('*')
            break
        else:
            print(" ",end='')
# for j in range(4,10):
#     for i in range(1.20):
#         if i==j:
#             print('*',end='')
#         elif i==20-j:
#             print('*')
#         else:
#             print(' ',end='')


# for x in  map(pow,[1,2,3,4],[4,3,2,1],range(5,10)):
#     print(x)
# def mysum(x):
#     return x**2
# s = sum(map(mysum,range(1,10)))
# print("和是:",s)
# def mysum2(x):
#     return x**3
# l=[]
# for i in map(mysum2,range(1,10)):
#     l.append(i)
# print(sum(l))



# s = sum(map(lambda x:x**2,range(1,10)))
# print(s)
# s = sum(map(lambda x:x**3,range(1,10)))
# print(s)
# s = sum(map(pow,range(1,10),range(9,0,-1)))
# print(s)

# names = ['tom','jerry','spike','tyke']
# def fn(x):
#     return x[::-1]
# l = sorted(names,key=fn)
# print(l)

# s = '1234'
# l = 0
# for i in s:
#     for a in s:
#         if a != i:
#             for b in s:
#                 if b != a and b != i:
#                     for c in s:
#                        if c !=b and c != a and c!=i: 
#                             l+=1
#                             print(i,a,b,c)
# print("总共能组成%d"%l)



