#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
             ___________________________
            |                           |
            |          Unicode          |
            |                           |
             ---------------------------
               |   /|\           |   /|\
               |    |            |    |
               |    |            |    |
            encode decode     encode decode
               |    |            |    |
               |    |            |    |
              \|/   |           \|/   |
             _________         _________
            |         |       |         |
            |  utf-8  |       |   gbk   |
            |         |       |         |
             ---------         ---------



            GBK 需要转换成 UTF-8 格式流程
        1. 首先通过编码[encode]转换为Unicode编码
        2. 然后通过解码[decode]转换为UTF-8编码

            UTF-8 需要转换成 GBK 格式流程
        1. 首先通过编码[encode]转换为Unicode编码
        2. 然后通过解码[decode]转换为UBK编码
'''


utf_8_01= '爱'  #utf-8字符集
unicode_01 = utf_8_01.encode('gbk')   #编码成gbk的unicode二进制
print(unicode_01)
gbk = unicode_01.decode('gbk')        #解码成gbk字符集
print(gbk)
unicode_02 = gbk.encode('utf-8')      #编码成utf-8的unicode二进制
print(unicode_02)
uff_8_02 = unicode_02.decode('utf-8') #解码成utf-8字符集
print(uff_8_02)


