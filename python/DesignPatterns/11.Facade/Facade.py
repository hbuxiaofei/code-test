#!/usr/bin/env python3
# -*- coding: utf-8 -*-



'''外观模式（Facade）

意图：
为子系统中的一组接口提供一个一致的界面，Facade模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。

适用性：
当你要为一个复杂子系统提供一个简单接口时。子系统往往因为不断演化而变得越来越复杂。大多数模式使用时都会产生更多更小的类。这使得子系统更具可重用性，也更容易对子系统进行定制，但这也给那些不需要定制子系统的用户带来一些使用上的困难。Facade 可以提供一个简单的缺省视图，这一视图对大多数用户来说已经足够，而那些需要更多的可定制性的用户可以越过facade层。
客户程序与抽象类的实现部分之间存在着很大的依赖性。引入facade 将这个子系统与客户以及其他的子系统分离，可以提高子系统的独立性和可移植性。
当你需要构建一个层次结构的子系统时，使用facade模式定义子系统中每层的入口点。如果子系统之间是相互依赖的，你可以让它们仅通过facade进行通讯，从而简化了它们之间的依赖关系。

'''

#外观模式（Facade），为子系统中的一组接口提供一个一致的界面，定义一个高层接口，这个接口使得这一子系统更加容易使用。
# 在以下情况下可以考虑使用外观模式：
# (1) 设计初期阶段，应该有意识的将不同层分离，层与层之间建立外观模式。
# (2) 开发阶段，子系统越来越复杂，增加外观模式提供一个简单的调用接口。
# (3) 维护一个大型遗留系统的时候，可能这个系统已经非常难以维护和扩展，但又包含非常重要的功能，为其开发一个外观类，以便新系统与其交互。

# 优点编辑
# （1）实现了子系统与客户端之间的松耦合关系。
# （2）客户端屏蔽了子系统组件，减少了客户端所需处理的对象数目，并使得子系统使用起来更加容易。



def printInfo(info):
    print(info)

class Stock():
    name = '股票'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class ETF():
    name = '指数型基金'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class Future():
    name = '期货'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class NationDebt():
    name = '国债'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class Option():
    name = '权证'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

#基金
class Fund():

    def __init__(self):
        self.stock = Stock()
        self.etf = ETF()
        self.future = Future()
        self.debt = NationDebt()
        self.option = Option()

    def buyFund(self):
        self.stock.buy()
        self.etf.buy()
        self.debt.buy()
        self.future.buy()
        self.option.buy()

    def sellFund(self):
        self.stock.sell()
        self.etf.sell()
        self.future.sell()
        self.debt.sell()
        self.option.sell()

def clientUI():
    myFund = Fund()
    myFund.buyFund()
    myFund.sellFund()
    return


'''
从执行结果可以看出：一个类被实例化成对象，该对象的初始化进行了实例化所有其他的类对象，通过调用该类的方法执行所有其他类对象的相同方法
'''
if __name__ == '__main__':
    clientUI()
