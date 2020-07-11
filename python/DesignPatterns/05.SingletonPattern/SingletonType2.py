'''Singleton Pattern with Python Code
'''

import threading

'''
基于metaclass方式实现
1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
'''
class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance


 # 指定创建SingletonClass的type为SingletonType
class SingletonClass(metaclass=SingletonType):
    def __init__(self,name):
        self.name = name


class Client(object):
    def main(self):
        # 执行type的 __call__ 方法，调用 SingletonClass类（是type的对象）的 __new__方法，用于创建对象，
        # 然后调用 SingletonClass类（是type的对象）的 __init__方法，用于对对象初始化。
        obj1 = SingletonClass("obj-1")
        obj2 = SingletonClass("obj-2")

        print(obj1)
        print(obj2)

        print(obj1.name, obj2.name)


if __name__ == '__main__':
    Client().main()