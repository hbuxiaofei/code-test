#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------变量声明-----------------------------------------------
side = 0                   # 轮到哪方走，0表示红方，1表示黑方
board = [0]*256            # 棋盘数组
FenString = ""             # 局面的FEN串格式


# ----------------------------------------------------------------------
def IntToChar(a):
    """  棋子整数值转换成字符表示 """
    if (a < 32):
        if a == 16:
            return 'K'
        elif a == 17 or a == 18:
            return 'A'
        elif a == 19 or a == 20:
            return 'B'
        elif a == 21 or a == 22:
            return 'N'
        elif a == 23 or a == 24:
            return 'R'
        elif a == 25 or a == 26:
            return 'C'
        elif a == 27 or a == 28 or a == 29 or a == 30 or a == 31:
            return 'P'
        else:
            return 0
    else:
        a = a - 16
        if a == 16:
            return 'k'
        elif a == 17 or a == 18:
            return 'a'
        elif a == 19 or a == 20:
            return 'b'
        elif a == 21 or a == 22:
            return 'n'
        elif a == 23 or a == 24:
            return 'r'
        elif a == 25 or a == 26:
            return 'c'
        elif a == 27 or a == 28 or a == 29 or a == 30 or a == 31:
            return 'p'
        else:
            return 0


def ClearBoard():
    """ 清空棋盘数组board """
    for i in range(len(board)):
        board[i] = 0


def CharToSubscript(ch):
    """
    FEN串中棋子对应的数组下标
    下标0，1，2，3，4，5，6分别对应表示将，仕，象，马，车，炮，兵
    """
    if ch == 'k' or ch == 'K':
        return 0
    elif ch == 'a' or ch == 'A':
        return 1
    elif ch == 'b' or ch == 'B':
        return 2
    elif ch == 'n' or ch == 'N':
        return 3
    elif ch == 'r' or ch == 'R':
        return 4
    elif ch == 'c' or ch == 'C':
        return 5
    elif ch == 'p' or ch == 'P':
        return 6
    else:
        return 7


def StringToArray(FenStr):
    """
    将FEN串表示的局面转换成一维数组
    """
    pcWhite = [16, 17, 19, 21, 23, 25, 27]
    pcBlack = [32, 33, 35, 37, 39, 41, 43]

    if len(FenStr) == 0:
        return

    ClearBoard()

    fen_list = list(FenStr)
    i = 3
    j = 3
    for index in range(len(fen_list)):
        if fen_list[index] == ' ':
            break

        if fen_list[index] == '/':
            j = 3
            i = i + 1
            if i > 12:
                break
        elif fen_list[index] >= '1' and fen_list[index] <= '9':
            for k in range(ord(fen_list[index]) - ord('0')):
                if (j >= 11):
                    break;
                j = j + 1
        elif fen_list[index] >= 'A' and fen_list[index] <= 'Z':
            if (j <= 11):
                k = CharToSubscript(fen_list[index])
                if (k < 7):
                    if (pcWhite[k] < 32):
                        board[(i<<4) + j] = pcWhite[k]
                        pcWhite[k] = pcWhite[k] + 1
                j = j + 1
        elif fen_list[index] >= 'a' and fen_list[index] <= 'z':
            if (j <= 11):
                k = CharToSubscript(fen_list[index])
                if (k < 7):
                    if (pcBlack[k] < 48):
                        board[(i<<4) + j] = pcBlack[k]
                        pcBlack[k] = pcBlack[k] + 1
                j = j + 1

    index = index + 1
    if (fen_list[index] == 'b'):
        side = 1
    else:
        side = 0


def ArrayToString(bd):
    """
    将一维数组表示的局面转换成FEN串
    """

    fen_list = [' ']*256
    index = 0
    for i in range(3, 13):
        k = 0
        for j in range(3, 12):
            pc = bd[(i << 4) + j]
            if (pc != 0):
                if (k > 0):
                    fen_list[index] = chr(k + ord('0'))
                    index = index + 1
                    k = 0
                fen_list[index] = IntToChar(pc)
                index = index + 1
            else:
                k = k + 1
        if (k > 0):
            fen_list[index] = chr(k + ord('0'))
            index = index + 1
        fen_list[index] = '/'
        index = index + 1
    index = index - 1
    fen_list[index] = ' '
    index = index + 1
    if side == 0:
        fen_list[index] = 'w'
    else:
        fen_list[index] = 'b'

    return ("".join(fen_list))


def OutputBoard():
    """ 输出棋盘数组 """
    for i in range(len(board)):
        print(board[i], end=' ')
    print("")


def test_str_list():
    str1 = 'abcde'
    print(list(str1))


def test_main():
    print("****************************************************************")
    print(" 示例程序3-1       局面表示  一维数组与FEN串相互转换")
    print("****************************************************************")

    fen_string = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
    """
    "w":表示红方，"b":表示黑方
    "- -":在中国象棋中没有意义
    "0":表示双方没有吃子的走棋步数(半回合数)，通常该值达到120就要判和(六十回合自然限着)，
        一旦形成局面的上一步是吃子，这里就标记"0"
    "1":表示当前的回合数
    """
    print("FEN串:", fen_string)
    print("FEN串转换为一维数组")
    StringToArray(fen_string)
    OutputBoard()
    print("一维数组转换为FEN串")
    FenString = ArrayToString(board)
    print(FenString)

if __name__ == "__main__":
    test_str_list()
    test_main()
