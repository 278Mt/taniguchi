import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np

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
    

class MyWindow(QMainWindow):
    
    def __init__(self, viewer):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MyWindow, self).__init__()
        self.initUI(viewer)
  
    def initUI(self, viewer):
        """ UIの初期化 """
        """↓ ここから """
        # (1) ニュー項目[File]-[Select]が選択されたときのアクションを生成
        selectAction = QAction('&Select', self)
        # (2) メニュー項目が選択されたときの処理として，MyViewクラスのsetImageメソッドを設定
        selectAction.triggered.connect(viewer.setImage)
        
        # (3) メインウィンドウのメニューバーオブジェクトを取得
        menubar = self.menuBar()
        # (4) メニューバーに[File]メニューを追加し，そのアクションとしてselectActionを登録
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(selectAction)
        
        self.resize(600, 600)
    
    
class MyView(QGraphicsView):

    def __init__(self, parent = None):
        """ コンストラクタ（インスタンスが生成される時に呼び出される） """
        super(MyView, self).__init__(parent)
        
        # 変数を初期化
        self.pixmap = None
        self.item = None
        self.rect_items = []

        # 描画キャンバスの初期化
        self.scene = QGraphicsScene()
        self.setScene(self.scene) 
        self.pen = QPen(QColor(0xff, 0x00, 0x00))     # ペンを作成 (RGB)
        self.pen.setWidth(3)                          # ペンの太さを設定
        #self.brush = QBrush(QColor(0xff, 0xff, 0xff), Qt.SolidPattern)    #ブラシを作成
        self.brush = QBrush()

    def setImage(self):
        """ 画像を取得して表示 """
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')     # 画像を選択してファイル名を取得
        n = np.fromfile(file_name[0], dtype=np.uint8)    # imreadだと日本語のファイル名に対応できないため，np.fromfileとcv2.imdecodeを使う
        cv_img = cv2.imdecode(n, cv2.IMREAD_COLOR)        
        if cv_img is None:
            return
        cv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)  # 色変換 BGR->RGB
        height, width, dim = cv_img.shape
        bytesPerLine = dim * width                       # 1行辺りのバイト数
        
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
    
    detector = ObjDetector("models/haarcascades/haarcascade_frontalface_default.xml")
    
    viewer = MyView()       # MyView ウィジエットviewを作成
    main = MyWindow(viewer)
    main.setWindowTitle("Face Detector")
    main.setCentralWidget(viewer)     # mainにviewを埋め込む
    main.show()
    
    app.exec_()
