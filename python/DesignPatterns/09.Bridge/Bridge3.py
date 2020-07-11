'''Bridge Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


class AbstractRoad(metaclass=ABCMeta):
    car = None


class AbstractCar(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Street(AbstractRoad):
    '''市区街道'''
    def run(self):
        self.car.run()
        print("在市区街道上行驶")


class SpeedWay(AbstractRoad):
    '''高速公路'''
    def run(self):
        self.car.run()
        print("在高速公路上行驶")


class Car(AbstractCar):
    '''小汽车'''
    def run(self):
        print("小汽车在")


class Bus(AbstractCar):
    '''公共汽车'''
    def run(self):
        print("公共汽车在")


class Client(object):
    def main(self):
        # 小汽车在高速上行驶
        road1 = SpeedWay()
        road1.car = Car()
        road1.run()

        # 公交车在高速上行驶
        road2 = SpeedWay()
        road2.car = Bus()
        road2.run()

        # 小汽车在市区街道行驶
        road3 = Street()
        road3.car = Bus()
        road3.run()


if __name__ == "__main__":
    Client().main()