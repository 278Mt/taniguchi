import numpy as np


class OthelloError(Exception):

    pass


class Othello(object):


    def __init__(self, size: int=8):

        if size % 2 != 0:
            raise OthelloError(f'size must be even number. <size: {size}>')

        self.size = size
        self.space = 0
        self.black = 1
        self.white = 2
        self.turn = self.black
        self.wait = self.white
        self.init_board()


    def init_board(self):

        size = self.size
        mid = size // 2
        self.board = np.full([size, size], self.space, dtype=np.int)
        self.board[mid-1, mid-1] = self.board[mid  , mid  ] = self.black
        self.board[mid  , mid-1] = self.board[mid-1, mid  ] = self.white


    def display(self):

        size = self.size
        turn = self.turn
        board = self.board
        black = self.black
        white = self.white
        print('[y]')
        print('--+' + '--' * size + '+--')
        for i in range(size):
            print('{:>2}|'.format(i), end='')
            for j in range(size):
                tmp = board[i, j]
                if tmp == black:
                    ch = '黒'
                elif tmp == white:
                    ch = '白'
                elif self.is_stoned(i, j):
                    ch = f'{j}{i}'
                else:
                    ch = '  '
                print(ch, end='')

            print('|')

        print('--+' + '--' * size + '+--')
        print('  |', end='')
        for j in range(size):
            print('{:>2}'.format(j), end='')

        print('[x]')
        print(f'turn: {"黒" if turn==black else "白"}, black: {self.count(white)}, white: {self.count(black)}')


    def get_ix(self):

        size = self.size
        while True:
            try:
                j, i = map(int, input('xy: '))
                if 0 <= i < size and 0 <= j < size:
                    return i, j
            except ValueError:
                continue


    def game(self):

        while True:

            self.display()
            i, j = self.get_ix()
            if not self.exist_stone(i, j) or self.is_filled() or self.is_pan_syn():
                break

        count_black = self.count(self.black)
        count_white = self.count(self.white)
        self.display()
        if count_black > count_white:
            print('黒 win')
        elif count_black < count_white:
            print('白 win')
        else:
            print('draw')


    def count(self, stone: int) -> int:

        return np.count_nonzero(self.board==stone)


    def is_filled(self) -> bool:

        return self.count(self.space) == 0


    def is_pan_syn(self):

        return self.count(self.black) == 0 \
        or     self.count(self.white) == 0


    def is_stoned(self, i: int, j: int, read_only: bool=True) -> bool:

        board = self.board
        size = self.size
        space = self.space
        turn = self.turn
        wait = self.wait

        if board[i, j] != space:
            return False

        to_li = [j+1, size-j, i+1, size-i, min(i+1, j+1), min(size-i, size-j), min(i+1, size-j), min(size-i, j+1)]
        query_li = [
            lambda i, j, k: (i  , j-k) if                j-k >= 0   else None,    # left
            lambda i, j, k: (i  , j+k) if                j+k < size else None,    # right
            lambda i, j, k: (i-k, j  ) if i-k >= 0                  else None,    # up
            lambda i, j, k: (i+k, j  ) if i+k < size                else None,    # down
            lambda i, j, k: (i-k, j-k) if i-k >= 0   and j-k >= 0   else None,    # left up
            lambda i, j, k: (i+k, j+k) if i+k < size and j+k < size else None,    # right down
            lambda i, j, k: (i-k, j+k) if i-k >= 0   and j+k < size else None,    # right up
            lambda i, j, k: (i+k, j-k) if i+k < size and j-k >= 0   else None     # left down
        ]

        res = False
        p = 0
        for to, query in zip(to_li, query_li):
            p += 1
            ix = query(i, j, 1)

            if ix is not None and board[ix] == wait:
                for k in range(2, to):
                    ix = query(i, j, k)

                    tmp = board[ix]
                    if tmp == turn:
                        res = True
                        if read_only:
                            return True

                        for k_ in range(1, k):
                            board[query(i, j, k_)] = turn

                    elif tmp == space:
                        break

        return res


    def exist_stone(self, i: int, j: int) -> bool:

        size = self.size
        if self.is_stoned(i, j, read_only=False):
            self.board[i, j] = self.turn
            self.turn, self.wait = self.wait, self.turn
            for i in range(size):
                for j in range(size):
                    if self.is_stoned(i, j):
                        return True

            self.turn, self.wait = self.wait, self.turn
            for i in range(size):
                for j in range(size):
                    if self.is_stoned(i, j):
                        return True

            return False

        return True

    
if __name__ == '__main__':

    o = Othello()
    o.game()
