# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Sep 26 17:12:07 2019

マインスイーパー
URL: https://github.com/278Mt/taniguchi/blob/master/
@author: n_toba
@id: 4617054
"""
import sys
from os.path import abspath
dirname = abspath('../03_1003_Minesweeper')
del abspath
sys.path.append(dirname)
from Minesweeper import Game
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random


MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

# ★今までに作成したコードからGameクラスをコピー★
# コピーせずに上位ディレクトリからimportする方が保守的に良いため、その方法をとった。


class MyPushButton(QPushButton):
    
    def __init__(self, text, x: int, y: int, parent=None):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent
        self.x = x
        self.y = y
        self.setMinimumSize(20, 20)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        
    def set_bg_color(self, colorname: str='gray'):
        """ セルの色を指定する
        Arguments:
            self
            colorname: 文字列 -- 色名 (例, "white")
        """
        self.setStyleSheet("MyPushButton{{background-color: {}}}".format(colorname))
        
        
    def on_click(self, game: Game):
        """ セルをクリックしたときの動作 """
        # ★以下，コードを追加★
        QApplication.keyboardModifiers()
        self.game = game
        self.clicked.connect(self.__fn)
        
        
    def __fn(self):
        
        x, y, text_str = self.x, self.y, self.text()
        print('condition: {}, x: {}, y: {}'.format(text_str, x, y))
        self.game.open_cell(x, y)


    
class MinesweeperWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        print('RUNNING PROGRAMME')
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
    
    
    def initUI(self):
        """ UIの初期化 """        
        self.resize(500, 500)
        self.setWindowTitle('Minesweeper')
        
        # ★以下，コードを追加★
        self.statusBar().showMessage('Shift+クリックでフラグをセット')  # ステータスバーに文言と表示
        self.__call_game_board()


    def __call_game_board(self):
        # ゲームボードを構築する.

        vbox = QVBoxLayout(spacing=0)
        for y in range(MS_SIZE-1, -1, -1):
            hbox = QHBoxLayout()
            for x in range(MS_SIZE):
                text = self.game.mine_map[y][x] if self.game.game_board[y][x]==OPEN else 'P' if self.game.game_board[y][x]==FLAG else 'x'
                b = MyPushButton(text, x, y)
                b.set_bg_color()
                b.on_click(self.game)
                hbox.addWidget(b)
            vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.show()


    def show_cell_status(self):
        """ ゲームボードを表示 """
        # ★以下，コードを追加★
                 
        
        
def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()
            
    
if __name__ == '__main__':
    main()