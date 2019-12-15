import numpy as np
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


MIN_WIDTH = 150 # 横幅をこの大きさまで縮める


class SeamCarving():


    def __init__(self, filename, window):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        self.window = window
        if filename is not None:
            self.img = cv2.imread(filename)
            width = self.img.shape[1]
            if width < MIN_WIDTH:
                print(f'The width of the input image must be larger than {MIN_WIDTH}')
                sys.exit()


    def carve(self):
        """ 実際にシームカービングを行うメソッド """

        width = self.img.shape[1]
        carved_images = [] ### 出力画像を格納するリスト
        carved_images.append(self.img.copy())
        self.window.setImages(carved_images)

        """"""""" 指定した横幅になるまで繰り返す """""""""
        prev_img = self.img
        for i in range(width, MIN_WIDTH, -1):
            energy_map = self.computeEnergy(prev_img) ### エネルギーマップを計算
            seam = self.findSeam(energy_map) ### エネルギー最小のシームを見つける
            out_img = self.removeSeam(prev_img, seam) ### 見つけたシームを取り除く
            prev_img = out_img

            carved_images.append(np.uint8(out_img.copy())) ### 出力画像を格納

            """"""""" スライダの値を変えながら進捗を表示 """""""""
            self.window.slider.setValue(i-1)
            self.window.pbar.setValue((width-i)/(width-MIN_WIDTH-1)*100)
            qApp.processEvents()

        # 最終画像の保存
        cv2.imwrite('output.jpg', prev_img)

        """"""""" 終わったら進捗バーを非表示 """""""""
        self.window.pbar.hide()


    def computeEnergy(self, img):
        """ エネルギーマップを計算するメソッド """
        # ★以下，コードを追加（STEP 1）★
        # maybe clear
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # matplotlibによる画像の表示のためRGBの順に変換
        xsobel = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        ysobel = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        lap = cv2.Laplacian(img, cv2.CV_64F)
        dst = np.abs(xsobel) + np.abs(ysobel) + np.abs(lap)
        out = np.sum(dst, axis=2)

        return out


    def findSeam(self, energy_map):
        """ エネルギー最小のシームを見つけるメソッド """

        height, width = energy_map.shape[0:2]
        # ★以下，コードを追加（STEP 2）★
        # まずエネルギーの累積計算をする
        conv = np.pad(energy_map, [(0,0),(1,1)], 'constant', constant_values=np.inf)
        # broadcastの計算にすることによって、2重for文よりも高速化される。
        for h in range(height-1):
            conv[h+1, 1:-1] += np.min(np.vstack([
                                   conv[h,  :-2],
                                   conv[h, 1:-1],
                                   conv[h, 2:  ]
                               ]), axis=0)

        seam = np.zeros((height), dtype=np.int32)
        idx = np.where(conv[-1]==np.min(conv[-1]))[0][0]
        pre_idx = seam[-1] = idx + (0 if idx >= 0 else width)

        for h in reversed(range(height-1)):

            part = conv[h, pre_idx-1:pre_idx+2]
            idx = np.where(part==np.min(part))[0][0] + pre_idx - 1
            pre_idx = seam[h] = idx + (0 if idx >= 0 else width)

        return seam - 1


    def removeSeam(self, img, seam):
        """ シームを取り除くメソッド """
        height, width, dim = img.shape
        out = np.zeros((height, width-1, dim), dtype=img.dtype)
        for i in range(height):
            out[i,:seam[i],:] = img[i,:seam[i],:]
            out[i,seam[i]:,:] = img[i,seam[i]+1:,:]

        return out



class MyWindow(QMainWindow):


    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MyWindow, self).__init__()
        self.initUI()


    def initUI(self):
        """ UIの初期化 """
        self.setWindowTitle('Seam Carving') # タイトルを設定

        # (1) QLabelとQSliderのWidget（インスタンス）を生成
        slider_label = QLabel('Width (pix):') # ラベルを生成
        self.slider = QSlider(Qt.Horizontal) # 横向きのスライダを生成
        # (2) sliderの値が変わったときにchangeImage()メソッドを呼び出すよう設定
        self.slider.valueChanged.connect(self.changeImage)
        # (3) QHBoxLayout(Widget1を水平方向に並べる)を生成し，slider_label, sliderを追加
        hbox = QHBoxLayout()
        hbox.addWidget(slider_label)
        hbox.addWidget(self.slider)
        # (4) QLineEdit（1行テキスト編集)のwidget(インスタンス)を生成しhboxに追加
        self.textbox = QLineEdit()
        self.textbox.setFixedWidth(30)
        hbox.addWidget(self.textbox)
        # (5) QVBoxLayout(Widetを垂直方向に並べる)を生成し，QLabel(後で画像を入れる)と進捗バーとhboxを追加
        vbox = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        vbox.addWidget(self.label)
        # 進捗バーの設定
        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)
        vbox.addWidget(self.pbar)
        vbox.addLayout(hbox)
        # (6) ウィンドウにvboxレイアウトを設定
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)


    def setImages(self, imgs):
        """ ウィンドウに画像を表示するメソッド(最初の1回目のみ) """
        self.carved_images = imgs
        img = self.carved_images[0]
        self.original_width = img.shape[1]

        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  # 色変換 BGR->RGB
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC) # 見やすさのために2倍に拡大して表示
        height, width, dim = img.shape
        bytesPerLine = dim * width                       # 1行辺りのバイト数

        qimage = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(self.pixmap)

        self.slider.setRange(MIN_WIDTH, self.original_width)         # スライダの値の範囲を設定
        self.slider.setValue(self.original_width) #スライダの初期値を設定
        self.resize(width, height+100)
        self.show()


    def changeImage(self):
        """ スライダの値が変更されたときに呼び出されるメソッド """

        if(self.original_width - self.slider.value() >= len(self.carved_images)): # エラー処理
            return

        """"""""" スライダの値に応じて結果画像を表示する """""""""
        img = self.carved_images[self.original_width - self.slider.value()]
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  # 色変換 BGR->RGB
        height, carved_width, dim = img.shape

        img_ = np.ones((height, self.original_width, dim), np.uint8)*255 # 余白を白く表示
        img_[:,:carved_width,:] = img

        img_ = cv2.resize(img_, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # 見やすさのために2倍に拡大して表示
        height_, width_, dim_ = img_.shape
        bytesPerLine = dim_ * width_     # 1行辺りのバイト数
        qimage = QImage(img_.data, width_, height_, bytesPerLine, QImage.Format_RGB888)
        self.pixmap.convertFromImage(qimage)
        self.label.setPixmap(self.pixmap)

        self.textbox.setText(str(self.slider.value())) #テキストボックスの値を更新



def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    sc = SeamCarving('./arashi.jpg', w)
    QTimer.singleShot(0, sc.carve) # 0ミリ秒後に非同期で実行
    app.exec_()

    output = cv2.imread('output.jpg')
    gr_truth = cv2.imread('ground_truth.jpg')
    print(f'2画像の相関係数: {np.corrcoef(np.vstack([output.reshape(-1), gr_truth.reshape(-1)]))[0, 1]}')


if __name__ == '__main__':
    main()
