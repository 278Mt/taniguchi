# -*- coding: utf-8 -*-
#!/usr/bin/env python3.8
"""
Created on Sun Nov 24 12:31:20 2019

テトリスのアルゴリズム部分
URL: https://github.com/wakame-tech/vendredi-noir/blob/master/src/alg/Tetris.py
@author: n_toba
@id: 4617054
"""

import random


class TetrisError(Exception):

    pass



class Board(object):

    def __init__(self, board_size: [int]):

        if type(board_size) is not list or len(board_size) != 2:
            raise TetrisError(f'board_size must be list and its length is just 2.<board_size={board_size}>')

        self.board = [[0 for _ in range(board_size[1])] for _ in range(board_size[0])]


    def __getitem__(self, key: int or tuple):

        if type(key) is int:
            return self.board[key]
        elif type(key) is tuple and len(key) == 2:
            return self.board[key[0]][key[1]]
        else:
            raise TetrisError(f'Irregal key.<key={key}>')


    def __setitem__(self, key: int or tuple, val2: int or [int]):

        if type(key) is int:
            if type(val2) is int:
                for i in range(len(self.board[key])):
                    self.board[key][i] = val2
            elif type(val2) is list:
                for i in range(len(self.board[key])):
                    self.board[key][i] = val2[i]
            else:
                raise TetrisError(f'Irregal value.<val2={val2}>')
        elif type(key) is tuple and len(key) == 2 and type(val2) is int:
            self.board[key[0]][key[1]] = val2
        else:
            raise TetrisError(f'Irregal key.<key={key}>')


    def __repr__(self):

        res = ''
        for part in self.board:
            for element in part:
                res += f'{element} '
            res = f'{res[:-1]}\n'

        return res[:-1]


    def list2board(self):
        print('YES')
        pass



def list2board(board_li: list) -> Board:

    size = [20, 10]
    board = Board(size)
    for i in range(size[0]):
        for j in range(size[1]):
            board[i][j] = board_li[i][j]

    return board



# 本当は構造体にしたいけど、Pythonにはないから
class Tetrimino(object):

    def __init__(self):

        self.t4mino_li = [
            # i
            [[[1, i] for i in range(4)],
             [[i, 1] for i in range(4)]] * 2,
            # o
            [[[0, 0], [0, 1], [1, 0], [1, 1]]] * 4,
            # t
            [[[0, 1]] + [[1, i] for i in range(3)],
             [[1, 2]] + [[i, 1] for i in range(3)],
             [[2, 1]] + [[1, i] for i in range(3)],
             [[1, 0]] + [[i, 1] for i in range(3)]],
            # j
            [[[0, 0]] + [[1, i] for i in range(3)],
             [[0, 2]] + [[i, 1] for i in range(3)],
             [[2, 2]] + [[1, i] for i in range(3)],
             [[2, 0]] + [[i, 1] for i in range(3)]],
            # l
            [[[0, 2]] + [[1, i] for i in range(3)],
             [[2, 2]] + [[i, 1] for i in range(3)],
             [[2, 0]] + [[1, i] for i in range(3)],
             [[0, 0]] + [[i, 1] for i in range(3)]],
            # s
            [[[0, 1], [0, 2], [1, 0], [1, 1]],
             [[0, 0], [1, 0], [1, 1], [2, 1]]] * 2,
            # t
            [[[0, 0], [0, 1], [1, 1], [1, 2]],
             [[0, 1], [1, 0], [1, 1], [2, 0]]] * 2
        ]


    def __getitem__(self, key: tuple):

        if type(key) is not tuple or len(key) != 2:
            raise TetrisError(f'Irregal key.<key={key}>')

        return self.t4mino_li[key[0]][key[1]]



class Game(object):


    def __init__(self, cui_mode: bool=False):

        self.cui_mode = cui_mode
        self.board_size = [20, 10]
        self.init_t4mino()
        self.init_cur_li()
        self.init_board()
        self.gen_t4mino()


    def wait_key(self):

        import tty, termios, signal, sys
    
        def timeout(signum, frame):
            raise RuntimeError('timeout')

        signal.signal(signal.SIGALRM, timeout)
        signal.alarm(1)     # timeout sec
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                if ord(key) == 3:
                    raise KeyboardInterrupt()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except RuntimeError:
            key = None
        finally:
            signal.alarm(0)

        return key


    def init_t4mino(self):
        
        # including rotation table
        self.t4mino_li = Tetrimino()


    def init_cur_li(self):

        self.cur_li = []
        for _ in range(4):
            self.gen_t4mino()


    def update_cur_li(self):

        self.cur_li.pop(0)


    def init_board(self):

        self.board = Board(self.board_size)


    def game(self):

        cmd_load = 0
        while self.yet():

            if self.cui_mode:
                self.display()
            _pt = self.pt.copy()
            key = self.wait_key() if self.cui_mode else input()
            self.move(key)
            if key in list('hlfa') + [None]:
                cmd_load += 1
            if cmd_load == 2:
                cmd_load = 0
                self.move()
            if _pt == self.pt and (key is None or key not in 'hlfa'):
                self.save_board()
                self.update_cur_li()
                self.gen_t4mino()
                cmd_load = 0

        print('END')

        return False


    def yet(self):

        mid = self.board_size[1] // 2
        if sum(self.board[0, mid-2:mid+2]) == 0:
            return True
        return False


    def save_board(self):

        pt = self.pt
        for ix in self.t4mino_li[self.cur, self.rot]:
            self.board[ix[0]+pt[0], ix[1]+pt[1]] = self.cur + 1

        # flush
        for i in range(self.board_size[0]):
            if 0 not in self.board[i]:
                for i_ in reversed(range(i)):
                    self.board[i_+1] = self.board[i_]


    def move(self, to: str=' ') -> bool:

        pt = self.pt
        # left
        if   to == 'h':
            q_li = [pt[0]  , pt[1]-1, self.rot]
        # right
        elif to == 'l':
            q_li = [pt[0]  , pt[1]+1, self.rot]
        # rotate right
        elif to == 'f':
            q_li = [pt[0]  , pt[1]  ,(self.rot+1)%4]
        # rotate left
        elif to == 'a':
            q_li = [pt[0]  , pt[1]  ,(self.rot-1)%4]
        # fall
        elif to == 'd':
            while self.move(): pass
            return True
        # down
        else:
            q_li = [pt[0]+1, pt[1]  , self.rot]

        for ix in self.t4mino_li[self.cur, q_li[-1]]:
            if ix[0]+q_li[0] >= self.board_size[0]          \
            or ix[1]+q_li[1] < 0                            \
            or ix[1]+q_li[1] >= self.board_size[1]          \
            or self.board[ix[0]+q_li[0], ix[1]+q_li[1]] != 0:
                return False

        pt[0], pt[1], self.rot = q_li

        return True


    def element(self, i: int, j: int) -> str:

        ix_li = self.t4mino_li[self.cur, self.rot]
        pt = self.pt

        for ix in ix_li:
            if ix[0]+pt[0] == i and ix[1]+pt[1] == j:
                if self.cui_mode:
                    return chr(ord('０') + self.cur + 1)
                return self.cur + 1

        if self.cui_mode:
            tmp = self.board[i, j]
            return '　' if tmp == 0 else chr(ord('０')+tmp)

        return self.board[i, j]


    def display(self):

        ix_li = self.t4mino_li[self.cur, self.rot]
        pt = self.pt
        for i in range(self.board_size[0]):
            print('{:>2}|'.format(i), end='')
            for j in range(self.board_size[1]):
                print(self.element(i, j), end='')

            print('|')

        print('--+' + 'ー' * self.board_size[1] + '+')
        print(f'next: {[i+1 for i in self.cur_li]}')

    
    def set_pt_rot(self):

        # i, otjlst
        self.pt  = [0, self.board_size[1] // 2 - (2 if self.cur == 0 else 1)]
        self.rot = 0


    def gen_t4mino(self):

        self.cur_li.append(random.randrange(7))    # current tetrimino index

        self.cur = self.cur_li[0]
        self.set_pt_rot()



if __name__ == '__main__':

    g = Game(True)
    g.game()
