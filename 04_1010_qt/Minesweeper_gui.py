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
from PyQt5.QtWidgets import(
    QPushButton, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox
)
#from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2
color_dic = {CLOSE: 'gray', OPEN: 'blue', FLAG: 'yellow'}
# アイコンを表示する？　pngで設定するとか？
flag_str = 'P'
close_str = 'x'

# ★今までに作成したコードからGameクラスをコピー★
# コピーせずに上位ディレクトリからimportする方が保守的に良いため、その方法をとった。


class MyPushButton(QPushButton):

    def __init__(self, text, x: int, y: int, parent):
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
            colorname: 文字列 -- 色名 (例, 'white')
        """
        self.setStyleSheet('MyPushButton{{background-color: {}}}'.format(colorname))


    def on_click(self):
        """ セルをクリックしたときの動作 """
        # ★以下，コードを追加★
        game = self.parent.game
        x, y = self.x, self.y
        print('condition: {}, x: {}, y: {}'.format(self.text(), x, y))
        # https://stackoverflow.com/questions/28588363/how-to-check-if-ctrl-and-shift-are-pressed-simultaneously-in-pyqt
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            print('フラグを立てます')
            game.flag_cell(x, y)
        else:
            if game.open_cell(x, y) == False:
                self.__game_over()

        if game.is_finished():
            self.__game_clear()

        self.parent.show_cell_status()


    def __game_over(self):
        print('ゲームオーバー!')
        QMessageBox.information(self, 'Game Over', 'ゲームオーバー！')
        self.parent.close()


    def __game_clear(self):
        print('ゲームクリア!')
        QMessageBox.information(self, 'Game Clear', 'ゲームクリア！')
        self.parent.close()



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
        self.button_dic = {}
        for y in range(MS_SIZE-1, -1, -1):
            hbox = QHBoxLayout()
            for x in range(MS_SIZE):
                button = MyPushButton(close_str, x, y, self)
                button.set_bg_color()
                button.clicked.connect(button.on_click)
                self.button_dic[(x, y)] = button
                hbox.addWidget(button)
            vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.show()


    def show_cell_status(self):
        """ ゲームボードを表示 """
        # ★以下，コードを追加★
        # なんだこの実装は。ゴミクズみたいなスパゲッティーコードを実装させるな。頭悪すぎ。こんなので社会に通用すると思うな。
        for y in range(MS_SIZE-1, -1, -1):
            for x in range(MS_SIZE):
                part = self.game.game_board[y][x]
                mine = self.game.mine_map[y][x]
                if part == OPEN:
                    if mine == 0:
                        text = ' '
                    else:
                        text = str(self.game.mine_map[y][x])
                elif part == FLAG:
                    text = flag_str
                else:
                    text = close_str
                button = self.button_dic[(x, y)]
                button.setText(text)
                button.set_bg_color(color_dic[part])



def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()


if __name__ == '__main__':
    main()