import sys
from PyQt5.QtWidgets import(
    QMainWindow, QAction, QApplication
)
import datetime


class MyWindow(QMainWindow):

    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MyWindow, self).__init__()
        self.initUI()


    def initUI(self):
        """ UIの初期化 """
        """↓ ここから """
        # (1) ニュー項目[File]-[Exit]が選択されたときのアクションを生成
        exitAction = QAction('&Exit', self)
        # (2) メニュー項目が選択されたときの処理として，qApp.quitを設定
        #exitAction.triggered.connect(qApp.quit)
        exitAction.triggered.connect(self.close)

        # (3) メインウィンドウのメニューバーオブジェクトを取得
        menubar = self.menuBar()
        # macの場合はこれを書かないとちゃんと動作しないよ
        from platform import system
        if system() == 'Darwin':
            menubar.setNativeMenuBar(False)
            del system
        # (4) メニューバーに[File]メニューを追加し，そのアクションとしてexitActionを登録
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        """ ↑ここまで"""

        self.time_draw()

        self.resize(250, 150)           # 250x150ピクセルにリサイズ
        self.setWindowTitle('MyWindow') # タイトルを設定
        self.show()


    def time_draw(self):
        """ 現在時刻をステータスバーに表示 """
        d = datetime.datetime.today()
        daystr = d.strftime('%Y-%m-%d %H:%M:%S')
        self.statusBar().showMessage(daystr)   # ステータスバーを取得しsendMessage()メソッドを呼び出す



def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    app.exec_()


if __name__ == '__main__':
    main()
