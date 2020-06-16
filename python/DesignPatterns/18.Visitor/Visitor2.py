#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

'''访问者模式Visitor

Visitor模式是在补修改已有程序结构前提下，通过添加额外的访问者完成对代码功能的拓
展。为什么这样用？当你的类层次较多，在某层结构中增加新的方法，要是在基类上面添加
或者变更，可能破坏原来的设计，有兼容问题，所以只在需要的类上面动态添加。

这里是个构建车的例子，每个部件都有一个accept的方法接受我上面说的所谓'访问者'，而
这个访问者以参数的方式传进来，但是其实他是一个含有一些功能的类的实例，它拥有很多
个visit开头的方法对应不同的部件。这样就不需要修改这些部件，而只是修改我们的访问
者类的相关部分。
'''

# 抽象元素
class Element(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


# 轮子,引擎, 车身这些定义好了都不需要变动
class Wheel(Element):
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        # 每个visitor是同样的，但是其中的方法是不一样的，比如这里是visitWheel，
        # 然后传入了self，想想？他其实想做什么就能做什么
        visitor.visitWheel(self)

class Engine(Element):
    def accept(self, visitor):
        visitor.visitEngine(self)

class Body(Element):
    def accept(self, visitor):
        visitor.visitBody(self)


# 我们要组合成车
class Car(Element):
    def __init__(self):
        self.engine = Engine()
        self.body   = Body()
        self.wheels = [Wheel("front left"), Wheel("front right"),
                       Wheel("back left") , Wheel("back right")]

    # 这个也不需要在动，他只是上面部件的组合，只是做了属性的委托
    def accept(self, visitor):
        visitor.visitCar(self)
        self.body.accept(visitor)
        self.engine.accept(visitor)
        for wheel in self.wheels:
            wheel.accept(visitor)


# 这个才是我们的访问者，每次的修改都在这里面
class Visitor(object):

    def visitCar(self, car):
        print("Visiting car")

    def visitBody(self, body):
        print("Visiting body")

    def visitEngine(self, engine):
        print("Visiting engine")

    def visitWheel(self, wheel):
        print("Visiting " + "wheel " + wheel.name)



if __name__ == '__main__':
    car = Car()
    visitor = Visitor()
    car.accept(visitor)
