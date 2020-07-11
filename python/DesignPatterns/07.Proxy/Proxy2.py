"""Proxy Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


class Subject(metaclass=ABCMeta):
    @abstractmethod 
    def Request(self):
        pass


class RealSubject(Subject):
    def Request(self):
        print("Receive a request")


class Proxy(Subject):
    def __init__(self):
        self.subject = None

    def Request(self):
        self.subject = RealSubject()
        self.subject.Request()


class Client(object):
    def main(self):
        p = Proxy()
        p.Request()


if __name__ == '__main__':
    Client().main()
      