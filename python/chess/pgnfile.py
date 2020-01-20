#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import copy

board_ground = [
"-------------------------------------------------",
"|     |     |     | \   |   / |     |     |     |",
"|     |     |     |   \ | /   |     |     |     |",
"-------------------------------------------------",
"|     |     |     |   / | \   |     |     |     |",
"|     |     |     | /   |   \ |     |     |     |",
"-------------------------------------------------",
"|     |     |     |     |     |     |     |     |",
"|     |     |     |     |     |     |     |     |",
"-------------------------------------------------",
"|     |     |     |     |     |     |     |     |",
"|     |     |     |     |     |     |     |     |",
"-------------------------------------------------",
"|                                               |",
"|                                               |",
"-------------------------------------------------",
"|     |     |     |     |     |     |     |     |",
"|     |     |     |     |     |     |     |     |",
"-------------------------------------------------",
"|     |     |     |     |     |     |     |     |",
"|     |     |     |     |     |     |     |     |",
"-------------------------------------------------",
"|     |     |     | \   |   / |     |     |     |",
"|     |     |     |   \ | /   |     |     |     |",
"-------------------------------------------------",
"|     |     |     |   / | \   |     |     |     |",
"|     |     |     | /   |   \ |     |     |     |",
"-------------------------------------------------",
]


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

        self._ground = copy.deepcopy(board_ground)

    def print_obj(self):
        for row in self._board:
            print(row)

    def set_pos(self, p, row, col):
        row_p = row * 3
        col_p = col * 6
        cur_str = self._ground[row_p]
        new_str = cur_str[:col_p] + p + cur_str[col_p+1:]
        self._ground[row_p] = new_str

    def get_pos(self, row, col):
        row_p = row * 3
        col_p = col * 6
        cur_str = self._ground[row_p]
        return  cur_str[col_p:col_p+1]

    def get_step(self, fen):
        step = []

        line = fen.split("/")
        if line[0] == 'r':
            pos = line[1][0:1]
            pos_fr = -1
            pos_fc = int(line[1][1:2])
            if pos in self._redlist:
                for pox_fr in range(10):
                    if pos == self._board[pos_fr][pos_fc]:
                        break
            print(pos)
        elif line[0] == 'b':
            print(line[0])
            print(line[1])

        return step


    def print_ground(self):
        row = 0
        for line in self._board:
            col = 0
            for p in line:
                self.set_pos(p, row, col)
                col = col + 1
            row = row + 1

        for item in self._ground:
            print(item)

        for row in range(10):
            line = []
            for col in range(9):
               p = self.get_pos(row, col)
               line.append(p)
            print(line)

        self.get_step("r/Z7f1")
        self.get_step("b/P2l3")


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
        return fen

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
        pass

if __name__ == "__main__":
    pgn_file = PgnFile("./LOVEAY.PGN")
    pgn_file.load_file()
    pgn_file.print_obj()

    board = Board()
    board.print_obj()
    board.print_ground()

    #  str_utf8 = ['进', '退',  '前', '中', '后', '二 二', '平' ]
    #  for item in str_utf8:
        #  print("%s(%d)  %s(%d)" % (item, len(item), bytes(item, "utf-8"), len(bytes(item,"utf-8"))))


