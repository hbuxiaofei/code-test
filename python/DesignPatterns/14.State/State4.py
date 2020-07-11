"""State Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


# 抽象的状态类
class LiftState(metaclass=ABCMeta):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def run(self):
        pass   
 
    @abstractmethod
    def stop(self):
        pass


class OpenState(LiftState):
    def open(self):
        print("OPEN:The door is opened...")
        return self

    def close(self):
        print("OPEN:The door start to close...")
        print("OPEN:The door is closed")
        return StopState()

    def run(self):
        print("OPEN:Run Forbidden.")
        return self
    
    def stop(self):
        print("OPEN:Stop Forbidden.")
        return self


class RunState(LiftState):
    def open(self):
        print("RUN:Open Forbidden.")
        return self

    def close(self):
        print("RUN:Close Forbidden.")
        return self

    def run(self):
        print("RUN:The lift is running...")
        return self

    def stop(self):
        print("RUN:The lift start to stop...")
        print("RUN:The lift stopped...")
        return StopState()


class StopState(LiftState):
    def open(self):
        print("STOP:The door is opening...")
        print("STOP:The door is opened...")
        return OpenState()

    def close(self):
        print("STOP:Close Forbidden")
        return self
    
    def run(self):
        print("STOP:The lift start to run...")
        return RunState()

    def stop(self):
        print("STOP:The lift is stopped.")
        return self


class Context(LiftState):
    def getState(self):
        return self._state

    def setState(self, state):
        self._state = state
    
    def open(self):
        self.setState(self._state.open())
    
    def close(self):
        self.setState(self._state.close())
    
    def run(self):
        self.setState(self._state.run())

    def stop(self):
        self.setState(self._state.stop())
    

# 电梯先在STOP状态，然后开门，开门时运行Run，被禁止，然后，关门、运行、停止。
class Client(object):
    def main(self):
        ctx = Context()
        ctx.setState(StopState())
        ctx.open()
        ctx.run()
        ctx.close()
        ctx.run()
        ctx.stop() 


if __name__ == "__main__":
    Client().main()