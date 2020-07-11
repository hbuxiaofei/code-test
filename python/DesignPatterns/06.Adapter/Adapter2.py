'''Adapter Pattern with Python Code
'''

class Target(object):
    def request(self):
        print("general request")


class Adaptee(object):
    def specific_request(self):
        print("specific request")


class Adapter(Target):
    def __init__(self):
        self.adaptee = Adaptee()

    def request(self):
        self.adaptee.specific_request()

class Client(object):
    def main(self):
        target = Adapter()
        target.request()


if __name__ == "__main__":
    Client().main()