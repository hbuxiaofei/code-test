#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Composite Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


# 为组合模式中的对象声明接口
class Component(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def operation(self, depth):
        pass

    @abstractmethod
    def add(self, c):
        pass

    @abstractmethod
    def remove(self, c):
        pass

    @abstractmethod
    def get_child(self, index):
        pass


# 表示组合部件
class Composite(Component):
    def __init__(self, name):
        Component.__init__(self, name)
        self.children = []

    def operation(self, depth):
        strtemp = ''
        for i in range(depth):
            strtemp += strtemp+'-'
        print(strtemp+self.name)
        for comp in self.children:
            comp.operation(depth+2)

    def add(self, c):
        self.children.append(c)

    def remove(self, c):
        self.children.remove(c)

    def get_child(self, index):
        return self.children[index]


# 表示叶节点对象，叶节点对象没有子节点，实现 Component 的所有方法
class Leaf(Component):
    def operation(self, depth):
        strtemp = ''
        for i in range(depth):
            strtemp += strtemp+'-'
        print(strtemp+self.name)

    def add(self, c):
        print('不能添加下级节点！')

    def remove(self, c):
        print('不能删除下级节点！')

    def get_child(self, index):
        print('没有下级节点！')


class Client(object):
    @staticmethod
    def main():
        # 生成树根
        root = Composite("root")
        # 根上长出2个叶子
        root.add(Leaf('leaf A'))
        root.add(Leaf('leaf B'))
        # 根上长出树枝Composite X
        comp = Composite("Composite X")
        comp.add(Leaf('leaf XA'))
        comp.add(Leaf('leaf XB'))
        root.add(comp)
        # 根上长出树枝Composite X
        comp2 = Composite("Composite XY")
        # Composite X长出2个叶子
        comp2.add(Leaf('leaf XYA'))
        comp2.add(Leaf('leaf XYB'))
        root.add(comp2)
        # 根上又长出2个叶子,C和D,D没长好,掉了
        root.add(Leaf('Leaf C'))
        leaf = Leaf("Leaf D")
        root.add(leaf)
        root.remove(leaf)
        # 展示组织
        root.operation(1)


if __name__ == '__main__':
    Client.main()
