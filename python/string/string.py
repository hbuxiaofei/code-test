#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''str字符串常用操作
'''

name = "my \tname is alex"
print(name.capitalize())# 首字母大写

print(name.count("a")) # 统计字母的重复数量

print(name.center(50,"-")) # 把变量放在中间左右输入25个-

print(name.endswith("ex")) # 判断环境变量的结尾是否和输入一致

print(name.expandtabs(tabsize=30))  # 该环境变量的tab建定义成30个空格

print(name.find("name")) # 获取该字符串的第一个字符n的下标4（tab算2个）

print(name[name.find("name"):9]) #切片 4-9  顾头不顾尾所以9不切  所以4-9 是name

print(name.rfind('n')) #找出最右边n该字符的长度位置（空格算一个）


name1 = "my name is {name} and i am {year} old."

print(name1.format(name='hello', year=23)) #变量name1里面大括号{} 可以进行格式化输出

print(name1.isalnum()) #如果name1 不是阿拉伯数字(英文+数字），就是假False

print('1123'.isdecimal()) #判断是否是十进制

print('1A'.isdigit())#判断是否是整数

print('-A'.isidentifier()) #判断是否是一个合法的标识符（合法的变量名）  -A 有-就不合法

print('dfA'.isidentifier()) #该字符串可以变量使用

print('a.1a'.isnumeric()) #判断是否数字 和isdigit没什么区别 不知道存在有什么用

print(' '.isspace()) #判断是否是空格

print('My Name Is'.istitle()) #判断是否是标题(国外标题每个单词的头字母是大写）

print('My Name Is'.isprintable()) #判断是否能够打印显示，如：tty文件设备终端驱动程序就不能打印的

print('MNA'.isupper()) #判断是否全是大写

print('-'.join(['1','2','3'])) #和Linux的tr替换符一样，这里需要加入列表,去除该列表每个元素使用-链接 得出结果是1-2-3

print(name1.ljust(50,'*'))#字符串长度如果不够50就用*在字符串后面补到50长度

print(name1.rjust(50,'-')) #字符串长度如果不够50就用-在字符串前面补到50长度

print('MNA'.lower()) # 变小写

print('abc'.upper()) # 变大写

print('\nBrugess'.lstrip()) #取消左边的回车键和空格键

print( 'Cristal\n'.rstrip()) #取消右边的回车键和空格键

print('\nCristal\n'.strip()) #取消左右边的回车键和空格键

p = str.maketrans("abcdefghi",'#@$%@%^&@')
print("hello world".translate(p))

print("hello world".replace('w','W')) #替换字符

print("hello world".replace('o','O',1)) #置换第一个对应的字符

print("he llo wor ld".split()) #换成列表格式默认空格为间隔分配下标

print("hel lo wor ld".split('o')) #转换成列表 指定o为间隔分配下标

print("1+2+3+4".split('+')) #转换成列表 指定+为间隔分配下标

print("1+2\n3+4".splitlines())  #转换成列表 指定换行建为间隔分配下标（自动识别不同系统的换行符）

print("Hello WORLD".swapcase())  #大小写互换

print("Hello WORLD".title())  #变成标题 单词第一个字母大写其他小写

print("Hello WORLD".zfill(50))  #不够自动用0在字符串的前面补位
