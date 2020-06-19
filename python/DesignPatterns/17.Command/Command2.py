#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Command Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


# Command抽象类，类中对需要执行的命令进行声明，一般来说要对外公布一个execute方法用来执行命令
class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


# 接收者，负责接收命令并且执行命令
class Receiver(object):
    def do_enter(self):
        print("Receive a command")


# 调用者，负责调用命令
class Invoker(object):
    def set_command(self, command):
        self._command = command

    def action(self):
        self._command.execute()


# Command类的实现类
class ConcreteCommand(Command):
    def __init__(self, receiver):
        self._receiver = receiver

    def execute(self):
        self._receiver.do_enter()


# 最终的客户端调用类
class Client(object):
    def main(self, args=None):
        receiver = Receiver()
        command = ConcreteCommand(receiver)

        # 客户端直接执行具体命令方式
        command.execute()

        # 客户端通过调用者来执行命令
        invoker = Invoker()
        invoker.set_command(command)
        invoker.action()


if __name__ == "__main__":
    Client().main()
