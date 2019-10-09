# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Oct  9 10:49:13 2019

マインスイーパー
URL: https://github.com/278Mt/taniguchi/blob/master/04_1010_qt/mac_surwindow.py
@author: n_toba
@id: 4617054
"""
import sys
from PyQt5.QtWidgets import(
    QMainWindow, QApplication, QMessageBox
)


class MyWindow(QMainWindow):

    def __init__(self, warn_title: str='警告', warn_msg: str= 'Warning! 何かおかしいようです',  info_title: str='情報', info_msg: str='Please contact at hoge@gmail.com'):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        self.warn_title, self.warn_msg, self.info_title, self.info_msg = warn_title, warn_msg, info_title, info_msg
        super(MyWindow, self).__init__()
        self.initUI()

    def initUI(self):
        """ UIの初期化 """
        self.resize(250, 150)           # 250x150ピクセルにリサイズ
        self.setWindowTitle('MyWindow') # タイトルを設定
        self.show()

        """ ↓ここから """
        # message box
        result = QMessageBox.question(self, 'Message',
                    'PyQtに慣れましたか?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            print ('Selected Yes.')
        else:
            print ('Selected No.')

        # Warning Message box
        # Qtの公式仕様書(https://doc.qt.io/archives/qt-4.8/qmessagebox.html#setWindowTitle)　によると、
        # macOSでは、setWindowTitleが使えないことになっている。まじですか……。
        msgBox = QMessageBox()
        msgBox.warning(self, '警告', self.warn_msg)

        # Information Message box
        QMessageBox.information(self, '情報', self.info_msg)
        """ ↑ここまで """


def main():
    warn_title='macで表示させたみが深い警告だけど出てきてくれない'
    warn_msg='あなたはPyQtについて何も知らないようですね'
    info_title='macで表示させたみが深い情報だけど出てきてくれない'
    info_msg='適切なGメールアドレスに送信してください'
    app = QApplication(sys.argv)
    w = MyWindow(warn_title=warn_title, warn_msg=warn_msg, info_title=info_title, info_msg=info_msg)
    app.exec_()


if __name__ == '__main__':
    main()
