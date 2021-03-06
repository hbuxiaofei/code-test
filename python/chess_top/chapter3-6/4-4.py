#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------变量声明-----------------------------------------------
side = 0                   # 轮到哪方走，0表示红方，1表示黑方
board = [0]*256            # 棋盘数组
piece = [0]*48             # 棋子数组
FenString = ""             # 局面的FEN串格式

class move(object):
    def __init__(self):
        self.from_pos = 0
        self.to_pos = 0

MoveArray = []      # 走法数组
for i in range(128):
    MoveArray.append(move())
MoveNum = 1;        # 走法总数，从1计数


# ----------------走法生成相关辅助数组---------------------------------------------
#各种棋子走法数组
KingDir =    [-0x10, -0x01, +0x01, +0x10,     0,     0,     0,     0]  # 将
AdvisorDir = [-0x11, -0x0f, +0x0f, +0x11,     0,     0,     0,     0]  # 士
BishopDir =  [-0x22, -0x1e, +0x1e, +0x22,     0,     0,     0,     0]  # 象
KnightDir =  [-0x21, -0x1f, -0x12, -0x0e, +0x0e, +0x12, +0x1f, +0x21]  # 马
RookDir =    [-0x01, +0x01, -0x10, +0x10,     0,     0,     0,     0]  # 车
CannonDir =  [-0x01, +0x01, -0x10, +0x10,     0,     0,     0,     0]  # 炮
PawnDir =   [[-0x01, +0x01, -0x10,     0,     0,     0,     0,     0],
             [-0x01, +0x01, +0x10,     0,     0,     0,     0,     0]] # 兵

KnightCheck = [-0x10,-0x10,-0x01,+0x01,-0x01,+0x01,+0x10,+0x10] # 马腿位置
BishopCheck = [-0x11,-0x0f,+0x0f,+0x11,0,0,0,0]                 # 象眼位置
kingpalace =  [54,55,56,70,71,72,86,87,88]                      # 黑方九宫位置


#各种棋子合理位置数组
LegalPosition = [
	[
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 1,25, 1, 9, 1,25, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 1, 9, 1, 9, 1, 9, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 17, 1, 1, 7, 19, 7, 1, 1, 17, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 1, 3, 7, 3, 1, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 17, 7, 3, 7, 17, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	    ],
	[
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 17, 7, 3, 7, 17, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 1, 3, 7, 3, 1, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 17, 1, 1, 7, 19, 7, 1, 1, 17, 0, 0, 0, 0,
	    0, 0, 0, 9, 1, 9, 1, 9, 1, 9, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 1,25, 1, 9, 1,25, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	    ]
	]
PositionMask = [2, 4, 16, 1, 1, 1, 8]


# --------------------函数实现----------------------------------

# 棋子整数值转换成字符表示
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
    for i in range(len(piece)):
        piece[i] = 0


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


def AddPiece(pos, pc):
    """
    增加棋子
    """
    board[pos] = pc
    piece[pc] = pos


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
                        AddPiece((i<<4) + j, pcWhite[k])
                        pcWhite[k] = pcWhite[k] + 1
                j = j + 1
        elif fen_list[index] >= 'a' and fen_list[index] <= 'z':
            if (j <= 11):
                k = CharToSubscript(fen_list[index])
                if (k < 7):
                    if (pcBlack[k] < 48):
                        AddPiece((i<<4) + j, pcBlack[k])
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
    for i in range(1, len(board)+1):
        print("%3d" % board[i-1], end='')
        if (i%16 == 0):
            print("")



def OutputPiece():
    """ 输出棋子数组 """
    print("棋子数组:")
    for i in range(0, 16):
        print("%4d" % piece[i], end='')
    print("")
    for i in range(16, 32):
        print("%4d" % piece[i], end='')
    print("")
    for i in range(32, 48):
        print("%4d" % piece[i], end='')
    print("")


def Check(lSide):
    """
    检测lSide一方是否被将军，是被将军返回1，否则返回0
    """
    SideTag = 32 - lSide * 16 # 此处表示lSide对方的将的值
    fSide = 1-lSide	# 对方标志
    PosAdd = 0	# 位置增量

    # wKing,bKing 红黑双方将帅的位置
    wKing = piece[16]
    bKing = piece[32]

    if (not wKing) or (not bKing):
        return 0

    # 检测将帅是否照面
    r = 1       # r=1表示将军，否则为0
    if (wKing%16 == bKing%16):
        wKing = wKing - 16
        while (wKing != bKing):
            if (board[wKing]):
                r=0
                break
            wKing=wKing - 16
        if (r):
            return r # 将帅照面

    q = piece[48-SideTag] # lSide方将的位置

    # 检测将是否被马攻击
    for i in range(5, 7):
        p = piece[SideTag + i]
        if (not p):
            continue
        for k in range(0, 8): # 8个方向
            n = p + KnightDir[k] # n为新的可能走到的位置
            if (n != q):
                continue
            if (LegalPosition[fSide][n] & PositionMask[3]): # 马将对应下标为3
                m = p + KnightCheck[k] # 马腿位置
                if (not board[m]): # 马腿位置无棋子占据
                    return 1

    # 检测将是否被车攻击
    r = 1
    for i in range(7, 9):
        p = piece[SideTag + i]
        if (not p):
            continue
        if (p%16 == q%16): # 在同一纵线上
            PosAdd = 16
            if p > q:
                PosAdd = -16
            else:
                PosAdd = 16

            p = p + PosAdd
            while (p != q):
                if (board[p]): # 车将中间有子隔着
                    r = 0
                    break
                p = p + PosAdd
            if (r):
                return r
        elif (p//16 == q//16): # 在同一横线上
            PosAdd = 1
            if p > q:
                PosAdd = -1
            else:
                PosAdd = 1

            p = p + PosAdd
            while (p != q):
                if (board[p]):
                    r = 0
                    break
                p = p + PosAdd
            if (r):
                return r

    # 检测将是否被炮攻击
    OverFlag = 0 # 翻山标志
    for i in range(9, 11):
        p = piece[SideTag + i]
        if (not p):
            continue
        if (p%16 == q%16): # 在同一纵线上
            PosAdd = 16
            if (p > q):
                PosAdd = -16
            else:
                PosAdd = 16

            p = p + PosAdd
            while (p != q):
                if (board[p]):
                    if(not OverFlag):  # 隔一子
                        OverFlag = 1
                    else:           # 隔两子
                        OverFlag = 2
                        break
                p = p + PosAdd
            if (OverFlag == 1):
                return 1
        elif (p//16 == q//16): # 在同一横线上
            PosAdd = 1
            if (p > q):
                PosAdd = -1
            else:
                PosAdd = 1

            p = p + PosAdd
            while (p != q):
                if(board[p]):
                    if (not OverFlag):
                        OverFlag = 1
                    else:
                        OverFlag = 2
                        break
                p = p + PosAdd
            if (OverFlag==1):
                return 1

    # 检测将是否被兵攻击
    for i in range(11, 16):
        p = piece[SideTag + i]
        if (not p):
            continue
        for k in range(3): # 3个方向
            n = p + PawnDir[fSide][k] # n为新的可能走到的位置
            if ((n == q) and (LegalPosition[fSide][n] & PositionMask[6])): # 兵士将对应下标为6
                return 1
    return 0


def InitGen():
    global MoveNum
    MoveNum = 0


def SaveMove(from_pos, to_pos):
    global MoveNum

    p = board[to_pos]
    piece[board[from_pos]] = to_pos
    if (p):
        piece[p]=0
    board[to_pos] = board[from_pos]
    board[from_pos] = 0

    r =Check(side)
    board[from_pos] = board[to_pos]
    board[to_pos] = p
    piece[board[from_pos]] = from_pos
    if (p):
        piece[p] = to_pos

    if (not r):
        MoveArray[MoveNum].from_pos = from_pos
        MoveArray[MoveNum].to_pos = to_pos
        MoveNum = MoveNum + 1


def KingMove(p):
    """
    将走棋
    """
    SideTag = 16 + side * 16 # 走棋方，红方16，黑方32
    for k in range(4):       # 4个方向
        n = p + KingDir[k]   # n为新的可能走到的位置
        if (LegalPosition[side][n] & PositionMask[0]): # 将对应下标为0
            if (not (board[n] & SideTag)): #目标位置上没有本方棋子
                SaveMove(p, n)


def AdvisorMove(p):
    """
    仕走棋
    """
    SideTag = 16 + side * 16  # 走棋方，红方16，黑方32
    for k in range(4):        # 4个方向
        n = p + AdvisorDir[k] # n为新的可能走到的位置
        if (LegalPosition[side][n] & PositionMask[1]): # 士将对应下标为1
            if (not (board[n] & SideTag)): # 目标位置上没有本方棋子
                SaveMove(p, n)


def BishopMove(p):
    """
    相走棋
    """
    SideTag = 16 + side * 16#走棋方，红方16，黑方32
    for k in range(4):        # 4个方向
        n = p + BishopDir[k]  # n为新的可能走到的位置
        if (LegalPosition[side][n] & PositionMask[2]):    # 象将对应下标为2
            m = p + BishopCheck[k]
            if not board[m]:  # 象眼位置无棋子占据
                if (not (board[n] & SideTag)): # 目标位置上没有本方棋子
                    SaveMove(p, n);


def KnightMove(p):
    """
    马走棋
    """
    SideTag = 16 + side * 16  # 走棋方，红方16，黑方32
    for k in range(8):        # 8个方向
        n = p + KnightDir[k]  # n为新的可能走到的位置
        if (LegalPosition[side][n] & PositionMask[3]): # 马将对应下标为3
            m = p + KnightCheck[k] # 马腿位置
            if (not board[m]):     # 马腿位置无棋子占据
                if (not (board[n] & SideTag)): # 目标位置上没有本方棋子
                    SaveMove(p, n)


def RookMove(p):
    """
    车走棋
    """
    SideTag = 16 + side * 16    # 走棋方，红方16，黑方32
    for k in range(4):          # 4个方向
        for j in range(1, 10):  # 横的最多有8个可能走的位置，纵向最多有9个位置
            n = p + j * RookDir[k]
            if (not (LegalPosition[side][n] & PositionMask[4])): # 车士将对应下标为4
                break
            if (not board[n]): # 目标位置上无子
                SaveMove(p, n)
            elif (board[n] & SideTag): # 目标位置上有本方棋子
                break
            else: # 目标位置上有对方棋子
                SaveMove(p, n)
                break


def CannonMove(p):
    """
    炮走棋
    """
    SideTag = 16 + side * 16    # 走棋方，红方16，黑方32
    for k in range(4):          # 4个方向
        OverFlag = 0
        for j in range(1, 10):  # 横的最多有8个可能走的位置，纵向最多有9个位置
            n = p + j * CannonDir[k]
            if (not (LegalPosition[side][n] & PositionMask[5])): # 炮士将对应下标为5
                break
            if (not board[n]):     # 目标位置上无子
                if (not OverFlag): # 未翻山
                    SaveMove(p, n)
                # 已翻山则不作处理，自动考察向下一个位置
            else: # 目标位置上有子
                if (not OverFlag): # 未翻山则置翻山标志
                    OverFlag = 1
                else: # 已翻山
                    if (not (board[n] & SideTag)): # 对方棋子
                        SaveMove(p, n)
                    break  # 不论吃不吃子，都退出此方向搜索


def PawnMove(p):
    """
    卒走棋
    """
    SideTag = 16 + side * 16 # 走棋方，红方16，黑方32
    for k in range(3): # 3个方向
        n = p + PawnDir[side][k] # n为新的可能走到的位置
        if (LegalPosition[side][n] & PositionMask[6]):    # 兵士将对应下标为6
            if (not (board[n] & SideTag)): # 目标位置上没有本方棋子
                SaveMove(p, n)


def GenAllMove():
    SideTag = 16 + side * 16   # 走棋方，红方16，黑方32

    for i in range(16):
        pc = SideTag + i
        p = piece[pc]
        if (p==0):
            continue
        if i == 0:   # 将
            KingMove(p)
        elif i == 1 or i == 2:  # 仕
            AdvisorMove(p)
        elif i == 3 or i == 4:  # 相
            BishopMove(p)
        elif i == 5 or i == 6:  # 马
            KnightMove(p)
        elif i == 7 or i == 8:  # 车
            RookMove(p)
        elif i == 9 or i == 10: # 炮
            CannonMove(p)
        elif i == 11 or i == 12 or i == 13 or i == 14 or i == 15: # 兵
            PawnMove(p)


def OutputMove():
    global MoveNum
    for i in range(MoveNum):
        print("from %d to %d" % (MoveArray[i].from_pos, MoveArray[i].to_pos))
    print("total move number:%d" % MoveNum)


def test_main():
    print("****************************************************************")
    print(" 示例程序4-4             走 法 生 成")
    print("")
    print("****************************************************************")
    print("初始局面:")
    # StringToArray("rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1")
    StringToArray("4k4/9/5a3/4p4/4C4/9/5R3/3nB4/9/2BAKA2r w - - 0 1");
    OutputBoard()

    OutputPiece()

    print("生成的走法:")
    InitGen()
    GenAllMove()
    OutputMove()



if __name__ == "__main__":
    test_main()
