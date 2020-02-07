
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


# 评估函数
def Eval():
    bValue = 0
    wValue = 0
    for i in range(16, 32):
	if (piece[i]>0):
            wValue = wValue + PieceValue[IntToSubscript(i)]
    for i in range(32, 48):
	if (piece[i]>0):
	    bValue = bValue + PieceValue[IntToSubscript(i)]
    return wValue - bValue

