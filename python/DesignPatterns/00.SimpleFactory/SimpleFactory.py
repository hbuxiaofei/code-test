#!/usr/bin/env python3
# -*- coding: utf-8 -*-



'''简单工厂模式（Simple Factory）

说明：
严格来说，简单工厂模式不是GoF总结出来的23种设计模式之一。
在工厂模式中，我们在创建对象时不会对客户端暴露创建逻辑，并且是通过使用一个共同的接口来指向新创建的对象。

意图：
定义一个用于创建对象的接口，让子类决定实例化哪一个类。Factory Method 使一个类的实例化延迟到其子类。 

适用性：
当一个类不知道它所必须创建的对象的类的时候。
当一个类希望由它的子类来指定它所创建的对象的时候。
当类将创建对象的职责委托给多个子类中的某一个。

'''


class Shape(object):
    '''
    父类
    '''
    def draw(self):
        raise NotImplementedError

class Circle(Shape):
    '''
    Shape子类
    '''
    def draw(self):
        print('draw circle')

class Rectangle(Shape):
    '''
    Shape的子类
    '''
    def draw(self):
        print('draw Rectangle')

class ShapeFactory(object):
    '''
    工厂模式：暴露给用户去调用的，
    用户可通过该类进行选择Shape的子类进行实例化
    '''
    def create(self, shape):
        if shape == 'Circle':
            return Circle()
        elif shape == 'Rectangle':
            return Rectangle()
        else:
            return None

'''
Shape（父类 or 基类）：提取出所有子类的重复方法代码
Circle（Shape子类 or 派生类）：作用为画圆形
Rectangle（Shape子类 or 派生类）：作用为画矩形
ShapeFactory（新式类）：该类作用为用户可根据该类对象创建指定的Shape子类对象（Circle or Rectangle）
优点：客户端不需要修改代码。
缺点： 当需要增加新的运算类的时候，不仅需新加运算类，还要修改工厂类，违反了开闭原则。
'''

fac = ShapeFactory() #实例化工厂类
obj = fac.create('Circle') #实例化Shape的Circle子类
obj.draw()
