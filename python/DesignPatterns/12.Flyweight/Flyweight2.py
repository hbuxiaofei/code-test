"""Flyweight Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


# 抽象享元类
class Flyweight(metaclass=ABCMeta):
    @abstractmethod 
    def operation(self):
        pass


# 具体享元类，实现了Flyweight
class ConcreteFlyweight(Flyweight):
    def __init__(self, name):
        self.name = name

    def operation(self):
        print("Name: %s" % self.name)


# 享元创建工厂类
class FlyweightFactory():
    _dict = {}

    def getFlyweight(self, name):
        if name not in self._dict:
            self._dict[name] = ConcreteFlyweight(name)
        return self._dict[name]
    
    def getFlyweightCount(self):
        return len(self._dict)


class Client(object):
    def main(self):
        factory = FlyweightFactory()

        c1_capp = factory.getFlyweight("cappuccino")
        c1_capp.operation()

        c2_mocha = factory.getFlyweight("mocha")
        c2_mocha.operation()
        
        c3_capp = factory.getFlyweight("cappuccino")
        c3_capp.operation()

        print("Num of Flyweight Instance: %s" % factory.getFlyweightCount())


if __name__=="__main__":
    Client().main()