#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random,time

'''
排序算法
算法（Algorithm）是指解题方案的准确而完整的描述，是一系列解决问题的清晰指令，算法代表着用系统的方法描述解决问题的策略机制。也就是说，能够对一定规范的输入，在有限时间内获得所要求的输出。如果一个算法有缺陷，或不适合于某个问题，执行这个算法将不会解决这个问题。不同的算法可能用不同的时间、空间或效率来完成同样的任务。一个算法的优劣可以用空间复杂度与时间复杂度来衡量。

    一个算法应该具有以下七个重要的特征：
①有穷性（Finiteness）：算法的有穷性是指算法必须能在执行有限个步骤之后终止；
②确切性(Definiteness)：算法的每一步骤必须有确切的定义；
③输入项(Input)：一个算法有0个或多个输入，以刻画运算对象的初始情况，所谓0个输     入是指算法本身定出了初始条件；
④输出项(Output)：一个算法有一个或多个输出，以反映对输入数据加工后的结果。没       有输出的算法是毫无意义的；
⑤可行性(Effectiveness)：算法中执行的任何计算步骤都是可以被分解为基本的可执行       的操作步，即每个计算步都可以在有限时间内完成（也称之为有效性）；
⑥高效性(High efficiency)：执行速度快，占用资源少；
⑦健壮性(Robustness)：对数据响应正确。

    算法时间复杂度
看别人写算法效率高不高（logn最高,O(1)常数不算）：
O(1)>O (log2n) > O(N) >= O (nlog2n)>O(n^2)> O(n^2 +logn)>O(n^3)...>O(n^k)

写算法最少控制在o(n^2) 空间控制在O(1)：

    空间复杂度：
你的算法使用的空间需要多少，一般情况就是暂用了临时的内存，就算占用也是很少，所以空间复杂度一直是O(1)，如果空间复杂度是O(N)等于是复制了一份到内存，根本就没必要
'''


'''
实战
    冒泡排序O(n^2)
普通版本
1.列表从第一个元素进行和相邻的元素进行比大，进行互换（大的往右规则互换），接着大的元素继续和后面相邻的元素进行比大，以此类推，最终列表最大的元素放置到了最右边（该次循环结束）
2.继续循环（上次循环得到最大元素切片出来（不包含在列表里面）），然后按照上面的方式继续把该次列表最大的元素放置在最右边
3.以上面方式，最终排序完毕（按照上面的情况每次循环只能提取一个最大的元素放置最右边，那么外层就应该还有个循环是根据列表元素数量的，这样循环套循环最终才排序出来）
详情：看实验（与选择排序（普通版）类似）
'''
def bubble1_sort(array):
    for i in range(len(array)):
        #array = [3,2,8,1]
        #len(array) = 4
        #i=0 i=1 i=2
        for j in range(len(array)-1-i,):
            #len(array)-1-i == 4-1-0 = 3
            #j=0 j=1 j=2 j=3
            if array[j] > array[j+1]:  #array[0] > array[1]  ==  3 > 2
                tmp = array[j] #tmp = 3
                array[j] = array[j+1] #array[0] = 2
                array[j+1] = tmp    #array[1]  =3
#第1次大循环的内部循环i=0  range(len(array)-1-i,) == range(3)
#内部循环最终结果 array = [2,3,1,8]  每次内部循环结果会把列表里面最大元素放到最右边
#第2次大循环的内部循环i=1  range(len(array)-1-i,) == range(2)
# 内部循环最终结果 array = [2,1,3,8]
#以此类推最终就排序了
def bubble1_sort_test():
    array =[] # [3,2,8,1]
    for i in range(1000):
        array.append(random.randrange(1000))
    #print(array)
    time_start = time.time()
    bubble1_sort(array)
    time_end = time.time()

    print(array[0:10])
    print("cost:",time_end-time_start)



'''
优化版本
1.列表从第一个元素进行和相邻的元素进行比大，大的下标进行标记（此刻不替换）再用标记好的下标元素和其他的元素比大（同理不替换），以此类推找到了列表中最大的元素下标，循环结束，然后把最大元素的下标和该列表最右的元素进行替换位置。
2.继续循环（上次循环得到最大元素切片出来（不包含在列表里面）），然后按照上面的方式继续把该次列表最大的元素放置在最右边
3.以上面方式，最终排序完毕（按照上面的情况每次循环只能提取一个最大的元素放置最右边，那么外层就应该还有个循环是根据列表元素数量的，这样循环套循环最终才排序出来）
详情：看实验（与选择排序（优化版）相反）
'''
def bubble2_sort(array):
    for i in range(len(array)):
        #array = [3,2,8,1]
        #len(array) = 4
        #i=0 i=1 i=2
        bigess = 0
        for j in range(0,len(array)-i):
            if array[bigess] < array[j]:
                bigess = j
        tmp = array[-1-i]
        array[-1-i] = array[bigess]
        array[bigess] =tmp

def bubble2_sort_test():
    array =[] # [871, 100, 160, 755, 614, 621, 403, 671, 256, 915, 174, 906, 253, 973, 199, 370, 950, 970, 287, 648]
    for i in range(1000):
        array.append(random.randrange(1000))
    time_start = time.time()
    bubble2_sort(array)
    time_end = time.time()
    print(array[0:10])
    print("cost:",time_end-time_start)


'''
选择排序O(n^2)
普通版本

1.    列表左边第1个元素进行其他的后面元素进行比小，小的元素替换成为左边第1个的元素，继续和其他的比，以此类推列表左边第一个元素是最小的，该次循环结束
2.    继续循环（上次左边的最小元素被切片了，当做不在列表内），形式如上找到最小的元素放在左边的第一个位置上
3.    按照以上方式最终完成选中排序
详情：看实验（与冒泡排序（普通版）类似）
'''
def selection1_sort(array):
    # array = [3,2,8,1]
    # len(array) = 4
    # i=0 i=1 i=2
    for i in range(len(array)):
        for j  in range(i,len(array)):
            if array[i] > array[j]:
                tmp = array[i]
                array[i] = array[j]
                array[j] = tmp

def selection1_sort_test():
    array = []
    # array =[871, 100, 160, 755, 614, 621, 403, 671, 256, 915, 174, 906, 253, 973, 199, 370, 950, 970, 287, 648]
    for i in range(1000):
        array.append(random.randrange(1000))
    time_start = time.time()
    selection1_sort(array)
    time_end = time.time()
    print(array[:10])
    print("cost:",time_end-time_start)


'''
优化版本

1.列表左边第1个元素进行其他的后面元素进行比小，小的下标进行标记（此刻不替换）再用标记好的下标元素和其他的元素比小（同理不替换），以此类推找到了列表中最小的元素下标，循环结束，然后把最小元素和该列表最左边的元素进行替换位置。
2.继续循环（上次循环得到最小元素切片出来（不包含在列表里面）），然后按照上面的方式继续把该次列表最小的元素放置在最左边
3.以上面方式，最终排序完毕（按照上面的情况每次循环只能提取一个最小的元素放置最左边，那么外层就应该还有个循环是根据列表元素数量的，这样循环套循环最终才排序出来）
详情：看实验（与冒泡排序（优化版）类似，规则也差不多）
'''
def selection2_sort(array):
    for i in range(len(array)):
        #array = [3,2,8,1]
        #len(array) = 4
        #i=0 i=1 i=2
        smallest_index = i
        for j  in range(i,len(array)):
            if array[smallest_index] > array[j]:
                smallest_index = j
        tmp = array[i]
        array[i]= array[smallest_index]
        array[smallest_index] = tmp

def selection2_sort_test():
    array =[] #[871, 100, 160, 755, 614, 621, 403, 671, 256, 915, 174, 906, 253, 973, 199, 370, 950, 970, 287, 648]
    for i in range(1000):
        array.append(random.randrange(1000))
    time_start = time.time()
    selection2_sort(array)
    time_end = time.time()
    print(array[:10])
    print("cost:",time_end-time_start)


'''
插入排序O(n^2)
for循环从下标1元素开始循环，记录下标1的元素，然后进行while循环，首先下标1跟下标0的元素进行比较，如果比下标0的元素小，那么久把下标0的元素替换到下标1的位置，下标1刚开始被记录的就替换到下标0，因为下标0是边界，所以排序完成
示例：[3,7,12,22,8]   x=8
while1: [3,7,12,22,22]
while2:[3,7,12,12,22]
while3:[3,7,7 ,12,22]
停止循环
last [3,7, 7-->x=8,12,22]
'''
def insertion_sort(source):
    for index in range(1,len(source)):
        current_val = source[index] #先记下来每次大循环走到的第几个元素的值
        position = index

        while position > 0 and source[position-1] > current_val: #当前元素的左边的紧靠的元素比它大,要把左边的元素一个一个的往右移一位,给当前这个值插入到左边挪一个位置出来
            source[position] = source[position-1] #把左边的一个元素往右移一位
            position -= 1 #只一次左移只能把当前元素一个位置 ,还得继续左移只到此元素放到排序好的列表的适当位置 为止

        source[position] = current_val #已经找到了左边排序好的列表里不小于current_val的元素的位置,把current_val放在这里
        # print(source)

def insertion_sort_test():
    source =[] #[64, 77, 67, 8, 6, 84, 55, 20, 43, 67] #[871, 100, 160, 755, 614, 621, 403, 671, 256, 915, 174, 906, 253, 973, 199, 370, 950, 970, 287, 648]
    #[55,64,64,67,77,84] 58
    for i in range(1000):
        source.append(random.randrange(1000))
    time_start = time.time()
    insertion_sort(source)
    time_end = time.time()
    print(source[:10])
    print("cost:",time_end-time_start)


if __name__ == '__main__':
    print('# 冒泡排序1:')
    bubble1_sort_test()
    print('# 冒泡排序2:')
    bubble2_sort_test()
    print('# 选择排序1:')
    selection1_sort_test()
    print('# 选择排序2:')
    selection2_sort_test()
    print('# 插入排序:')
    insertion_sort_test()



