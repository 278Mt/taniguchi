# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Oct  9 10:47:54 2019

マインスイーパー
ディレクトリ構成
.
|- 03_1003_Minesweeper
|  |- Minesweeper.py
|
|- 04_1010_qt
   |- Minesweeper_gui_opt.py
   |- help.txt
   |- ms_im
      |- *.png

URL: https://github.com/278Mt/taniguchi/blob/master/04_1010_qt/Minesweeper_gui_opt.py
@author: n_toba
@id: 4617054
"""
import sys
from os.path import(
    abspath, isfile, isdir
)
# Minesweeperのバックエンド処理を親ディレクトリからimportする。
# 余分なImportErrorを引き起こさないために、パスをポップしておく
dirname = abspath('../03_1003_Minesweeper')
if isdir(dirname) or isfile('Minesweeper.py'):
    sys.path.append(dirname)
    from Minesweeper import Game
    sys.path.pop()
else:
    raise FileNotFoundError('指定されたディレクトリにファイルがありません<dirname: {}>'.format(dirname))
# オプション: 数字やxなどの代わりに、画像を表示するように工夫した。
# 何をどこでimportしたか分かるようにするために書き換えた。
from PyQt5.QtWidgets import(
    QPushButton, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox, QAction
)
from PyQt5.QtGui import(
    QPixmap, QIcon
)
from PyQt5.QtCore import(
    Qt, QSize
)

MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2
MINE, NONMINE, FLAGMINE = -1, -2, -3
# アイコンを表示する？　pngで設定するとか？

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
        # スタックオーバーフローに掲載されていた方法を用いる
        # https://stackoverflow.com/questions/28588363/how-to-check-if-ctrl-and-shift-are-pressed-simultaneously-in-pyqt
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            print('フラグを立てます<x: {}, y: {}>'.format(x, y))
            game.flag_cell(x, y)
        else:
            print('セルを開けます<x: {}, y: {}>'.format(x, y))
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
        self.parent.sb.showMessage(self.parent.statusbar_str(number_of_flags, number_of_residue))


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
        self.statusbar_str = 'Shift+クリックでフラグをセット(フラグ数: {}, 予想残り地雷数: {})'.format
        self.iconsize = (50, 50)
        print('RUNNING PROGRAMME')
        super(MinesweeperWindow, self).__init__()

        # 画像の設定
        im_dir = 'ms_im'
        im_dic = {
            CLOSE   : {'color': 'gray',   'png': 'close'},
            OPEN    : {'color': 'blue',   'png': {i: i for i in range(8+1)}},
            FLAG    : {'color': 'yellow', 'png': 'flag'},
            MINE    : {'color': 'aqua',   'png': 'mine'},
            NONMINE : {'color': 'navy',   'png': 'nonmine'},
            FLAGMINE: {'color': 'teal',   'png': 'flagmine'}
        }
        for key in im_dic:
            if key == OPEN:
                for num in im_dic[key]['png']:
                    im_dic[key]['png'][num] = QIcon(QPixmap('{}/{}.png'.format(im_dir, num)))

            else:
                im_dic[key]['png'] = QIcon(QPixmap('{}/{}.png'.format(im_dir, im_dic[key]['png'])))

        self.im_dir = im_dir
        self.im_dic = im_dic
        self.game = Game(number_of_mines=10, size=MS_SIZE)
        self.initUI()


    def initUI(self):
        """ UIの初期化 """
        self.resize(500, 500)
        self.setWindowTitle('Minesweeper')

        # menubarを追加
        self.__menuBarUI()

        # ★以下，コードを追加★
        self.number_of_mines = self.game.flatten_count(self.game.mine_map, MINE)
        self.sb = self.statusBar()
        self.sb.showMessage(self.statusbar_str(0, self.number_of_mines))  # ステータスバーに文言と表示
        self.__call_game_board()


    def __menuBarUI(self):

        # ヘルプの文章を取り出す
        help_path = 'help.txt'
        if isfile(help_path):
            with open(help_path, mode='r') as file:
                help_text = file.read()
        else:
            help_text = 'ヘルプを表示します。'

        helpAction = QAction('&Help', self)
        helpAction.triggered.connect(lambda: QMessageBox.information(self, 'Help', help_text))
        exitAction = QAction('&Exit', self)
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        # macの場合はこれを書かないとちゃんと動作しないよ
        from platform import system
        if system() == 'Darwin':
            menubar.setNativeMenuBar(False)
            del system
        fileMenu = menubar.addMenu('&Tool')
        fileMenu.addAction(helpAction)
        fileMenu.addAction(exitAction)


    def __call_game_board(self):
        # ゲームボードを構築する.

        vbox = QVBoxLayout(spacing=0)
        self.button_dic = {}
        for y in reversed(range(MS_SIZE)):
            hbox = QHBoxLayout()
            for x in range(MS_SIZE):
                button = MyPushButton('x', x, y, self)
                button.set_bg_color()
                button.clicked.connect(button.on_click)
                button.setIcon(self.im_dic[CLOSE]['png'])
                button.setIconSize(QSize(*self.iconsize))
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
        im_dic = self.im_dic
        for y in reversed(range(MS_SIZE)):
            for x in range(MS_SIZE):
                part = self.game.game_board[y][x]
                mine = self.game.mine_map[y][x]
                if part == OPEN:
                    im = im_dic[OPEN]['png'][mine]
                elif part == FLAG:
                    im = im_dic[FLAG]['png']
                else:
                    im = im_dic[CLOSE]['png']
                button = self.button_dic[(x, y)]
                button.setIcon(im)
                button.setIconSize(QSize(*self.iconsize))
                button.set_bg_color(im_dic[part]['color'])


    def show_result(self, isclear: bool=True):

        im_dic = self.im_dic
        if not isclear:
            im_dic[MINE]['color'] = 'red'
            im_dic[FLAGMINE]['color'] = 'fuchsia'
            # global宣言をしないと、存在しないローカル変数を呼び出すことになる。これはPython上の仕様である。

            im_dic[MINE]['png'] = QIcon(QPixmap('{}/explode.png'.format(self.im_dir)))
            im_dic[FLAGMINE]['png'] = QIcon(QPixmap('{}/flagexplode.png'.format(self.im_dir)))

        for y in reversed(range(MS_SIZE)):
            for x in range(MS_SIZE):
                part = self.game.game_board[y][x]
                mine = self.game.mine_map[y][x]

                if mine == MINE and part == FLAG:
                    im = im_dic[FLAGMINE]['png']
                    color = im_dic[FLAGMINE]['color']
                elif mine == MINE:
                    im = im_dic[MINE]['png']
                    color = im_dic[MINE]['color']
                elif mine != MINE and part == FLAG:
                    im = im_dic[NONMINE]['png']
                    color = im_dic[NONMINE]['color']
                else:
                    im = im_dic[OPEN]['png'][mine]
                    color = im_dic[OPEN]['color']

                button = self.button_dic[(x, y)]
                button.setIcon(QIcon(im))
                button.setIconSize(QSize(*self.iconsize))
                button.set_bg_color(color)



def main():

    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()


if __name__ == '__main__':
    main()
