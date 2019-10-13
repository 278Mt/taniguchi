#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:32:05 2019

@author: 278mt
"""

import cv2
from matplotlib import pyplot as plt
import numpy as np


class Graph(object):
    
    def __init__(self, fname: str):
        
        self.im = cv2.imread(fname)[:, :, ::-1]
        self.filt = np.zeros_like(self.im)
        self.fname = fname
        
        
    def imshow(self, im: np.ndarray):
        
        plt.imshow(im)
        plt.show()
        
        
    def imsave(self, im: np.ndarray, fname: str=None):
        
        if fname is None:
            fname = self.fname.replace('.', '_res.')
            
        cv2.imwrite(fname, im[:, :, ::-1])

        
    def laplacian(self):
        
        lap_im = cv2.Laplacian(self.im, cv2.CV_32F)
        self.lap_im = lap_im
        
        
    def filtering(self, point: tuple):
        
        if (self.lap_im[point[::-1]] > 0).any():
            return
        
        filt = self.lap_im.copy()
        filt[filt <= 0] = 0
        filt[filt > 0] = 255
        filt[filt.sum(axis=2) > 0] = 255

        # 塗りつぶしに関する
        # http://pynote.hatenablog.com/entry/opencv-flood-fill
        mask = np.zeros(np.array(filt.shape[:2], dtype=np.uint) + 2, dtype=np.uint8)
        fl = cv2.floodFill(filt[:, :, 0], mask, point, 127)
        pre_filt = fl[1].get()
        for i in range(3):
            filt[:, :, i] = pre_filt
                
        filt[filt != 127] = 0
        filt[filt == 127] = 255
        
        # 近傍編集に関する
        # https://www.blog.umentu.work/python-opencv3%E3%81%A7%E7%94%BB%E7%B4%A0%E3%81%AE%E8%86%A8%E5%BC%B5%E5%87%A6%E7%90%86dilation%E3%81%A8%E5%8F%8E%E7%B8%AE%E5%87%A6%E7%90%86erosion-%E3%81%A1%E3%82%87%E3%81%A3%E3%81%A8%E8%A7%A3/
        nb = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]], np.uint8)
        
        # 8近傍で膨張処理
        filt = cv2.dilate(filt, nb, iterations=1)

        self.filt |= filt.astype(np.uint8)


    def inpainting(self):
        
        dst = np.zeros_like(self.filt)
        for i in range(3):
            dst[:, :, i] = cv2.inpaint(self.im[:, :, i], self.filt[:, :, i], 3, cv2.INPAINT_TELEA)
        
        self.dst = dst
        


if __name__ == '__main__':
    
    fname = 'sample_im.png'
    xg = Graph(fname)
    xg.imshow(xg.im)
    xg.laplacian()
    xg.imshow(xg.lap_im)
    points = [(5, 5), (30, 155), (300, 195), (315, 200), (105, 107), (200, 125)]
    for point in points:        
        xg.filtering(point=point)
        xg.imshow(xg.filt)

    xg.inpainting()
    xg.imshow(xg.dst)
    xg.imsave(xg.dst)
