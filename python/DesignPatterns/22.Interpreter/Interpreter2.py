"""Interpreter Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


# 抽象一个解释器类
class AbstractExpression(metaclass=ABCMeta):
    @abstractmethod
    def interpreter(self, context):
        pass


# 具体解释器——终端 继承抽象解释器
class TerminalExpression(AbstractExpression):
    def interpreter(self, context):
        print("终端解释器", context)


# 具体解释器——非终端 继承抽象解释器
class NotTerminalExpression(AbstractExpression):
    def interpreter(self, context):
        print("非终端解释器", context)


class Context(object):
    def __init__(self):
        self.name = ""


class Client(object):
    def main(self):
        context = Context()
        context.name = 'Andy'
        arr_list = [NotTerminalExpression(),TerminalExpression(),TerminalExpression()]
        for entry in arr_list:
            entry.interpreter(context)


if __name__ == "__main__":
    Client().main()