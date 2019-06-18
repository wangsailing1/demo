#! --*-- coding:utf-8 --*--

def maopai(L):
	for i in range(len(L)):
		for a in range(i+1, len(L)):
			if L[i] > L[a]:
			    L[i], L[a] = L[a], L[i]
	return L

# 每次循环将I的值跟所有的值进行比较, 将最小的值换到第一个, 第二次将第二小的值放在
# 第二个, 以此类推将所有的值遍历一遍
## 遍历出一个值(索引为i), 然后跟列表中的所有值进行比较, 谁比他小, 就跟谁换位置, 这一次比较完
# 当前索引上的值是这些值中最小的

if __name__ == '__main__':
	print(maopai([45,39,4,5,6,32,22,0,2]))
