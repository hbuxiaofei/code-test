#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Visitor Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


# 定义一个表示元素（Element）的接口
class Element(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def do_entry(self):
        pass


# 定义一个表示访问者（Visitor）的接口
class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visit_element1(self, e):
        pass

    @abstractmethod
    def visit_element2(self, e):
        pass

# 元素实体1
class ConcreteElement1(Element):
    def accept(self, visitor):
        visitor.visit_element1(self)

    def do_entry(self):
        print('This is Element 1')


# 元素实体2
class ConcreteElement2(Element):
    def accept(self, visitor):
        visitor.visit_element2(self)

    def do_entry(self):
        print('This is Element 2')


# 访问者实体
class ConcreteVisitor(Visitor):
    def visit_element1(self, visitor):
        visitor.do_entry()

    def visit_element2(self, visitor):
        visitor.do_entry()


# 对象结构，迭代元素提供访问者访问
class ObjectStruture(object):
    def get_elements(self):
        _list = [ConcreteElement1(),
                 ConcreteElement2()]
        return _list


class Client(object):
    def main(self):
        element_list = ObjectStruture().get_elements()
        for e in element_list:
            e.accept(ConcreteVisitor())


if __name__ == '__main__':
    Client().main()
