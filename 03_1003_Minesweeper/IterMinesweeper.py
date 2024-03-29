# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Sep 26 17:12:07 2019

マインスイーパー
URL: https://github.com/278Mt/taniguchi/blob/master/03_1003_Minesweeper/Minesweeper.py
たぶんぜんぶのオプションもやってある
本当は np で手抜きしたかったのに
リスト内包式はノロノロのノロなので、適宜 map からの list に書き換えている
@author: n_toba
@id: 4617054
"""
import random


MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2
MINE = -1



class Game(object):


    def __init__(self, number_of_mines: int=10):
        """ ゲームボードの初期化

        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """
        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()


    def arround_iter(self, x, y) -> iter:

        res = iter(sum(
            list(map(lambda x_:
                list(map(lambda y_:
                    (x_, y_),
                    range(max(0, y-1), min(MS_SIZE, y+2))
                )),
                range(max(0, x-1), min(MS_SIZE, x+2))
            )),
            []
        ))

        return res


    def init_game_board(self):
        """ ゲーム盤を初期化 """
        # <-- (STEP 1) ここにコードを追加
        # オプション1はやった
        self.game_board = list(map(lambda y:
            list(map(lambda x:
                CLOSE,
                range(MS_SIZE)
            )),
            range(MS_SIZE)
        ))

        return


    def init_mine_map(self, number_of_mines: int):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数

        地雷セルに-1を設定する．
        """
        # number_of_minesが規定数よりも多かったり少なかったりする場合を想定する
        if number_of_mines < 0:
            number_of_mines = 0
        elif number_of_mines > MS_SIZE ** 2:
            number_of_mines = MS_SIZE ** 2

        # <-- (STEP 2) ここにコードを追加
        # オプション2もやった。0 から 64 までの重複しないリストを生成してから、それを用いる
        idx_li = sorted(random.sample(range(MS_SIZE**2), number_of_mines))
        self.mine_map = list(map(lambda y:
            list(map(lambda x:
                MINE if y * 8 + x in idx_li else 0,
                range(MS_SIZE)
            )),
            range(MS_SIZE)
        ))

        return


    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納
        地雷数をmine_map[][]に設定する．
        """
        # <-- (STEP 3) ここにコードを追加

        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                if self.mine_map[y][x] != MINE:
                    self.mine_map[y][x] = list(map(lambda pos:
                        self.mine_map[pos[1]][pos[0]],
                        self.arround_iter(x, y)
                    )).count(MINE)

        return


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
        is_safe = self.mine_map[y][x] != MINE
        if is_safe:
            # ユーザーが指定したセルが既に開いている場合は、そのままで8近傍セルは開かない
            if self.game_board[y][x] != OPEN:
                # フラグが設置してある場合でも指定されていたら開く
                if self.game_board[y][x] == FLAG:
                    self.game_board[y][x] = OPEN

                for x_, y_ in self.arround_iter(x, y):

                    # フラグがあったら開かない
                    if self.game_board[y_][x_] == FLAG:
                        continue
                    # 8近傍のセルのうち地雷セルは開かない
                    elif self.mine_map[y_][x_] == MINE:
                        continue

                    self.game_board[y_][x_] = OPEN

        # ユーザーが指定したセルが地雷セルの場合は、ゲームオーバー
        return is_safe


    def flag_cell(self, x: int, y: int):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """
        # <-- (STEP 5) ここにコードを追加
        tmp = self.game_board[y][x]
        if tmp == CLOSE:
            self.game_board[y][x] = FLAG
        elif tmp == FLAG:
            self.game_board[y][x] = CLOSE

        return


    def is_finished(self) -> bool:
        """ 地雷セル以外のすべてのセルが開かれたかチェック """
        # <-- (STEP 6) ここにコードを追加
        # この足し算がキモい。そもそも、地雷の数はパブリック変数に入れておいてほしい。
        return sum(self.game_board, []).count(OPEN) + sum(self.mine_map, []).count(MINE) == MS_SIZE**2


    def print_header(self):

        print('=====================================')
        print('===  Mine Sweeper Python Ver. 1  ====')
        print('=====================================')

        return


    def print_footer(self):

        print('   {}[x]'.format('---'*MS_SIZE))
        print('   ' + ''.join(map(lambda x: '{:>3}'.format(x), range(MS_SIZE))))

        return


    def print_mine_map(self):

        print(' [y]')
        for y in range(MS_SIZE):
            print('{:>2}|'.format(y) + ''.join(map(lambda x: '{:>2}'.format(self.mine_map[y][x]), range(MS_SIZE))))

        return


    def print_game_board(self):

        marks = {CLOSE: 'x'*9, OPEN: ''.join(map(str, [' ', *range(1, 1+8)])), FLAG: 'P'*9}
        self.print_header()
        print('[y]')
        for y in range(MS_SIZE):
            # オプション3もやった
            print('{:>2}|'.format(y) + ''.join(map(lambda x: '{:>3}'.format(marks[self.game_board[y][x]][self.mine_map[y][x]]), range(MS_SIZE))))
        self.print_footer()

        return



if __name__ == '__main__':
    b = Game()
    quitGame = False

    while not quitGame:

        b.print_game_board()
        print('o x y: セルを開く，f x y: フラグ設定/解除, q: 終了 -->', end='')
        command_str = input()

        try:
            cmd = command_str.split(' ')
            if cmd[0] == 'o':
                x, y = list(map(int, cmd[1:]))
                if b.open_cell(x, y) == False:
                    print('ゲームオーバー!')
                    quitGame = True
            elif cmd[0] == 'f':
                x, y = list(map(int, cmd[1:]))
                b.flag_cell(x, y)
            elif cmd[0] == 'q':
                print('ゲームを終了します．')
                quitGame = True
                break
            else:
                print('コマンドはo, f, qのいずれかを指定してください．')
        except:
            print('もう一度，コマンドを入力してください．')

        if b.is_finished():
            b.print_game_board()
            print('ゲームクリア!')
            quitGame = True
