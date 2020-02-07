
PieceValue = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1000,20,20,20,20,40,40,90,90,45,45,10,10,10,10,10,
1000,20,20,20,20,40,40,90,90,45,45,10,10,10,10,10]

def Eval():
    bValue = 0
    wValue = 0
    for i in range(16, 32):
        if (piece[i]>0):
            wValue = wValue + PieceValue[i]
    for i in range(32, 48):
        if (piece[i]>0):
            bValue = bValue + PieceValue[i]
    return wValue - bValue

