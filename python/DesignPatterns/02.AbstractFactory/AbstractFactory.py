#!/usr/bin/env python3
# -*- coding: utf-8 -*-



'''抽象工厂模式（Abstract Factory）

　　抽象工厂模式是对象的创建模式，它是工厂方法模式的进一步推广。

　　假设一个子系统需要一些产品对象，而这些产品又属于一个以上的产品等级结构。那
么为了将消费这些产品对象的责任和创建这些产品对象的责任分割开来，可以引进抽象工厂模式。
这样的话，消费产品的一方不需要直接参与产品的创建工作，而只需要向一个公用的工厂接口请求所需要的产品。

　　通过使用抽象工厂模式，可以处理具有相同（或者相似）等级结构中的多个产品族中的产品对象的创建问题。


在什么情况下应当使用抽象工厂模式:

　　1.一个系统不应当依赖于产品类实例如何被创建、组合和表达的细节，这对于所有形态的工厂模式都是重要的。

　　2.这个系统的产品有多于一个的产品族，而系统只消费其中某一族的产品。

　　3.同属于同一个产品族的产品是在一起使用的，这一约束必须在系统的设计中体现出来。（比如：Intel主板必须使用Intel CPU、Intel芯片组）

　　4.系统提供一个产品类的库，所有的产品以同样的接口出现，从而使客户端不依赖于实现。


抽象工厂模式的起源:

　　抽象工厂模式的起源或者最早的应用，是用于创建分属于不同操作系统的视窗构建。
比如：命令按键（Button）与文字框（Text)都是视窗构建，在UNIX操作系统的视窗环境和Windows操作系统的视窗环境中，
这两个构建有不同的本地实现，它们的细节有所不同。

　　在每一个操作系统中，都有一个视窗构建组成的构建家族。在这里就是Button和Text组成的产品族。而每一个视窗构件都构成自己的等级结构，
由一个抽象角色给出抽象的功能描述，而由具体子类给出不同操作系统下的具体实现。


抽象工厂模式的优点:

- 分离接口和实现
　　客户端使用抽象工厂来创建需要的对象，而客户端根本就不知道具体的实现是谁，客户端只是面向产品的接口编程而已。也就是说，客户端从具体的产品实现中解耦。

- 使切换产品族变得容易
　　因为一个具体的工厂实现代表的是一个产品族，比如上面例子的从Intel系列到AMD系列只需要切换一下具体工厂。

抽象工厂模式的缺点:

- 不太容易扩展新的产品
    如果需要给整个产品族添加一个新的产品，那么就需要修改抽象工厂，这样就会导致修改所有的工厂实现类。

'''

class AbstractFactory(object):
    computer_name = ''
    def createCpu(self):
        pass
    def createMainboard(self):
        pass

class IntelFactory(AbstractFactory):
    computer_name = 'Intel I7-series computer '
    def createCpu(self):
        return IntelCpu('I7-6500')

    def createMainboard(self):
        return IntelMainBoard('Intel-6000')

class AmdFactory(AbstractFactory):
    computer_name = 'Amd 4 computer '

    def createCpu(self):
        return AmdCpu('amd444')

    def createMainboard(self):
        return AmdMainBoard('AMD-4000')

class AbstractCpu(object):
    series_name = ''
    instructions = ''
    arch=''

class IntelCpu(AbstractCpu):
    def __init__(self,series):
        self.series_name = series

class AmdCpu(AbstractCpu):
    def __init__(self,series):
        self.series_name = series

class AbstractMainboard(object):
    series_name = ''

class IntelMainBoard(AbstractMainboard):
    def __init__(self,series):
        self.series_name = series

class AmdMainBoard(AbstractMainboard):
    def __init__(self,series):
        self.series_name = series

class ComputerEngineer(object):

    def makeComputer(self,factory_obj):

        self.prepareHardwares(factory_obj)

    def prepareHardwares(self,factory_obj):
        self.cpu = factory_obj.createCpu()
        self.mainboard = factory_obj.createMainboard()

        info = '''------- computer [%s] info:
    cpu: %s
    mainboard: %s
-------- End --------
        '''% (factory_obj.computer_name,self.cpu.series_name,self.mainboard.series_name)
        print(info)


'''
AbstractFactory（父类or基类 ）
    IntelFactory（AbstractFactory的子类or派生类）：作用为进行了创建自定品牌的零件
    AmdFactory（AbstractFactory的子类or派生类）：作用为进行了创建自定品牌的零件
AbstractCpu（父类or基类 ）
    IntelCpu（AbstractCpu的子类or派生类）：作用为记录cup的型号
    AmdCpu（AbstractCpu的子类or派生类）：作用为记录cup的型号
AbstractMainboard（父类or基类 ）
    IntelMainBoard（AbstractMainboard的子类or派生类）：作用为记录主板的型号
    AmdMainBoard（AbstractMainboard的子类or派生类）：作用为记录主板的型号
ComputerEngineer（新式类）：作用为根据工厂对象（如IntelFactory()）让其组装自身型号的零件

抽象工厂和工厂模式的对比区别：
抽象工厂：规定死了，依赖限制，假上面实验，你用intel的机器只能配置intel的CPU不能配置AMD的CPU（由各自的工厂指定自己的产品生产品牌）
工厂模式：不是固定死的，举例：你可使用intel的机器配置AMD的CPU
'''
if __name__ == "__main__":
    engineer = ComputerEngineer()   #装机工程师

    intel_factory = IntelFactory()    #intel工厂
    engineer.makeComputer(intel_factory)

    amd_factory = AmdFactory()      #adm工厂
    engineer.makeComputer(amd_factory)

