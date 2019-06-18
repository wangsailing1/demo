# encoding:utf8
def insert_sort(L):
    for i in range(len(L)):
        for a in range(i):
            # if L[i] > L[a]:
            if L[i] < L[a]:
                L.insert(a, L.pop(i))
                break
    return L

# 升序,  第一个元素默认有序, 然后跟索引小于他的所有值进行比较, 谁大于他他就去谁的前面
# 降序, 取出一个遍历的元素, 我大余谁, 我就去谁前面

if __name__ == '__main__':
    print(insert_sort([5,4,6,7,3,2,8,1]))




