#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import copy
import sys

'''
二分查找（两种方式：递归和while）
1.对列表进行排序
2.计算出列表的长度，
3.通过长度除以2变整数取出列表中间下标的元素
4.要查找的的数字和列表中间的元素进行判断
         如果该数字<中间的元素，说明中间元素的后面元素们就不用找了
                   我们就应该取该列表中间元素的下标-1作为结尾的下标
         如果该数字>中间的元素，说明中间元素的前面元素们就不用找了
             我们就应该取该列表中间元素的下标+1作为起始的下标
'''

def cal_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print("%s running time: %s secs." % (func.__name__, t2 - t1))
        return result
    return wrapper

@cal_time
def bin_search(data_set, val):
    low = 0
    high = len(data_set) - 1
    while low <= high:
        mid = (low+high)//2
        if data_set[mid] == val:
            return data_set[mid]
        elif data_set[mid] < val:
            low = mid + 1
        else:
            high = mid - 1
    return


#装饰器不可以装饰在递归函数
#那么可以使用一种方法就是另起一个函数，接收该递归函数的结果，这样装饰
def binary_search(dataset, find_num):
    if len(dataset) > 1:
        mid = int(len(dataset) / 2) #该列表中间元素的下标
        if dataset[mid] == find_num:
            #print("Find it")
            return dataset[mid]
        elif dataset[mid] > find_num:
            return binary_search(dataset[0:mid], find_num)
            # 如果该数小于列表中间的元素
            # 这里很清楚如果小于中间的元素代表后面的元素就不用查了
            # 那么我们只需要把中间元素的下标mid-1作为结尾下标进行递归寻找
        else:
            return binary_search(dataset[mid + 1:], find_num)
            # 如果该数大于于列表中间的元素
            # 这里很清楚如果大于中间的元素代表前面的元素就不用查了
            # 那么我们只需要把中间元素的下标mid+1最为起始下标进行递归寻找

    else:
        if dataset[0] == find_num:
            #print("Find it")
            return dataset[0]
        else:
            pass
            print("Cannot find it.")

#装饰器不可以装饰在递归函数
#那么可以使用一种方法就是另起一个函数，接收该递归函数的结果，这样装饰
@cal_time
def binary_search_alex(data_set, val):
    return binary_search(data_set, val)


def binary_search_test():
    data = list(range(1000))
    print(bin_search(data, 120))
    print(binary_search_alex(data, 120))


'''
top榜单排序
场景（榜单TOP）：如微博，新闻等排行榜，要从提取点赞最多的新闻排行榜，或者评论排行榜的前10名or前20名等等...
就需要在某个列表中取出排序最小的10个元素（等于点赞最多的）形成一个新的列表（排序完毕），其他的元素无需理会（不管是否有排序）
'''
def cal_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print("%s running time: %s secs." % (func.__name__, t2 - t1))
        return result
    return wrapper

###############Python自带排序###################
@cal_time
def sys_sort(data):
    return data.sort()
######################################


#######题目#####################################
#现在又n个数（n>10000),设计算法，按大小顺序排序后，我们只需要得到前面0-9的下标元素,其余不要
##############################################################

##############O(n)方案############################
#示例演变：得到li列表排序好的前3个元素，其余元素排序不排序不理会
#1. li = [1,3,5,4,2,7,9,6,8]
#2. top = [1,3,5,4] 提取了li列表的前4个元素形成top列表
        #对top列表使用插入排序 得到 top = [1,3,4,5]
#3. top[3] = li[4]    top[3] = 2   top=[1,3,4,2]
        # 对top列表使用插入排序 得到 top = [1,2,3,4]
#按照上面这种方式，不断的把li的元素进行替换top列表执行插入排序
#直到li的元素全被替换完毕，结果自然就出来，我们也得到了前面4个排序好的元素（切片取前3个）

#简单的来说：
    #1从真正的列表提取前面11个元素形成临时列表，对临时列表进行插入排序
    #2.真正列表只需要进行循环从12个元素开始替换掉临时列表的第11个元素
    #3.临时列表第11个元素被替换就执行一次插入排序（排序11个元素的列表）
    #4.最终临时列表得到了真正列表所有元素排序过后的11个最小的元素，那么提取前10个元素就OK了

def insert(li, i):
    '''
    row1
    :param li: [1,5,2,4]
    :param i: 1
    row2
    :param li: [1,5,2,4]
    :param i: 2
    row3
    :param li: [1,5,2,4]
    :param i: 3
    '''
    tmp = li[i]
    j = i - 1
    while j >= 0 and li[j] > tmp:
        li[j + 1] = li[j]
        j = j - 1
    li[j + 1] = tmp

def insert_sort(li):
    '''
    :param li: [1,5,2,4]
    :return:
    '''
    for i in range(1, len(li)):  #range(1, len(li)) == [1,2,3]
        insert(li, i)  #调用 insert ([1,5,2,4],1)  #得到了li = [1,5,2,4]
                       #调用 insert ([1,5,2,4],2)  #得到了li = [1,2,5,4]
                        # 调用 insert ([1,5,2,4],3)  #得到了li = [1,2,4,5]
@cal_time
def topk(li, k):
    '''
    假设
    :param li: [1,5,2,4,3]
    :param k: 3  #获取排序完毕前3个元素
    :return:
    '''
    top = li[0:k + 1]  #[1,5,2,4] ,为什么要4个，是预留后面排序中插入到前面的元素，
    insert_sort(top)   #调用insert_sort该函数  得到 top = [1,2,4,5]
    for i in range(k+1, len(li)): #range(k+1, len(li) == range(4,len(1,5,2,4,3)) == [4,5]
        top[k] = li[i]   #top[3] = li[4]   ==  top =  [1,2,4,3]
        insert(top, k)  #重新开始排序得出前3位
    return top[:-1]
####################################################


####堆的方案##########################################

def sift(data, low, high):
    '''
    根据完全二叉树堆的原理，通过非叶子节点最终把列表元素最大的替换到列表的下标0
    #示例演变：得到li列表排序好的前4个元素，其余元素排序不排序不理会
    #1. li = [1,5,7,4,3,8,2,0]
    #2. heap=[1,5,7,4,3] 提取了li列表的前5个元素形成heap列表
            #对heap列表使用堆排序（列表最大的元素替换到下标 0）
    #3. 条件如果 heap[0]>li[5]才执行heap[0] =li[5] 替换li第6个元素（等于把heap最大的元素扔掉）
            （循环整个li列表下标了5开始到结尾）
            每替换heap一个大元素就进行对heap列表使用堆排序
            以此类推最终：循环最终heap该列表得到了最小的5个元素
    #4  在遍历heap该列表，让其进行排序（元素小的往前面）
#简单的来说：
    #1从真正的列表提取前面10个元素形成临时列表，进行对该临时列表进行堆排序，先对临时列表变成大顶堆（下标0元素最大）
    #2.真正列表只需要进行循环从12个元素开始到结尾每次判断元素否小于临时列表的下标0该元素吗，小就替换
    #3.临时列表的下标0元素被替换以后就不在是大顶堆了，如果继续堆排序成为大顶堆，如此循环到真正列表元素结束为止
    #4.最终临时列表获取到了最小的5个元素，我们在进行堆排序头尾替换循环遍历对该列表进行排序
    row1:
    :param data: [1,5,7,4,3]
    :param low: 1
    :param high: 4
    row2:
    :param data: [1,5,7,4,3]
    :param low: 0
    :param high: 4
    :return:
    '''
    i = low     #非叶子节点（子树）
        # row1:i=1
        # row2: i=0
    j = 2 * i + 1   #左孩子
        #row1: j=3
        #row2: j=1
    tmp = data[i]
        # row1: tmp=5
        # row2: tmp=1
    while j <= high:
        #row1: 3<= 4  成立
        #row2: 1<= 4  成立
        #row2_while j=5 <= 4 不成立 执行结束 data = [7,5,1,4,3]
        if j + 1 <= high and data[j] < data[j+1]:
               #row1: j+1 = 4：右孩子   4<=4 and 4 < 3    不成立
               #row2: j+1 = 2 :右孩子   2<=4 and 5 < 7   成立
            j += 1   #j指向右孩子
                # row2: j+1 = 2 :右孩子

        if data[j] > tmp:
            #row1: 4>5不成立
            #row2: j=2 7>1 成立
            data[i] = data[j]   #孩子填到父亲的空位上
                # row2:  data[i] = 1  替换成  7  data[i] =7  data = [7,5,1,4,3]
                # while1: data = [5,4,7,1,3]
            i = j
                #row2：j成为了非叶子节点 i = 2
            j = 2 * i +1
                #row0：新左孩子3  j=5
            #row2_while1循环
        else:
            break
    data[i] = tmp           #最高领导放到父亲位置

@cal_time
def topn(li, n):
    '''
    假设
    :param li: [1,5,7,4,3,8,2,0]
    :param n: 5 #获取排序完毕前4个元素
    :return:
    '''
    heap = li[0:n]   #heap=[1,5,7,4,3]

    #该循环负责吧指定列表进行完全二叉树堆排序最大的元素替换到列表的下标0位置
    for i in range(n // 2 - 1, -1, -1):  #==for i in [1,0]  #1为非叶子节点（子树）
        sift(heap, i, n - 1)  # row1:  sift([1,5,7,4,3],1,4) 获取到  heap = [1,5,7,4,3]
                            #row2:  sift([1,5,7,4,3],0,4) 获取到  heap = data = [7,5,1,4,3]

    #遍历
    for i in range(n, len(li)):  #5,8  == for i in [5,6,7]
        if li[i] < heap[0]:
            # row1:  li[5]=8 < heap[0]=7 不成立
            # row2:  li[6]=2 < heap[0]=7 成立
            # row3:  [5,2,1,4,3]   li[7]=0 < heap[0]=5 成立
            heap[0] = li[i]
            # row2:  heap = [2,5,1,4,3]    li=[2,5,7,4,3,8,7,0]
            # row3:  heap = [0,2,1,4,3]    i=[0,5,7,4,3,8,7,5]
            sift(heap, 0, n - 1)
            # row2: sift([2,5,1,4,3],0,4)  获取到：heap = [5,2,1,4,3]
            # row3:sift([0,5,1,4,3],0,4)   获取到：heap = [4,0,1,2,3]

    for i in range(n - 1, -1, -1):  # i指向堆的最后  [4,3,2,1,0]
        heap[0], heap[i] = heap[i], heap[0]  # 领导退休，刁民上位
            #heap = [4, 0, 1, 2, 3]   heap[0]和heap[4]互换位置   [3,0,1,2,4]
            #row2:heap = [3,2,1,0,4] heap[0]和heap[3]互换位置   [0,2,1,3,4]
            #row3:heap = [2,0,1,3,4] heap[0]和heap[2]互换位置   [1,0,2,3,4]
            # row4:heap = 1,0,2,3,4]  heap[0]和heap[2]互换位置   [0,1,2,3,4]
        sift(heap, 0, i - 1)  # 调整出新领导
        # row2: sift(  [3,0,1,2,4]   , 0, 4 - 1) 获取到：heap = [3,2,1,0,4]
        # row3: sift(  [0,2,1,3,4]   , 0, 3- 1) 获取到：heap = [2,0,1,3,4]
        # row4: sift(  [1,0,2,3,4]   , 0, 2 -1) 获取到：heap = [1,0,2,3,4]
        # row5...                         1
        # row6...                         0
        #最终得到了heap = [0,1,2,3,4]
    return heap
############################################################

def top_sort_test():
####################测试3种排序###############################
    data0 = list(range(10000))
    random.shuffle(data0)
    print(topk(data0,10))

    data1 = list(range(10000))
    random.shuffle(data1)
    print(topn(data1, 10))

    data2 = list(range(10000))
    random.shuffle(data2)
    sys_sort(data2)
    print(data2[0:10])


if __name__ == '__main__':
    print('# 二分查找:')
    binary_search_test()
    print('#  top榜单排序:')
    top_sort_test()
