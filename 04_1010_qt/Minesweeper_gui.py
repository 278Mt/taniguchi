# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Oct  9 10:45:35 2019

マインスイーパー
URL: https://github.com/278Mt/taniguchi/blob/master/04_1010_qt/Minesweeper_gui.py
@author: n_toba
@id: 4617054
"""

"""
文字列を検索する方法
emacs          -> Ctrl-S または Command-S + 文字列
vim            -> /(スラッシュ)           + 文字列
VS Code        -> Ctrl-F または Command-F + 文字列
jupyter        -> Ctrl-F または Command-F + 文字列
spyder         -> Ctrl-F または Command-F + 文字列
atom           -> Ctrl-F (? たぶん)       + 文字列
xcode          -> 氏ね。Pythonでxcode使うな。(たぶんCommand-F + 文字列)
他のエディター -> 知らないけどたぶん Ctrl-F か Command-F をすれば出てくると思う。ググれば出てくるし便利。
"""

import sys
from os.path import abspath
# 捜索するディレクトリにさっきの dirname を追加。こうすることで、 Minesweeper.py から Game をラクに import できる
# sys.path.append についてはググって。
dirname = abspath('../03_1003_Minesweeper')
del abspath
sys.path.append(dirname)
from Minesweeper import Game
from PyQt5.QtWidgets import(
    QPushButton, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt


MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2
COLOR_DIC = {
    CLOSE: 'gray',
    OPEN : 'blue',
    FLAG : 'yellow'
}
FLAG_STR = 'P'
CLOSE_STR = 'x'

# ★今までに作成したコードからGameクラスをコピー★
# コピーせずに上位ディレクトリから import する方が保守的に良いため、その方法をとった。


# button に関する。ここが一番面倒だと思う。
class MyPushButton(QPushButton):

    def __init__(self, text: str, x: int, y: int, parent):
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
        # game board の召喚は下に書く。こうすることで可読性が上がる。
        self.__call_game_board()


    def __call_game_board(self):
        # ゲームボードを構築する.

        vbox = QVBoxLayout(spacing=0)
        self.button_dic = {}
        # reversed 自体は書く必要ないけど、あった方が最初に作った Game における座標との整合性が取りやすくなる。
        for y in reversed(range(MS_SIZE)):
            hbox = QHBoxLayout()
            for x in range(MS_SIZE):
                # MyPushButton の引数の parent はこのクラスが生成されるときにできるインスタンス自体。
                # と言われてもピンとこない人には、「とりあえず書かなきゃならないやつ」というふうに説明。
                # というか、このプログラムの著者本人も最初 1 時間くらい、 MyPushButton の中に parent がある訳がわからなかった。
                button = MyPushButton(CLOSE_STR, x, y, self)
                button.set_bg_color()

                # button と関数をつなげる。
                # ここで button.clicked.connect(lambda: button.on_click()) とカッコよく lambda でキメちゃったりすると、
                # 開示座標が x, y == 7, 0 で固定されてしまうので注意。理由は鳥羽もよくわかってないです。m(__)m
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
        # like spaghetti
        for y in reversed(range(MS_SIZE)):
            for x in range(MS_SIZE):
                part = self.game.game_board[y][x]
                mine = self.game.mine_map[y][x]
                if part == OPEN:
                    if mine == 0:
                        text = ' '
                    else:
                        text = str(mine)
                elif part == FLAG:
                    text = FLAG_STR
                else:
                    text = CLOSE_STR
                # ここで button を書き換える操作を記述する。
                button = self.button_dic[(x, y)]
                button.setText(text)
                button.set_bg_color(COLOR_DIC[part])



def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()


if __name__ == '__main__':
    main()
