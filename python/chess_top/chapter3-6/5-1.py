
PieceValue = [1000,20,20,40,90,45,10,0]

# 棋子整数值转换成字符表示
def IntToSubscript(a):
    if (a >= 32):
        a = a-16

    if a == 16:
        return 0
    elif a == 17 or a == 18:
        return 1
    elif a == 19 or a == 20:
        return 2
    elif a == 21 or a == 22:
        return 3
    elif a == 23 or a == 24:
        return 4
    elif a == 25 or a == 26:
        return 5
    elif a == 27 or a == 28 or a == 29 or a == 30 or a == 31:
        return 6
    else:
        return 7


def Eval():
    bValue = 0
    wValue = 0
    for i in range(3, 13): # 10行
        for j in range(3, 12): # 9列
            p = (i<<4) + j  # 棋子位置
            if (board[p] == 0): # 无棋子
                continue
            elif (board[p] <32 ) == 0):
                wValue = wValue + PieceValue[IntToSubscript(board[p])]
            else:
                bValue = bValue + PieceValue[IntToSubscript(board[p])];
    return wValue - bValue

