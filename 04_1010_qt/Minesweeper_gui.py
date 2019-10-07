import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

# ★今までに作成したコードからGameクラスをコピー★

class Game:
    pass

class MyPushButton(QPushButton):
    
    def __init__(self, text, x, y, parent):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent
        self.x = x
        self.y = y
        self.setMinimumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, 
            QSizePolicy.MinimumExpanding)
        
    def set_bg_color(self, colorname):
        """ セルの色を指定する
        Arguments:
            self
            colorname: 文字列 -- 色名 (例, "white")
        """
        self.setStyleSheet("MyPushButton{{background-color: {}}}".format(colorname))
        
    def on_click(self):
        """ セルをクリックしたときの動作 """
        # ★以下，コードを追加★
        pass
            
class MinesweeperWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
    
    def initUI(self):
        """ UIの初期化 """        
        self.resize(100, 100) 
        self.setWindowTitle('Minesweeper')
        
        # ★以下，コードを追加★
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