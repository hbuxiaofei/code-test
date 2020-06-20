#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''Factory Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


# 工厂接口。工厂接口是工厂方法模式的核心，与调用者直接交互用来提供产品
class IProduct(metaclass=ABCMeta):
    @abstractmethod
    def productMethod(self):
        pass


# 工厂实现。在编程中，工厂实现决定如何实例化产品，是实现扩展的途径
class Product(IProduct):
    def productMethod(self):
        print("create product")


# 产品接口。产品接口的主要目的是定义产品的规范
class IFactory(metaclass=ABCMeta):
    @abstractmethod
    def createProduct(self):
        pass


# 产品实现。实现产品接口的具体类，决定了产品在客户端中的具体行为
class Factory(IFactory):
    def createProduct(self):
        return Product()


class Client(object):
    def main(self):
        factory = Factory()
        product = factory.createProduct()
        product.productMethod()


if __name__ == "__main__":
    Client().main()
