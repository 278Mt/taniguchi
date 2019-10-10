# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Oct  9 10:47:54 2019

マインスイーパー
URL: https://github.com/278Mt/taniguchi/blob/master/04_1010_qt/Minesweeper_gui_opt.py
@author: n_toba
@id: 4617054
"""
import sys
from os.path import abspath
# Minesweeperのバックエンド処理を親ディレクトリからimportする。
# 無駄なImportErrorを引き起こさないようにするために、変数を殺したりポップしたりする。
dirname = abspath('../03_1003_Minesweeper')
sys.path.append(dirname)
del abspath
from Minesweeper import Game
sys.path.pop()
# オプション: 数字やxなどの代わりに、画像を表示するように工夫した。
im_dir = 'ms_im'
nonzero_png = 'ms_im/{}.png'.format
zero_png = '{}/zero.png'.format(im_dir)
flag_png = '{}/flag.png'.format(im_dir)
close_png = '{}/close.png'.format(im_dir)
mine_png = '{}/mine.png'.format(im_dir)
nonmine_png = '{}/nonmine.png'.format(im_dir)
flag_mine_png = '{}/flag-mine.png'.format(im_dir)
# 何をどこでimportしたか分かるようにするために書き換えた。
from PyQt5.QtWidgets import(
    QPushButton, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox
)
from PyQt5.QtGui import(
    QPixmap, QIcon
)
from PyQt5.QtCore import(
    Qt, QSize
)

MS_SIZE = 10          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2
MINE, NONMINE, FLAGMINE = -1, -2, -3
color_dic = {
    CLOSE  : 'gray',
    OPEN   : 'blue',
    FLAG   : 'yellow',
    MINE   : 'aqua',
    NONMINE: 'navy',
    FLAGMINE: 'teal'
}
# アイコンを表示する？　pngで設定するとか？
flag_str = 'P'
close_str = 'x'
iconsize = (50, 50)
status_bar_text = 'Shift+クリックでフラグをセット(フラグ数: {}, 予想残り地雷数: {})'.format

# ★今までに作成したコードからGameクラスをコピー★
# コピーせずに上位ディレクトリからimportする方が保守的に良いため、その方法をとった。

class MyPushButton(QPushButton):

    def __init__(self, text: str, x: int, y: int, parent):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(None, parent)
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
        print('x: {}, y: {}'.format(x, y))
        # スタックオーバーフローに掲載されていた方法を用いる
        # https://stackoverflow.com/questions/28588363/how-to-check-if-ctrl-and-shift-are-pressed-simultaneously-in-pyqt
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            print('フラグを立てます')
            game.flag_cell(x, y)
        else:
            print('セルを開けます')
            if game.open_cell(x, y) == False:
                self.__game_over()

        if game.is_finished():
            self.__game_clear()

        self.parent.show_cell_status()

        # オプション: 取り扱いしやすくなる工夫として、ステータスバーに残り地雷数を表示するように変更した
        number_of_flags = game.flatten_count(game.game_board, FLAG)
        number_of_residue = self.parent.number_of_mines-number_of_flags
        if number_of_residue < 0:
            number_of_residue = str(number_of_residue) + '?'
        self.parent.sb.showMessage(status_bar_text(number_of_flags, number_of_residue))


    def __game_over(self):
        print('ゲームオーバー!')
        self.parent.show_result(isclear=False)
        QMessageBox.information(self, 'Game Over', 'ゲームオーバー！')
        self.parent.close()


    def __game_clear(self):
        print('ゲームクリア!')
        self.parent.show_result(isclear=True)
        QMessageBox.information(self, 'Game Clear', 'ゲームクリア！')
        self.parent.close()



class MinesweeperWindow(QMainWindow):

    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        print('RUNNING PROGRAMME')
        super(MinesweeperWindow, self).__init__()
        self.game = Game(number_of_mines=20, size=MS_SIZE)
        self.initUI()


    def initUI(self):
        """ UIの初期化 """
        self.resize(500, 500)
        self.setWindowTitle('Minesweeper')

        # ★以下，コードを追加★
        self.number_of_mines = self.game.flatten_count(self.game.mine_map, MINE)
        self.sb = self.statusBar()
        self.sb.showMessage(status_bar_text(0, self.number_of_mines))  # ステータスバーに文言と表示
        self.__call_game_board()


    def __call_game_board(self):
        # ゲームボードを構築する.

        vbox = QVBoxLayout(spacing=0)
        self.button_dic = {}
        for y in reversed(range(MS_SIZE)):
            hbox = QHBoxLayout()
            for x in range(MS_SIZE):
                #button = MyPushButton(close_str, x, y, self)
                button = MyPushButton(close_str, x, y, self)
                button.set_bg_color()
                button.clicked.connect(button.on_click)
                close_im = QPixmap(close_png)
                button.setIcon(QIcon(close_im))
                button.setIconSize(QSize(*iconsize))
                hbox.addWidget(button)
                self.button_dic[(x, y)] = button

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
                        im = QPixmap(zero_png)
                    else:
                        im = QPixmap(nonzero_png(mine))
                elif part == FLAG:
                    im = QPixmap(flag_png)
                else:
                    im = QPixmap(close_png)
                button = self.button_dic[(x, y)]
                button.setIcon(QIcon(im))
                button.setIconSize(QSize(*iconsize))
                button.set_bg_color(color_dic[part])


    def show_result(self, isclear: bool=True):

        if not isclear:
            color_dic[MINE] = 'red'
            color_dic[FLAGMINE] = 'fuchsia'
            # global宣言をしないと、存在しないローカル変数を呼び出すことになる。これはPython上の仕様である。
            global mine_png
            mine_png = '{}/explode.png'.format(im_dir)
            global flag_mine_png
            flag_mine_png = '{}/flag-explode.png'.format(im_dir)

        for y in reversed(range(MS_SIZE)):
            for x in range(MS_SIZE):
                part = self.game.game_board[y][x]
                mine = self.game.mine_map[y][x]

                if mine == MINE and part == FLAG:
                    im = QPixmap(flag_mine_png)
                    color = color_dic[FLAGMINE]
                elif mine == MINE:
                    im = QPixmap(mine_png)
                    color = color_dic[MINE]
                elif mine != MINE and part == FLAG:
                    im = QPixmap(nonmine_png)
                    color = color_dic[NONMINE]
                elif mine == 0:
                    im = QPixmap(zero_png)
                    color = color_dic[OPEN]
                else:
                    im = QPixmap(nonzero_png(mine))
                    color = color_dic[OPEN]

                button = self.button_dic[(x, y)]
                button.setIcon(QIcon(im))
                button.setIconSize(QSize(*iconsize))
                button.set_bg_color(color)




def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()


if __name__ == '__main__':
    main()