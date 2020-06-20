#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


# 接口类:接口类就是一个规范,接口类一般是项目设计人员写好的
class PaymentInterface(metaclass=ABCMeta):   # 规范
    @abstractmethod
    def pay(self, money):
        raise NotImplementedError


# 微信支付
class WeChatPay(PaymentInterface):
    def pay(self, money):
        print("Pay for %s dollars with WeChat" % money)


# 支付宝支付
class AliPay(PaymentInterface):
    def pay(self, money):
        print("Pay for %s dollars with AliPay" % money)


# apple pay
class ApplePay(PaymentInterface):
    def pay(self, money):
        print("Pay for %s dollars with ApplePay" % money)


class Payment(object):
    def pay(self, method: PaymentInterface, money: int) -> int:
        method.pay(money)
        return money


class Client(object):
    def main(self):
        wp = WeChatPay()
        alp = AliPay()
        app = ApplePay()

        payment = Payment()
        payment.pay(wp, 100)
        payment.pay(alp, 100)
        payment.pay(app, 100)


if __name__ == "__main__":
    Client().main()
