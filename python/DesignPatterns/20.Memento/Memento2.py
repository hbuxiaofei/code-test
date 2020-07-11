"""Memento Pattern with Python Code
"""

class Memento(object):
    def __init__(self, state):
        self.state = state
    
    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state


class Originator(object):
    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state
    
    def createMemento(self):
        return Memento(self.state)
    
    def restoreMemento(self, memento:Memento):
        self.setState(memento.getState())
    

class Caretaker(object):
    def getMemento(self):
        return self.memento
    
    def setMemento(self, memento:Memento):
        self.memento = memento
    

class Client(object):
    def main(self):
        originator = Originator()
        originator.setState("状态1");
        print("初始状态:" + originator.getState())
        caretaker = Caretaker()
        caretaker.setMemento(originator.createMemento())
        originator.setState("状态2")
        print("改变后状态:" + originator.getState())
        originator.restoreMemento(caretaker.getMemento())
        print("恢复后状态:" + originator.getState())


if __name__ == "__main__":
    Client().main()   