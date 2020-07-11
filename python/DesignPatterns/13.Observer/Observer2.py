"""Observer Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


class Observer(metaclass=ABCMeta):
    @abstractmethod 
    def update(self):
        pass


class Subject(metaclass=ABCMeta):
    obs = []

    def addObserver(self, obs:Observer):
        self.obs.append(obs);
    
    def delObserver(self, obs:Observer):
        self.obs.remove(obs)

    def notifyObserver(self):
        for o in self.obs:
            o.update()

    @abstractmethod
    def doSomething(self):
        pass


class ConcreteSubject(Subject):
    def doSomething(self):
        print("被观察者事件反生")
        self.notifyObserver()
    

class ConcreteObserver1(Observer):
    def update(self):
        print("观察者1收到信息，并进行处理")
    

class ConcreteObserver2(Observer):
    def update(self):
        print("观察者2收到信息，并进行处理")


class Client(object):
    def main(self):
        sub = ConcreteSubject()
        sub.addObserver(ConcreteObserver1()) # 添加观察者1
        sub.addObserver(ConcreteObserver2()) # 添加观察者2
        sub.doSomething()


if __name__ == "__main__":
    Client().main()    