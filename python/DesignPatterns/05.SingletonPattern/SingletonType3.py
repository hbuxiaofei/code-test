'''Singleton Pattern with Python Code
'''

import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            # 线程安全
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance



class Client(object):
    def main(self):
        obj = Singleton.getInstance()
        print(obj)

        obj = Singleton.getInstance()
        print(obj)

if __name__ == '__main__':
    Client().main()