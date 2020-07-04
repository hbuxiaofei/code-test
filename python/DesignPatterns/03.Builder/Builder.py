#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''创建者模式（Builder）

意图：
将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。

适用性：
当创建复杂对象的算法应该独立于该对象的组成部分以及它们的装配方式时。

当构造过程必须允许被构造的对象有不同的表示时。

'''


#建造者模式
#相关模式：思路和模板方法模式很像，模板方法是封装算法流程，对某些细节，提供接口由子类修改，建造者模式更为高层一点，将所有细节都交由子类实现。
# 建造者模式：将一个复杂对象的构建与他的表示分离，使得同样的构建过程可以创建不同的表示。
# 基本思想
# 某类产品的构建由很多复杂组件组成；
# 这些组件中的某些细节不同，构建出的产品表象会略有不同；
# 通过一个指挥者按照产品的创建步骤来一步步执行产品的创建；
# 当需要创建不同的产品时，只需要派生一个具体的建造者，重写相应的组件构建方法即可。

def printInfo(info):
    print(info)

#建造者基类
class PersonBuilder():
    def BuildHead(self):

        pass

    def BuildBody(self):
        pass

    def BuildArm(self):
        pass

    def BuildLeg(self):
        pass

#胖子
class PersonFatBuilder(PersonBuilder):
    type = '胖子'
    def BuildHead(self):
        printInfo("构建%s的大。。。。。头" % self.type)

    def BuildBody(self):
        printInfo("构建%s的身体" % self.type)

    def BuildArm(self):
        printInfo("构建%s的手" % self.type)

    def BuildLeg(self):
        printInfo("构建%s的脚" % self.type)


#瘦子
class PersonThinBuilder(PersonBuilder):
    type = '瘦子'
    def BuildHead(self):
        printInfo("构建%s的头" % self.type)

    def BuildBody(self):
        printInfo("构建%s的身体" % self.type)

    def BuildArm(self):
        printInfo("构建%s的手" % self.type)

    def BuildLeg(self):
        printInfo("构建%s的脚" % self.type)

#指挥者
class PersonDirector():
    pb = None;
    def __init__(self, pb):
        self.pb = pb

    def CreatePereson(self):
        self.pb.BuildHead()
        self.pb.BuildBody()
        self.pb.BuildArm()
        self.pb.BuildLeg()

def clientUI():
    pb = PersonThinBuilder()
    pd = PersonDirector(pb)
    pd.CreatePereson()

    pb2 = PersonFatBuilder()
    #pd = PersonDirector(pb)
    pd.pb = pb2
    pd.CreatePereson()
    return



'''
personBuilder（父类 or 基类）
PersonFatBuilder(personBuilder的子类 or派生类）：作用为创建一个胖子的身体部位
PersonThinBuilder(personBuilder的子类 or派生类）：作用为创建一个瘦子的身体部位
PersonDirector（新式类）：作用为根据personBuilder子类对象（如PersonFatBuilder()）让其创建其身体部位
'''
if __name__ == '__main__':
    clientUI();