# -*- coding: utf-8 -*-
#!/usr/bin/env python3.8
"""
Created on Sun Dic 15 16:30:35 2019
HAAR画像検出
URL: https://github.com/wakame-tech/vendredi-noir/blob/master/src/gui/haar.py
@author: n_toba
@id: 4617054
"""
import cv2

class ObjDetector(object):
    """ 物体検出器 """
    def __init__(self, filename = None):
        # カスケード分類器の初期化
        self.cascade = cv2.CascadeClassifier()  # カスケード識別器のインスタンスを作成
        if filename != None:
            self.cascade.load(filename) # モデルファイルを読み込み
    
    def load(self, filename):
        self.cascade.load(filename)
        if self.cascade.empty():
            raise IOError(f'error in loading cascade file "{filename}"')
        
    def detect(self, im):

        if self.cascade.empty():
            return False

        scalefactor = 1.1
        minneighbors = 3
        return len(self.cascade.detectMultiScale(im, scaleFactor=scalefactor, minNeighbors=minneighbors)) > 0

