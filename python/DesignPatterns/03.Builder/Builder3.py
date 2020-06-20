#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''Builder Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


# 产品类：一般是一个较为复杂的对象，也就是说创建对象的过程比较复杂
class Product(object):
    name = None
    mode = None

    def showProduct(self):
        print("名称：" + self.name)
        print("型号：" + self.mode)

    def setName(self, name):
        self.name = name

    def setMode(self, mode):
        self.mode = mode


# 抽象建造者：引入抽象建造者的目的，是为了将建造的具体过程交与它的子类来实现
class Builder(metaclass=ABCMeta):
    @abstractmethod
    def setPart(self, arg1, arg2):
        pass

    @abstractmethod
    def getProduct(self):
        pass


# 建造者：实现抽象类的所有未实现的方法
class ConcreteBuilder(Builder):
    product = Product()

    def getProduct(self):
        return self.product

    def setPart(self, arg1, arg2):
        self.product.setName(arg1)
        self.product.setMode(arg2)


# 导演类：负责调用适当的建造者来组建产品
class Director(object):
    builder = ConcreteBuilder()

    def getAProduct(self):
        self.builder.setPart("宝马汽车", "X7")
        return self.builder.getProduct()

    def getBProduct(self):
        self.builder.setPart("奥迪汽车", "Q5")
        return self.builder.getProduct()


class Client(object):
    def main(self):
        director = Director()
        product1 = director.getAProduct()
        product1.showProduct()

        product2 = director.getBProduct()
        product2.showProduct()


if __name__ == "__main__":
    Client().main()
