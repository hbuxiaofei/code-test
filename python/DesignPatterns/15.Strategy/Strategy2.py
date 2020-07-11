"""Strategy Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


class IStrategy(metaclass=ABCMeta):
    @abstractmethod
    def doSomething(self):
        pass


class ConcreteStrategy1(IStrategy):
    def doSomething(self):
        print("具体策略1")
    

class ConcreteStrategy2(IStrategy):
    def doSomething(self):
        print("具体策略2")
    

class Context(object):
    def __init__(self, strategy:IStrategy):
        self.strategy = strategy
    
    def execute(self):
        self.strategy.doSomething()


class Client(object):
    def main(self):
        print("-----执行策略1-----")
        context = Context(ConcreteStrategy1())
        context.execute()

        print("-----执行策略2-----")
        context = Context(ConcreteStrategy2())
        context.execute()


if __name__ == "__main__":
    Client().main()