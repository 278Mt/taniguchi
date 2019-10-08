#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 12:11:15 2019

ブレインアナリスト協会のデータを解析する
@author: 278mt
"""
import sys
from os.path import abspath
dirname = abspath('../03_1003_Minesweeper')
del abspath
sys.path.append(dirname)
from Minesweeper import Game
from PyQt5.QtWidgets import QMainWindow, QApplication
import datetime



class MyWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        print('RUNNING THE PROGRAMME')
        super(MyWindow, self).__init__()
        self.initUI()
    
    
    def initUI(self):
        """ UIの初期化 """
        self.resize(250, 150)           # 250x150ピクセルにリサイズ
        self.setWindowTitle('MyWindow') # タイトルを設定
        
        self.time_draw()                # 現在時刻をステータスバーに表示
        
        self.show()


    def time_draw(self):
        """ 現在時刻をステータスバーに表示 """
        d = datetime.datetime.today()
        daystr=d.strftime('%Y-%m-%d %H:%M:%S')
        self.statusBar().showMessage(daystr)   # ステータスバーを取得しsendMessage()メソッドを呼び出す

# この def main をサボると、カーネルがぶっ飛ぶらしい。Flaskと似てる。
def main():
    
    app = QApplication(sys.argv)
    w = MyWindow()
    app.exec_()


if __name__ == '__main__':
    main()