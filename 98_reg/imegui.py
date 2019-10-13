#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 15:56:01 2019

@author: 278mt
"""

import sys
from PyQt5.QtWidgets import(
    QMainWindow, QApplication, QAction, QFileDialog, QHBoxLayout, QLabel, QWidget
)
from PyQt5.QtGui import(
    QPixmap
)
from PyQt5.QtCore import(
    Qt, QEvent
)
from imedit import Graph


class GUIWindow(QMainWindow):

    def __init__(self):

        super(GUIWindow, self).__init__()
        self.initUI()


    def initUI(self):

        self.resize(500, 500)
        self.setWindowTitle('ImEdit')
        print('ファイルのアップデートを要求')
        
        # メニューバーのアイコン設定
        openFile = QAction('&Open', self)
        # ショートカット設定
        openFile.setShortcut('Ctrl+O')
        # ステータスバー設定
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.__call_imedit)

        # メニューバー作成
        # macの場合はこれを書かないとちゃんと動作しないよ
        menubar = self.menuBar()
        from platform import system
        if system() == 'Darwin':
            menubar.setNativeMenuBar(False)
            del system
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        #fname = 'sample_im.png'
        #self.xg = Graph(fname)
        #self.statusBar().showMessage('Shift+クリックでフラグをセット')  # ステータスバーに文言と表示


    def __call_imedit(self):

        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        print('fname: {}'.format(fname))
        self.xg = Graph(fname)
        self.xg.laplacian()

        hbox = QHBoxLayout()
        
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(fname))
        self.label.installEventFilter(self)

        hbox.addWidget(self.label)
        
        container = QWidget()
        container.setLayout(hbox)
        self.setCentralWidget(container)

        h, w = self.xg.im.shape[:2]
        self.resize(w+50, h+50)


    def eventFilter(self, source, event):
        
        if event.type() == QEvent.MouseButtonPress and source is self.label:
            if event.button() == Qt.LeftButton:
                pos = event.pos()
                x, y = pos.x(), pos.y()
                
                self.__edit(x, y)
                
        return QWidget.eventFilter(self, source, event)
    
    
    def __edit(self, x: int, y: int):
        
        xg = self.xg
        rngelm = 2
        for x in range(max(0, x-rngelm), min(x+rngelm+1, xg.im.shape[1])):
            for y in range(max(0, y-rngelm), min(y+rngelm+1, xg.im.shape[0])):                    
                xg.filtering(point=(x, y))
                xg.inpainting()
            
        xg.imsave(xg.dst, fname='tmp.png')
        self.label.setPixmap(QPixmap('tmp.png'))


def main():
    
    app = QApplication(sys.argv)
    w = GUIWindow()
    w.show()
    app.exec_()


# これをすることによって、ガベコレをプログラム終了時と同時に殺すことができる。
if __name__ == '__main__':
    
    main()
