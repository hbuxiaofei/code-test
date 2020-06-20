#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''AbstractFactory Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


class IProduct1(metaclass=ABCMeta):
    @abstractmethod
    def show(self):
        pass


class IProduct2(metaclass=ABCMeta):
    @abstractmethod
    def show(self):
        pass


class Product1(IProduct1):
    def show(self):
        print("This is 1 mode product")


class Product2(IProduct2):
    def show(self):
        print("This is 2 mode product")


class IFactory(metaclass=ABCMeta):
    @abstractmethod
    def createProduct1():
        pass

    @abstractmethod
    def createProduct2():
        pass


class Factory(IFactory):
    def createProduct1(self):
        return Product1()

    def createProduct2(self):
        return Product2()


class Client(object):
    def main(self):
        factory = Factory()
        factory.createProduct1().show()
        factory.createProduct2().show()


if __name__ == "__main__":
    Client().main()
