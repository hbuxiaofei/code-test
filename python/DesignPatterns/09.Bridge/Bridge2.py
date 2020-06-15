#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
桥接模式（Bridge）来做(多维度变化);
结合上面的例子,增加一个维度"人",不同的人开着不同的汽车在不同的路上行驶(三个维度);
结合上面增加一个类"人",并重新调用.
'''


'''
应用设计模式（Bridge多维度）
'''
class AbstractRoad(object):
    '''公路基类'''
    car = None

class AbstractCar(object):
    '''车辆基类'''

    def run(self):
        pass

class People(object):
    pass


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
    road = None

    def run(self):
        print("公共汽车在")



#加上人
class Man(People):
    def drive(self):
        print("男人开着")
        self.road.run()
#加上人
class Woman(People):
    def drive(self):
        print("女人开着")
        self.road.run()

'''
AbstractRoad（父类or基类）
Street（AbstractRoad的子类or派生类）：作用为执行了车辆对象的方法
SpeedWay（AbstractRoad的子类or派生类）：作用为执行了车辆对象的方法

AbstractCar（父类or基类）
Car（AbstractCar的子类or派生类）：作用为被调用执行
Bus（AbstractCar的子类or派生类）：作为为被调用执行

People（父类or基类）
Man（People的子类or派生类）：作用为执行了路对象的方法
Woman（People的子类or派生类）：作用为执行了路对象的方法
'''
if __name__ == "__main__":
    #小汽车在高速上行驶
    road1 = SpeedWay()
    road1.car = Car()
    road1.run()

    #
    road2 = SpeedWay()
    road2.car = Bus()
    road2.run()

    #人开车
    road3 = Street()
    road3.car = Car()

    p1 = Man()
    p1.road = road3
    p1.drive()

    p2 = Woman()
    p2.road = road3
    p2.drive()
