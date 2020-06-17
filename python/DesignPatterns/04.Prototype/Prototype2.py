#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''原型模式（Prototype）

案例：展示书籍信息的应用

很多畅销书籍会经历多个版本的迭代。
有变化的信息：价格、长度(页数)以及出版日期。
但也有很多相似之处：作者、出版商以及描述该书的标签/关键词都是完全一样的。这表明从头创建一版新书并不总是最佳方式。
如果知道两个版本之间的诸多相似之处，则可以先克隆一份，然后仅修改新版本与旧版本之间的不同之处。

'''

import copy
from collections import OrderedDict

class Prototype(object):
    def __init__(self):
        self._objects = {}

    def register_object(self, name, obj):
        """
        注册对象实例
        :param name: obj_name -> str
        :param obj: object -> object
        """
        self._objects[name] = obj

    def unregister_object(self, name):
        """
        删除对象
        :param name: object_name -> str
        """
        del self._objects[name]

    def clone(self, id, **attrs):
        """
        从已存在的实例深拷贝一个新实例
        :param name: 被copy的实例
        :param attrs: 新对象属性
        :return: 新对象
        """
        old_obj = self._objects.get(id)
        if not old_obj:
            raise ValueError("Incorrect object name")
        obj_new = copy.deepcopy(old_obj)
        obj_new.__dict__.update(attrs)
        return obj_new

class Book(object):
    def __init__(self, name, authors, price, **kwargs):
        """
        初始化书籍公用信息
        :param name: 书名
        :param authors: 作者
        :param price: 价格
        :param kwargs: 其他信息
        """
        self.name = name
        self.authors = authors
        self.price = price
        self.__dict__.update(kwargs)

    def __str__(self):
        """
        调用print()时自动打印书籍信息
        """
        mylist = []
        ordered = OrderedDict(sorted(self.__dict__.items()))
        for i in ordered.keys():
            mylist.append('{}: {}'.format(i, ordered[i]))
            if i == 'price':
                mylist.append('$')
            mylist.append('\n')
        return ''.join(mylist)

def main():
    book_1 = Book("Python核心编程（第一版）", "Peter", "45.9", publisher="邮电出版社", length="350页")
    prototype = Prototype()
    prototype.register_object('book_1', book_1)

    book_2 = prototype.clone('book_1', name="Python核心编程（第二版）", price="75.9", length="550页")
    print(book_1)
    print(book_2)

if __name__ == "__main__":
    main()
