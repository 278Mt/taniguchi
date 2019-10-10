# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Oct  3 16:13:20 2019

マインスイーパー
numpyを使った
ただし、ベンチマークでは二次元リスト型によるものなので、TestMinesweeperではこれを実行できない。
URL: https://github.com/278Mt/taniguchi/blob/master/03_1003_Minesweeper/NpMinesweeper.py
@author: n_toba
"""
import numpy as np
from scipy.signal import correlate2d
from random import randrange

MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2
MINE = -1


def timer(fn):
    from time import time
    def inr_fn(*args, **kwargs):
        com = time()
        res = fn(*args, **kwargs)
        print(time() - com)

        return res

    return inr_fn


class Game(object):


    def __init__(self, number_of_mines: int=10, size: int=8):
        """ ゲームボードの初期化

        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """
        global MS_SIZE
        MS_SIZE = size
        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()


    def init_game_board(self):
        """ ゲーム盤を初期化 """
        # <-- (STEP 1) ここにコードを追加
        # オプション1はやった
        # 追加課題
        # init_game_board(): 配列の初期化関数を使って 1 行で表現
        self.game_board = np.zeros([MS_SIZE] * 2, dtype=np.int8)


    def init_mine_map(self, number_of_mines: int):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数

        地雷セルに-1を設定する．
        """
        # number_of_minesが規定数よりも多かったり少なかったりする場合を想定する
        number_of_mines = min(max(number_of_mines, 0), MS_SIZE ** 2)

        # <-- (STEP 2) ここにコードを追加
        # オプション2もやった。0 から 64 までの重複しないリストを生成してから、それを用いる
        self.mine_map = np.zeros([MS_SIZE] * 2, dtype=np.int8)
        for y, x in self.fisher_yates(number_of_mines):
            self.mine_map[y, x] = MINE


    # random.sample が「期待した答え」ではなかったらしいので、変更
    def fisher_yates(self, number_of_mines) -> list:

        tmp_li = [i for i in range(MS_SIZE**2)]
        res = []
        for i in range(number_of_mines):
            idx = randrange(0, MS_SIZE**2 - i)
            res.append(divmod(tmp_li[idx], MS_SIZE))
            tmp_li.pop(idx)

        return sorted(res)


    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納
        地雷数をmine_map[][]に設定する．
        """
        # <-- (STEP 3) ここにコードを追加
        # 追加課題
        # count_mines(): 4 重ループを 2 重ループに減らす
        # signal で畳み込みをすればもっと短く書ける

        mask = np.full([3] * 2, MINE)
        mask[1, 1] = 0
        tmp = correlate2d(self.mine_map, mask, mode='same', boundary='fill')
        self.mine_map[self.mine_map != MINE] = tmp[self.mine_map != MINE]


    def open_cell(self, x: int, y: int) -> bool:
        """ セル(x, y)を開ける
        Arguments:
        x, y -- セルの位置

        Returns:
          True  -- 8近傍セルをOPENに設定．
                   ただし，既に開いているセルの近傍セルは開けない．
                   地雷セル，FLAGが設定されたセルは開けない．
          False -- 地雷があるセルを開けてしまった場合（ゲームオーバ）
        """
        # <-- (STEP 4) ここにコードを追加
        is_safe = self.mine_map[y, x] != MINE
        if is_safe:
            # ユーザーが指定したセルが既に開いている場合は、そのままで8近傍セルは開かない
            if self.game_board[y, x] != OPEN:
                # フラグが設置してある場合でも指定されていたら開く
                if self.game_board[y, x] == FLAG:
                    self.game_board[y, x] = OPEN

                x_slice = slice(max(0, x-1), min(MS_SIZE, x+2))
                y_slice = slice(max(0, y-1), min(MS_SIZE, y+2))
                for _x in range(max(0, x-1), min(MS_SIZE, x+2)):
                    for _y in range(max(0, y-1), min(MS_SIZE, y+2)):
                        # フラグがあったら開かない
                        if self.game_board[_y, _x] == FLAG:
                            continue
                        # 8近傍のセルのうち地雷セルは開かない
                        elif self.mine_map[_y, _x] == MINE:
                            continue

                        self.game_board[_y, _x] = OPEN

        # ユーザーが指定したセルが地雷セルの場合は、ゲームオーバー
        return is_safe


    def flag_cell(self, x: int, y: int):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """
        # <-- (STEP 5) ここにコードを追加
        tmp = self.game_board[y, x]
        if tmp == CLOSE:
            self.game_board[y, x] = FLAG
        elif tmp == FLAG:
            self.game_board[y, x] = CLOSE


    def is_finished(self) -> bool:
        """ 地雷セル以外のすべてのセルが開かれたかチェック """
        # <-- (STEP 6) ここにコードを追加
        # is_finished() : 1 行で表現
        # 追加課題
        return np.all(self.mine_map[self.game_board != OPEN] == MINE)


    def print_header(self):

        print('=====================================')
        print('===  Mine Sweeper Python Ver. 1  ====')
        print('=====================================')


    def print_footer(self):

        print('   {}[x]'.format('---'*MS_SIZE))
        print('   ' + ''.join(map(lambda x: '{:>3}'.format(x), range(MS_SIZE))))


    def print_mine_map(self):

        print(' [y]')
        for y in range(MS_SIZE):
            print('{:>2}|'.format(y) + ''.join(map(lambda x: '{:>3}'.format(self.mine_map[y, x]), range(MS_SIZE))))


    def print_game_board(self):

        marks = {CLOSE: 'x'*9, OPEN: ''.join(map(str, [' ', *range(1, 1+8)])), FLAG: 'P'*9}
        self.print_header()
        print('[y]')
        for y in range(MS_SIZE):
            # オプション3もやった
            print('{:>2}|'.format(y) + ''.join(map(lambda x: '{:>3}'.format(marks[self.game_board[y, x]][self.mine_map[y, x]]), range(MS_SIZE))))
        self.print_footer()



if __name__ == '__main__':
    b = Game()

    if False:
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                if b.mine_map[y, x] != -1:
                    b.game_board[y, x] = OPEN

    while True:

        b.print_game_board()
        print('o x y: セルを開く，f x y: フラグ設定/解除, q: 終了 -->', end='')
        command_str = input()

        try:
            cmd = command_str.split(' ')
            if cmd[0] == 'o':
                x, y = list(map(int, cmd[1:]))
                if b.open_cell(x, y) == False:
                    print('ゲームオーバー!')
                    break
            elif cmd[0] == 'f':
                x, y = list(map(int, cmd[1:]))
                b.flag_cell(x, y)
            elif cmd[0] == 'q':
                print('ゲームを終了します．')
                break
            else:
                print('コマンドはo, f, qのいずれかを指定してください．')
        except:
            print('もう一度，コマンドを入力してください．')

        if b.is_finished():
            b.print_game_board()
            print('ゲームクリア!')
            break
