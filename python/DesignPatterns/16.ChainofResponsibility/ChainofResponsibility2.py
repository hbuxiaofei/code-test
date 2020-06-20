#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Chain of Responsibility Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


class Level(object):
    num = 0

    def __init__(self, num):
        self.num = num

    def above(self, level):
        if(self.num >= level.num):
            return True
        return False


class Request(object):
    level = None

    def __init__(self, level):
        self.level = level

    def getLevel(self):
        return self.level


class Response(object):
    pass


class Handler(metaclass=ABCMeta):
    nextHandler = None

    def handleRequest(self, request):
        response = None

        if self.getHandlerLevel().above(request.getLevel()):
            response = self.response(request);
        else:
            if self.nextHandler != None:
                response = self.nextHandler.handleRequest(request)
            else:
                print("deny access")

        return response

    def setNextHandler(self, handler):
        self.nextHandler = handler

    @abstractmethod
    def getHandlerLevel(self):
        pass

    @abstractmethod
    def response(self, request):
        pass


class ConcreteHandler1(Handler):
    def getHandlerLevel(self):
        return Level(10)

    def response(self, request):
        print("Level 1 access")
        return Response()


class ConcreteHandler2(Handler):
    def getHandlerLevel(self):
        return Level(100)

    def response(self, request):
        print("Level 2 access")
        return Response()


class ConcreteHandler3(Handler):
    def getHandlerLevel(self):
        return Level(1000)

    def response(self, request):
        print("Level 3 access")
        return Response()


class Client(object):
    def main(self):
        handler1 = ConcreteHandler1()
        handler2 = ConcreteHandler2()
        handler3 = ConcreteHandler3()

        handler1.setNextHandler(handler2)
        handler2.setNextHandler(handler3)

        response = handler1.handleRequest(Request(Level(500)))


if __name__ == "__main__":
    Client().main()
