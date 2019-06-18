#！--*-- encoding:utf-8 --*--
# print('    *        *')
# print('   * *      * *')
# print('  *     *      *')

# def func(*args):
# 	print("实参的个数:",len(args))
# 	print("args=",args)
# func()
# func(1,2,3,4)


# def mysun (*args):
#     return sum(args)
# print(mysun(1,2,3,4))#10
# print(mysun(1,2,3)) 

# def mysun (*args):
#     s = 0
#     for i in args:
#         s+=i
#     return s 
# print(mysun(1,2,3,4))#10
# print(mysun(1,2,3)) 

# def myprint(*args):


# 二)
# def mymax(*args):
#     da = a = 0
#     for i in args:
#         if i>da:
#             da=i
#     return da
# print(mymax(*[100,1,199,3,45]))
# print(mymax(100,200))
# print(mymax())


#2种)
# def mymax(*args):
#     l = []
#     for i in args:
#         l.append(i)
#         l.sort()
#     return l[-1]
# print(mymax[100,1,2,3,45])


class Node(object):

    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __del__(self):
        print '__del__'

n = Node(0)
del n
# __del__
print '执行到这里'
n1 = Node(1)
n2 = Node(2)
n1.add_child(n2)
del n1 # no output
n2.parent




 