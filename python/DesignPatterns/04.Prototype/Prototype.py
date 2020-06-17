#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''原型模式（Prototype）

意图：
用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。

适用性：
当要实例化的类是在运行时刻指定时，例如，通过动态装载；或者为了避免创建一个与产品
类层次平行的工厂类层次时；或者当一个类的实例只能有几个不同状态组合中的一种时。建
立相应数目的原型并克隆它们可能比每次用合适的状态手工实例化该类更方便一些。

假如你爱玩游戏，你能想到游戏里面有很多的角色，但是其实你有没有注意:脸型，身材，
眼睛..这些其实都是略有不同的搭配， 这也就是原型的作用：不需要你每次都制造一个复
杂的人物，只是根据一个原型的人物做些简单的修改即可。

'''

# 这里肯定要做深拷贝，要不然python的就是对象的引用
from copy import deepcopy

class Prototype:
    def __init__(self):
        self._objs = {}

    def registerObject(self, name, obj):
        """注册对象"""
        self._objs[name] = obj

    def unregisterObject(self, name):
        """取消注册"""
        del self._objs[name]

    def clone(self, name, **attr):
        """克隆对象"""
        obj = deepcopy(self._objs[name])
        # 但是会根据attr增加或覆盖原对象的属性
        obj.__dict__.update(attr)
        return obj

if __name__ == '__main__':
    class A:
        pass

    a=A()
    prototype=Prototype()
    prototype.registerObject("a",a)
    b=prototype.clone("a",a=1,b=2,c=3)

    # 这里会返回对象a
    print(a)
    # 这里的对象其实已经被修改成(1, 2, 3)
    print(b.a, b.b, b.c)
