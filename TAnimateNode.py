#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from datetime import datetime, timedelta
from qroundprogressbar import QRoundProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QTransform
from PyQt5.QtCore import *
from TConfig import TConfig


class TAnimateNode():
    def __init__(self, parent, obj, type):
        self.parent = parent
        self.picObj = obj
        self.type = type
        self.playing = False
        self.startTime = datetime.now()
        return

    def Start(self):
        self.Reset()

        self.timer = threading.Timer(1.0, self.TimeCB)
        self.timer.start()
        self.playing = True
        self.startTime = datetime.now()
        return

    def Pause(self):
        self.playing = False
        return

    def Continue(self):
        self.playing = True
        return

    def Stop(self):
        if self.playing:
            self.timer.cancel()
        self.startTime = datetime.now()
        return

    def Reset(self):
        self.playing = False
        self.setPic(0)
        return

    def setPic(self, index):
        self.timeEnd = datetime.now() + timedelta(seconds=5)
        self.picIndex = index % len(TConfig.ANIMATE_LiST)
        png = QPixmap(TConfig.ANIMATE_LiST[self.picIndex]['pic'])
        png = png.scaled(TConfig.ICO_WIDTH, TConfig.ICO_HEIGHT, Qt.KeepAspectRatio)
        self.parent.icoSignal.emit(self.picObj, png)
        return

    def rotatePic(self):
        self.timeEnd = datetime.now() + timedelta(seconds=1)
        ts = datetime.now() - self.startTime
        angle = 360 / 60 * ts.total_seconds() % 360
        png = self.picObj.pixmap()
        png = QPixmap('8.png')
        png = png.scaled(TConfig.ICO_WIDTH, TConfig.ICO_HEIGHT, Qt.KeepAspectRatio)
        png = png.transformed(QTransform().rotate(angle))
        # self.parent.icoSignal.emit(self.picObj, png)
        self.picObj.setPixmap(png)

    def update(self):
        if self.type == 'list':
            self.setPic(self.picIndex + 1)
        elif self.type == 'rotation':
            self.rotatePic()
        print('time remain ' + str((self.timeEnd - datetime.now()).total_seconds()))
        return

    def TimeCB(self):

        if self.playing:
            if self.timeEnd > datetime.now():
                self.update()

        self.timer = threading.Timer(0.1, self.TimeCB)
        self.timer.start()
        return
