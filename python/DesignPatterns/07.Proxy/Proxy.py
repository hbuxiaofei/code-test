#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''代理模式（Proxy）

意图：为其他对象提供一种代理以控制对这个对象的访问。

主要解决：在直接访问对象时带来的问题，比如说：要访问的对象在远程的机器上。在面向
对象系统中，有些对象由于某些原因（比如对象创建开销很大，或者某些操作需要安全控制
，或者需要进程外的访问），直接访问会给使用者或者系统结构带来很多麻烦，我们可以在
访问此对象时加上一个对此对象的访问层。

何时使用：想在访问一个类时做一些控制。

如何解决：增加中间层。

关键代码：实现与被代理类组合。

优点： 1、职责清晰。 2、高扩展性。 3、智能化。

缺点： 1、由于在客户端和真实主题之间增加了代理对象，因此有些类型的代理模式可能会
造成请求的处理速度变慢。 2、实现代理模式需要额外的工作，有些代理模式的实现非常复
杂。

使用场景：按职责来划分，通常有以下使用场景： 1、远程代理。 2、虚拟代理。
3、Copy-on-Write 代理。 4、保护（Protect or Access）代理。 5、Cache代理。
6、防火墙（Firewall）代理。 7、同步化（Synchronization）代理。
8、智能引用（Smart Reference）代理。

'''

# 代理模式
# 应用特性：需要在通信双方中间需要一些特殊的中间操作时引用，多加一个中间控制层。
# 结构特性：建立一个中间类，创建一个对象，接收一个对象，然后把两者联通起来

class sender_base:
    def __init__(self):
        pass

    def send_something(self, something):
        pass


class send_class(sender_base):
    def __init__(self, receiver):
        self.receiver = receiver

    def send_something(self, something):
        print("SEND " + something + ' TO ' + self.receiver.name)


class agent_class(sender_base):
    def __init__(self, receiver):
        self.send_obj = send_class(receiver)

    def send_something(self, something):
        self.send_obj.send_something(something)


class receive_class:
    def __init__(self, someone):
        self.name = someone


'''
sender_base（父类or基类）
send_class（sender_base的子类or派生类）：作用为发送信息
agent_class（sender_base的子类or派生类）：作用为代理（发送信息给接受者）
receive_class（新式类）：作用为实例化一个接受者
'''
if '__main__' == __name__:
    receiver = receive_class('Burgess')
    agent = agent_class(receiver)
    agent.send_something('agentinfo')

    print(receiver.__class__)
    print(agent.__class__)

