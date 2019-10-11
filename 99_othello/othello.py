#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:49:20 2019

othello
@author: 278mt
"""
SIZE = 8
SPACE, BLACK, WHITE = 0, 1, 2


class Othello(object):

    def __init__(self, size: int=8):

        global SIZE
        SIZE = max(4, size//2*2)

        self.__make_board()


    def __make_board(self):

        self.board = [[SPACE for _ in range(SIZE)] for _ in range(SIZE)]
        centre = SIZE // 2
        self.board[centre  ][centre  ] = self.board[centre-1][centre-1] = BLACK
        self.board[centre-1][centre  ] = self.board[centre  ][centre-1] = WHITE


    def show_board(self):

        print(' [i]')
        for i in range(SIZE):
            print('{:>2}|'.format(i) + ''.join(['{:>3}'.format(self.board[i][j]) for j in range(SIZE)]))

        print('   {}[j]'.format('---'*SIZE))
        print('   ' + ''.join(['{:>3}'.format(j) for j in range(SIZE)]))


    def stone(self, i: int, j: int):

        pass



if __name__ == '__main__':

    o = Othello()
    o.show_board()
