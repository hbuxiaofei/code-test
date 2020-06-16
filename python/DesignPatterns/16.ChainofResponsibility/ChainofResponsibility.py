#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 职责链模式（Chain of Responsibility）：使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。将这些对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。
# 适用场景：
# 1、有多个的对象可以处理一个请求，哪个对象处理该请求运行时刻自动确定；
# 2、在不明确指定接收者的情况下，向多个对象中的一个提交一个请求；
# 3、处理一个请求的对象集合应被动态指定。

class BaseHandler(object):
    '''处理基类'''
    def successor(self,successor): #next_handler
        #与下一个责任者关联
        self._successor = successor

class RequestHandlerL1(BaseHandler):
    '''第一级请求处理者'''
    name = "TeamLeader"
    def handle(self,request):
        if request < 500 :
            print("审批者[%s],请求金额[%s],审批结果[审批通过]"%(self.name,request))
        else:
            print("\033[31;1m[%s]无权审批,交给下一个审批者\033[0m" %self.name)
            self._successor.handle(request)

class RequestHandlerL2(BaseHandler):
    '''第二级请求处理者'''
    name = "DeptManager"
    def handle(self,request):
        if request < 5000 :
            print("审批者[%s],请求金额[%s],审批结果[审批通过]"%(self.name,request))
        else:
            print("\033[31;1m[%s]无权审批,交给下一个审批者\033[0m" %self.name)
            self._successor.handle(request)

class RequestHandlerL3(BaseHandler):
    '''第三级请求处理者'''
    name = "CEO"
    def handle(self,request):
        if request < 10000 :
            print("审批者[%s],请求金额[%s],审批结果[审批通过]"%(self.name,request))
        else:
            print("\033[31;1m[%s]要太多钱了,不批\033[0m"%self.name)
            #self._successor.handle(request)

class RequestAPI(object):
    h1 = RequestHandlerL1()
    h2 = RequestHandlerL2()
    h3 = RequestHandlerL3()

    h1.successor(h2)
    h2.successor(h3)

    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

    def handle(self):
        '''统一请求接口'''
        self.h1.handle(self.amount)

'''
#如OA系统 不同等级领导批示资金大小权限不同（根据资金大小自动流转到责任人）
简单解释：
1.接口类对象内把最高层级处理者领对象赋值到比其低一层级处理者对象（层级高的对象作为形参实例化层级低对象）以此类推
2.实例化接口类，把申请人和申请资金传递进去，执行该接口类对象处理方法
3.该处理方法执行最低层级领导的处理方法（进行判断该资金是否自己有权限处理，没权限处理就调用比其高一层级的处理对象进行处理，以此类推）
'''
if __name__ == "__main__":
    r1 = RequestAPI("Burgess", 8000)
    r1.handle()
    print(r1.__dict__)



