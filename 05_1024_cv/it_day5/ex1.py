import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np

class VideoCaptureView(QGraphicsView):
    """ ビデオキャプチャ """
    repeat_interval = 200 # ms 間隔で画像更新

    def __init__(self, parent = None):
        """ コンストラクタ（インスタンスが生成される時に呼び出される） """
        super(VideoCaptureView, self).__init__(parent)
        
        # 変数を初期化
        self.pixmap = None
        self.item = None
        
        # VideoCapture (カメラからの画像取り込み)を初期化
        self.capture = cv2.VideoCapture(0)

        if self.capture.isOpened() is False:
            raise IOError("failed in opening VideoCapture")

        # ウィンドウの初期化
        self.scene = QGraphicsScene()   # 描画用キャンバスを作成
        self.setScene(self.scene) 
        self.setVideoImage()
        
        # タイマー更新 (一定間隔でsetVideoImageメソッドを呼び出す)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setVideoImage)
        self.timer.start(self.repeat_interval)
        
    def setVideoImage(self):
        """ ビデオの画像を取得して表示 """
        ret, cv_img = self.capture.read()                # ビデオキャプチャデバイスから画像を取得
        if ret == False:
            return
        cv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)  # 色変換 BGR->RGB
        
        cv_img = self.processing(cv_img)

        height, width, dim = cv_img.shape
        bytesPerLine = dim * width                       # 1行辺りのバイト数
        
        #cv_img = self.processing(cv_img)
        
        self.image = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        if self.pixmap == None:                          # 初回はQPixmap, QGraphicPixmapItemインスタンスを作成
            self.pixmap = QPixmap.fromImage(self.image)
            self.item = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.item)                # キャンバスに配置
        else:
            self.pixmap.convertFromImage(self.image)     # ２回目以降はQImage, QPixmapを設定するだけ
            self.item.setPixmap(self.pixmap)
    
    def processing(self, src):
        """ 画像処理 """
        im = src.copy()
        
        dst = cv2.resize(im, (320, 240))
        # <-- 練習問題1: ここにコードを追加
        
        # 階調変換
        
        # 空間フィルタ

        # 一部領域のみ
        
        return dst
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    
    main = QMainWindow()              # メインウィンドウmainを作成
    main.setWindowTitle("Video Capture")
    viewer = VideoCaptureView()       # VideoCaptureView ウィジエットviewを作成
    main.setCentralWidget(viewer)     # mainにviewを埋め込む
    main.show()
    
    app.exec_()
    
    viewer.capture.release()
