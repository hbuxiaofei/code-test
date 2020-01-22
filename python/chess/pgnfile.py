#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import copy


fen2pgn_dic = {
        'C': [b'\xe8\xbd\xa6'], 'c': [b'\xe8\xbd\xa6'],
        'M': [b'\xe9\xa9\xac'], 'm': [b'\xe9\xa9\xac'],
        'X': [b'\xe7\x9b\xb8'], 'x': [b'\xe8\xb1\xa1'],
        'S': [b'\xe4\xbb\x95'], 's': [b'\xe5\xa3\xab'],
        'J': [b'\xe5\xb8\x85'], 'j': [b'\xe5\xb0\x86'],
        'P': [b'\xe7\x82\xae'], 'p': [b'\xe7\x82\xae'],
        'Z': [b'\xe5\x85\xb5'], 'z': [b'\xe5\x8d\x92'],

        '1': [b'\xe4\xb8\x80', b'\xef\xbc\x91'],
        '2': [b'\xe4\xba\x8c', b'\xef\xbc\x92'],
        '3': [b'\xe4\xb8\x89', b'\xef\xbc\x93'],
        '4': [b'\xe5\x9b\x9b', b'\xef\xbc\x94'],
        '5': [b'\xe4\xba\x94', b'\xef\xbc\x95'],
        '6': [b'\xe5\x85\xad', b'\xef\xbc\x96'],
        '7': [b'\xe4\xb8\x83', b'\xef\xbc\x97'],
        '8': [b'\xe5\x85\xab', b'\xef\xbc\x98'],
        '9': [b'\xe4\xb9\x9d', b'\xef\xbc\x99'],

        'f': [b'\xe8\xbf\x9b'],
        'b': [b'\xe9\x80\x80'],
        'l': [b'\xe5\xb9\xb3'],
        'h': [b'\xe5\x89\x8d'],
        'i': [b'\xe4\xb8\xad'],
        't': [b'\xe5\x90\x8e'],
        }


class Background(object):
    def __init__(self):
        self._ground = [
                "  -------------------------------------------------  ",
                "  |     |     |     | \   |   / |     |     |     |  ",
                "  |     |     |     |   \ | /   |     |     |     |  ",
                "  -------------------------------------------------  ",
                "  |     |     |     |   / | \   |     |     |     |  ",
                "  |     |     |     | /   |   \ |     |     |     |  ",
                "  ------*-----------------------------------*------  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  *-----------*-----------*-----------*-----------*  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  -------------------------------------------------  ",
                "  |                                               |  ",
                "  |                                               |  ",
                "  -------------------------------------------------  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  *-----------*-----------*-----------*-----------*  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  |     |     |     |     |     |     |     |     |  ",
                "  ------*-----------------------------------*------  ",
                "  |     |     |     | \   |   / |     |     |     |  ",
                "  |     |     |     |   \ | /   |     |     |     |  ",
                "  -------------------------------------------------  ",
                "  |     |     |     |   / | \   |     |     |     |  ",
                "  |     |     |     | /   |   \ |     |     |     |  ",
                "  -------------------------------------------------  ",
                ]

        self._format = {
                'C':(r"[ -]C[ -][ -]", "\033[0;37;41m[车]\033[0m"),
                'M':(r"[ -]M[ -][ -]", "\033[0;37;41m[马]\033[0m"),
                'X':(r"[ -]X[ -][ -]", "\033[0;37;41m[相]\033[0m"),
                'S':(r"[ -]S[ -][ -]", "\033[0;37;41m[仕]\033[0m"),
                'J':(r"[ -]J[ -][ -]", "\033[0;37;41m[帅]\033[0m"),
                'P':(r"[ -]P[ -][ -]", "\033[0;37;41m[炮]\033[0m"),
                'Z':(r"[ -]Z[ -][ -]", "\033[0;37;41m[兵]\033[0m"),

                'c':(r"[ -]c[ -][ -]", "\033[0;37;42m[车]\033[0m"),
                'm':(r"[ -]m[ -][ -]", "\033[0;37;42m[马]\033[0m"),
                'x':(r"[ -]x[ -][ -]", "\033[0;37;42m[象]\033[0m"),
                's':(r"[ -]s[ -][ -]", "\033[0;37;42m[士]\033[0m"),
                'j':(r"[ -]j[ -][ -]", "\033[0;37;42m[将]\033[0m"),
                'p':(r"[ -]p[ -][ -]", "\033[0;37;42m[炮]\033[0m"),
                'z':(r"[ -]z[ -][ -]", "\033[0;37;42m[卒]\033[0m"),
                }

    def set_pos(self, p, row, col):
        row_p = row * 3
        col_p = col * 6 + 2
        cur_str = self._ground[row_p]
        new_str = cur_str[:col_p] + p + cur_str[col_p+1:]
        self._ground[row_p] = new_str

    def get_pos(self, row, col):
        row_p = row * 3
        col_p = col * 6 + 2
        cur_str = self._ground[row_p]
        return cur_str[col_p:col_p+1]

    def show(self, flag=False):
        if flag:
            for row in range(10):
                pos_lists = []
                for col in range(9):
                    pos = self.get_pos(row, col)
                    if pos in self._format:
                        pos_lists.append(pos)
                if pos_lists:
                    for pos in set(pos_lists):
                        item = re.sub(self._format[pos][0],
                                      self._format[pos][1],
                                      self._ground[row * 3])
                        if item:
                            self._ground[row * 3] = item

        for item in self._ground:
            print(item)


class Board(object):
    """
    '进':'f', '退':'b', '平':'l',

    '前':'h', '中':'i', '后':'t',
    '二':'2', '三':'3', '四':'4', '五':'5'
    """
    def __init__(self):
        self._board = [
                ['c', 'm', 'x', 's', 'j', 's', 'x', 'm', 'c'],
                ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', 'p', '-', '-', '-', '-', '-', 'p', '-'],
                ['z', '-', 'z', '-', 'z', '-', 'z', '-', 'z'],
                ['-', '-', '-', '-', '-', '-', '-', '-', '-'],

                ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                ['Z', '-', 'Z', '-', 'Z', '-', 'Z', '-', 'Z'],
                ['-', 'P', '-', '-', '-', '-', '-', 'P', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                ['C', 'M', 'X', 'S', 'J', 'S', 'X', 'M', 'C']
                ]
        self._blacklist = ['c', 'm', 'x', 's', 'j', 'p', 'z']
        self._redlist = ['C', 'M', 'X', 'S', 'J', 'P', 'Z']
        self._leadlist = ['h', 'i', 't', '2', '3', '4', '5']
        self._actionlist = ['f', 'b', 'l']

    def print_obj(self):
        for row in self._board:
            print(row)

    def set_pos(self, p, row, col):
        self._board[row][col] = p

    def get_pos(self, row, col):
        return self._board[row][col]

    def get_step_red_from(self, pos, col):
        """
        TODO: 有两组兵同时同线（比如五路和四路各有两只兵）：则分别称为前兵四、后兵四；前兵五、后兵五
               ----------
                |      |
                |      |
               -Z------Z-
                |      |
                |      |
               ----------
                |      |
                |      |
               -Z------Z-
                |      |
        """
        step_from = None
        if pos in self._redlist:
            c = 9 - int(col)
            for row in range(10):
                if pos == self._board[row][c]:
                    step_from = (row, c)
                    break
        elif pos in self._leadlist:
            if pos == '5' or pos == 't':
                # '五':'5', '后':'t'
                index = 0
                for c in range(9):
                    #  for row in range(9, -1, -1):
                    index = 0
                    for row in range(10):
                        if col == self._board[row][c]:
                            index = index + 1
                            step_from = (row, c)
                    if index >= 2:
                        break
                if index < 2:
                    step_from = None
            else:
                if pos == 'h' or pos == 'i':
                    # '前':'h', '中':'i'
                    num = 1
                else:
                    # '二':'2', '三':'3', '四':'4'
                    num = int(pos)
                for c in range(9):
                    index = 0
                    for row in range(10):
                        if col == self._board[row][c]:
                            index = index + 1
                            if index == num:
                                step_from = (row, c)
                                break
                    if index == num:
                        break
        return step_from

    def get_step_red(self, pos, col, action, steps):
        step_from = self.get_step_red_from(pos, col)
        step_to_row = 0
        step_to_col = 0

        if step_from == None:
            return None

        length = 0
        # ['f', 'b', 'l']
        if action == 'f':
            length = 0 - int(steps)
        elif action == 'b':
            length = int(steps)

        kind = None
        if pos in self._redlist: # ['C', 'M', 'X', 'S', 'J', 'P', 'Z']
            kind = pos
        elif col in self._redlist:
            kind = col

        if kind == 'C' or kind == 'P':
            if action == 'f' or action == 'b':
                step_to_row = step_from[0] + length
                step_to_col = step_from[1]
            elif action == 'l':
                step_to_row = step_from[0]
                step_to_col = 9 - int(steps)
        elif kind == 'M':
            step_to_col = 9 - int(steps)
            if action == 'f':
                if abs(step_to_col - step_from[1]) == 2:
                    step_to_row = step_from[0] - 1
                else:
                    step_to_row = step_from[0] - 2
            elif action == 'b':
                if abs(step_to_col - step_from[1]) == 2:
                    step_to_row = step_from[0] + 1
                else:
                    step_to_row = step_from[0] + 2
        elif kind == 'X':
            if action == 'f':
                step_to_row = step_from[0] - 2
            elif action == 'b':
                step_to_row = step_from[0] + 2
            step_to_col = 9 - int(steps)
        elif kind == 'S':
            if action == 'f':
                step_to_row = step_from[0] - 1
            elif action == 'b':
                step_to_row = step_from[0] + 1
            step_to_col = 9 - int(steps)
        elif kind == 'J' or kind == 'Z':
            if action == 'f' or action == 'b':
                step_to_row = step_from[0] + length
                step_to_col = step_from[1]
            elif action == 'l':
                step_to_row = step_from[0]
                step_to_col = 9 - int(steps)

        return [step_from, (step_to_row, step_to_col)]

    def get_step_black_from(self, pos, col):
        step_from = None
        if pos in self._blacklist:
            c = int(col) - 1
            for row in range(10):
                if pos == self._board[row][c]:
                    step_from = (row, c)
                    break
        elif pos in self._leadlist:
            if pos == '5' or pos == 't':
                # '五':'5', '后':'t'
                index = 0
                for c in range(9):
                    index = 0
                    for row in range(9, -1, -1):
                        if col == self._board[row][c]:
                            index = index + 1
                            step_from = (row, c)
                    if index >= 2:
                        break
                if index < 2:
                    step_from = None
            else:
                if pos == 'h' or pos == 'i':
                    # '前':'h', '中':'i'
                    num = 1
                else:
                    # '二':'2', '三':'3', '四':'4'
                    num = int(pos)
                for c in range(9):
                    index = 0
                    for row in range(9, -1, -1):
                        if col == self._board[row][c]:
                            index = index + 1
                            if index == num:
                                step_from = (row, c)
                                break
                    if index == num:
                        break
        return step_from

    def get_step_black(self, pos, col, action, steps):
        step_from = self.get_step_black_from(pos, col)
        step_to_row = 0
        step_to_col = 0

        if step_from == None:
            return None

        length = 0
        # ['f', 'b', 'l']
        if action == 'f':
            length = int(steps)
        elif action == 'b':
            length = 0 - int(steps)

        kind = None
        if pos in self._blacklist: # ['c', 'm', 'x', 's', 'j', 'p', 'z']
            kind = pos
        elif col in self._blacklist:
            kind = col

        if kind == 'c' or  kind == 'p':
            if action == 'f' or action == 'b':
                step_to_row = step_from[0] + length
                step_to_col = step_from[1]
            elif action == 'l':
                step_to_row = step_from[0]
                step_to_col = int(steps) - 1
        elif kind == 'm':
            step_to_col = int(steps) - 1
            if action == 'f':
                if abs(step_to_col - step_from[1]) == 2:
                    step_to_row = step_from[0] + 1
                else:
                    step_to_row = step_from[0] + 2
            elif action == 'b':
                if abs(step_to_col - step_from[1]) == 2:
                    step_to_row = step_from[0] - 1
                else:
                    step_to_row = step_from[0] - 2
        elif kind == 'x':
            if action == 'f':
                step_to_row = step_from[0] + 2
            elif action == 'b':
                step_to_row = step_from[0] - 2
            step_to_col = int(steps) - 1
        elif kind == 's':
            if action == 'f':
                step_to_row = step_from[0] + 1
            elif action == 'b':
                step_to_row = step_from[0] - 1
            step_to_col = int(steps) - 1
        elif kind == 'j' or kind == 'z':
            if action == 'f' or action == 'b':
                step_to_row = step_from[0] + length
                step_to_col = step_from[1]
            elif action == 'l':
                step_to_row = step_from[0]
                step_to_col = int(steps) - 1

        return [step_from, (step_to_row, step_to_col)]

    def get_step(self, fen):
        """
        两个兵同线：从前到后称为前兵、后兵
        三个兵同线：从前到后称为前兵、中兵、后兵
        四个兵同线：从前到后称为前兵、二兵、三兵、后兵
        五个兵同线：从前到后称为前兵、二兵、中兵、四兵、后兵
        有两组兵同时同线（比如五路和四路各有两只兵）：则分别称为前兵四、后兵四；前兵五、后兵五
        """
        step = []

        line = fen.split("/")
        pos = line[1][0:1]
        col = line[1][1:2]
        action = line[1][2:3]
        steps = line[1][3:4]
        if line[0] == 'r':
            step = self.get_step_red(pos, col, action, steps)
        elif line[0] == 'b':
            step = self.get_step_black(pos, col, action, steps)

        return step

    def move(self, fen):
        step = self.get_step(fen)
        print("move: ", step)
        kind = self.get_pos(step[0][0], step[0][1])
        self.set_pos(kind, step[1][0], step[1][1])
        self.set_pos('-', step[0][0], step[0][1])

    def show(self, flag=False):
        ground = Background()
        row = 0
        for line in self._board:
            col = 0
            for p in line:
                ground.set_pos(p, row, col)
                col = col + 1
            row = row + 1
        ground.show(flag)

    def print_board(self):
        for row in range(10):
            line = []
            for col in range(9):
               p = self.get_pos(row, col)
               line.append(p)
            print(line)

        # ['f', 'b', 'l']
        #  step = self.move("r/Z7f1")
        #  step = self.move("r/P2f1")
        #  step = self.move("r/C1f1")
        #  step = self.move("r/M2f3")
        #  step = self.move("r/X3f5")
        #  step = self.move("r/S4f5")
        #  step = self.move("r/J5f1")

        #  step = self.move("b/z7f1")
        #  step = self.move("b/p2f1")
        #  step = self.move("b/c1f1")
        #  step = self.move("b/m2f3")
        #  step = self.move("b/x3f5")
        #  step = self.move("b/s4f5")
        #  step = self.move("b/j5f1")
        self.show(flag=True)


class PgnFile(object):
    def __init__(self, file_path=None):
        self._filepath = file_path
        self._game = {"match":r'\[Game(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._event = {"match":r'\[Event(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._round = {"match":r'\[Round(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._date = {"match":r'\[Date(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._site = {"match":r'\[Site(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._redteam = {"match":r'\[RedTeam(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._red = {"match":r'\[Red(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._blackteam = {"match":r'\[BlackTeam(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._black = {"match":r'\[Black(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._result = {"match":r'\[Result(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._ecco = {"match":r'\[ECCO(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._opening = {"match":r'\[Opening(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._variation = {"match":r'\[Variation(\s+)\"(.*)\"\]', "val":None, "type":"var"}
        self._movelist = {"match":r'(\s+)([0-9]+\.)(\s)(.*)', "val":[], "type":"list"}

        self._fenlist = {"val":[], "type":"list"}

    def get_val(self, line, dic):
        m = re.match(dic["match"], line)
        if m:
            if dic["type"] == "var":
                dic["val"] = m.group(2)
            elif dic["type"] == "list":
                dic["val"].append(m.group(4))
            return True
        return False

    def get_fen_from_pgn(self, pgn, is_red=True):
        fen = 'r/'
        if not is_red:
            fen = 'b/'
        pgn_types = bytes(pgn, "utf-8")
        pgn_types_len = int(len(pgn_types))
        for i in range(pgn_types_len//3):
            is_match = False
            pgn_types_i = (pgn_types[i*3]).to_bytes(length=1, byteorder='big') + \
                          (pgn_types[i*3+1]).to_bytes(length=1, byteorder='big') + \
                          (pgn_types[i*3+2]).to_bytes(length=1, byteorder='big')
            for key in fen2pgn_dic:
                for item in fen2pgn_dic[key]:
                    if item == pgn_types_i:
                        fen = fen + key
                        is_match = True
                        break
                if is_match:
                    break
            i = i + 1
        if is_red:
            return fen
        else:
            return fen.lower()

    def load_file(self):
        with open(self._filepath) as fp:
            for line in fp.readlines():
                if self.get_val(line, self._game):
                    pass
                elif self.get_val(line, self._event):
                    pass
                elif self.get_val(line, self._round):
                    pass
                elif self.get_val(line, self._date):
                    pass
                elif self.get_val(line, self._site):
                    pass
                elif self.get_val(line, self._redteam):
                    pass
                elif self.get_val(line, self._red):
                    pass
                elif self.get_val(line, self._blackteam):
                    pass
                elif self.get_val(line, self._black):
                    pass
                elif self.get_val(line, self._result):
                    pass
                elif self.get_val(line, self._ecco):
                    pass
                elif self.get_val(line, self._opening):
                    pass
                elif self.get_val(line, self._variation):
                    pass
                elif self.get_val(line, self._movelist):
                    pass
        for step in self._movelist["val"]:
            step_bytes = bytes(step, "utf-8")
            ret = self.get_fen_from_pgn(step.split()[0], is_red = True)
            self._fenlist["val"].append(ret)
            ret = self.get_fen_from_pgn(step.split()[1], is_red = False)
            self._fenlist["val"].append(ret)

    def print_obj(self):
        print('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))

    def get_fenlist(self):
        return self._fenlist


if __name__ == "__main__":
    pgn_file = PgnFile("./LOVEAY.PGN")
    pgn_file.load_file()
    pgn_file.print_obj()

    board = Board()
    board.print_obj()
    board.print_board()

    os.system("clear")
    fenlist = pgn_file.get_fenlist()
    for fen in fenlist["val"]:
        print("\x1b[0;0H")
        board.move(fen)
        board.show(True)
        print(fen)
        in_put = input()
        if in_put == 'q':
            break

    #  str_utf8 = ['进', '退',  '前', '中', '后', '二 二', '平' ]
    #  for item in str_utf8:
        #  print("%s(%d)  %s(%d)" % (item, len(item), bytes(item, "utf-8"), len(bytes(item,"utf-8"))))
