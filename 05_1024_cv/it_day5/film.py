import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2

class ObjDetector():

    """ 物体検出器 """
    def __init__(self, filename = None):
        # カスケード分類器の初期化
        self.cascade = cv2.CascadeClassifier()  # カスケード識別器のインスタンスを作成
        if filename != None:
            self.cascade.load(filename) # モデルファイルを読み込み

    def load(self, filename):
        self.cascade.load(filename)
        if self.cascade.empty():
            raise IOError("error in loading cascade file \"" + filename + "\"")

    def detect(self, im):
        """ 物体検出処理 """
        if self.cascade.empty():
            return []

        scalefactor = 1.1
        minneighbors = 3
        objects = self.cascade.detectMultiScale(im, scaleFactor=scalefactor, minNeighbors=minneighbors)

        #count = len(objects)
        #print('detection count: %s' % (count,))

        return objects


class VideoCaptureView(QGraphicsView):
    """ ビデオキャプチャ """
    repeat_interval = 200 # ms 間隔で画像更新

    def __init__(self, parent = None):
        """ コンストラクタ（インスタンスが生成される時に呼び出される） """
        super(VideoCaptureView, self).__init__(parent)

        # 変数を初期化
        self.pixmap = None
        self.item = None
        self.rect_items = []

        # VideoCapture (カメラからの画像取り込み)を初期化
        self.capture = cv2.VideoCapture(0)

        if self.capture.isOpened() is False:
            raise IOError("failed in opening VideoCapture")

        # 描画キャンバスの初期化
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pen = QPen(QColor(0xff, 0x00, 0x00))     # ペンを作成 (RGB)
        self.pen.setWidth(3)                          # ペンの太さを設定
        #self.brush = QBrush(QColor(0xff, 0xff, 0xff), Qt.SolidPattern)    #ブラシを作成
        self.brush = QBrush()

        self.setVideoImage()

        # タイマー更新 (一定間隔でsetVideoImageメソッドを呼び出す)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setVideoImage)
        self.timer.start(self.repeat_interval)

    def setVideoImage(self):
        """ ビデオの画像を取得して表示 """
        ret, cv_img = self.capture.read()                # ビデオキャプチャデバイスから画像を取得
        if ret is False:
            return

        cv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)  # 色変換 BGR->RGB
        height, width, dim = cv_img.shape
        bytesPerLine = dim * width                       # 1行辺りのバイト数

        # 物体検出を実行
        # <--- ここに追加


        self.image = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        if self.pixmap is None:                          # 初回はQPixmap, QGraphicPixmapItemインスタンスを作成
            self.pixmap = QPixmap.fromImage(self.image)
            self.item = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.item)                # キャンバスに配置
        else:
            self.pixmap.convertFromImage(self.image)     # ２回目以降はQImage, QPixmapを設定するだけ
            self.item.setPixmap(self.pixmap)

        # 物体検出を実行
        rects = detector.detect(cv_img)
        # 直前に描画した矩形を削除
        for item in self.rect_items:
            self.scene.removeItem(item)
        # 新しい矩形を描画
        self.rect_items = []
        for (x, y, w, h) in rects:
            self.rect_items.append(self.scene.addRect(x, y, w, h, self.pen, self.brush))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)

    #detector = ObjDetector("models/lbpcascades/lbpcascade_frontalface.xml")
    detector = ObjDetector("models/haarcascades/haarcascade_frontalface_default.xml")

    main = QMainWindow()              # メインウィンドウmainを作成
    main.setWindowTitle("Face Detector")
    viewer = VideoCaptureView()       # VideoCaptureView ウィジエットviewを作成
    main.setCentralWidget(viewer)     # mainにviewを埋め込む
    main.show()

    app.exec_()

    viewer.capture.release()
