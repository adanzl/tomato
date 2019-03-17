#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
import threading
import time
from datetime import datetime, timedelta
from TRoundBar import TRoundBar
import random

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from win32com.client import Dispatch
from TConfig import TConfig
from TAnimateNode import TAnimateNode
from TUtil import TUtil

LOCAL_SAVE = {}


class Main(QWidget):
    lbSignal = QtCore.pyqtSignal(QLabel, str)
    icoSignal = QtCore.pyqtSignal(QLabel, QtGui.QPixmap)

    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端
        self.setAutoFillBackground(True)
        self.setWindowTitle("Tomato")

        self.progress = TRoundBar(self)
        self.progress.setDecimals(0)
        gradientPoints = [(0, Qt.green), (0.5, Qt.yellow), (1, Qt.red)]
        self.progress.setDataColors(gradientPoints)
        # self.connectToSlider(self.RoundBar4)

        self.pbLayout.addWidget(self.progress)
        self.progress.installEventFilter(self)
        self.progress.show()

        self.lbSignal.connect(self.updateLabel)
        self.icoSignal.connect(self.updatePic)
        # ICO
        png = QPixmap(TConfig.ANIMATE_LiST[0]['pic'])
        png = png.scaled(TConfig.ICO_WIDTH, TConfig.ICO_HEIGHT, Qt.KeepAspectRatio)
        self.lbIco.setPixmap(png)
        # self.pbLayout.stackUnder(self.icoBox)
        self.icoBox.installEventFilter(self)

        self.lbBox.installEventFilter(self)
        # Label music name
        self.lbMusic.installEventFilter(self)

        # Label MSG
        self.lbMsg.installEventFilter(self)

        # Label Time
        self.lbTime.installEventFilter(self)

        # Button Frame
        self.bBox.installEventFilter(self)
        # Daily Statistic
        self.lbTodayCount.installEventFilter(self)

        # Pause Button
        self.btnPauseOrContinue.setText("-")
        self.btnPauseOrContinue.clicked.connect(self.PauseOrContinue)

        # Reset Button
        self.btnReset.setText('\u21BA')
        self.btnReset.clicked.connect(self.Reset)

        # Close Button
        self.btnClose.clicked.connect(self.Close)

        self.timer = threading.Timer(1.0, self.TimeCB)
        self.timer.start()
        self.timerCounting = False

        self.animate = TAnimateNode(self, self.icoBox, 'rotation')
        # self.animate.Start()

        # load save
        global LOCAL_SAVE
        LOCAL_SAVE = TUtil.LoadSave()
        self.RefreshUI()

        self.mediaPlayer = Dispatch("WMPlayer.OCX")
        return

    def eventFilter(self, obj, event):
        if type(obj) != QPushButton:
            if event.type() == QEvent.MouseMove:
                if event.buttons() == Qt.LeftButton:
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()
            elif event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
                    QApplication.postEvent(self, QEvent(174))
                    event.accept()
        return False

    def Show(self):
        self.StartTask(0)
        self.show()
        return

    def Close(self):
        self.timer.cancel()
        self.animate.Stop()
        QCoreApplication.instance().quit()
        return

    def StartCounter(self, msg, time):
        self.timerCounting = True
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now() + timedelta(seconds=time)
        self.lbMsg.setText(msg)
        return

    def PauseOrContinue(self):
        if self.timerCounting:
            self.mediaPlayer.controls.pause()
            self.animate.Pause()
        else:
            self.mediaPlayer.controls.play()
            self.animate.Continue()
        self.timerCounting = not self.timerCounting
        self.RefreshUI()
        return

    def Reset(self):
        self.timerCounting = False
        self.timeEnd = datetime.now()
        self.StartTask(0)
        return

    def updateLabel(self, obj, text):
        obj.setText(text)
        return

    def updatePic(self, obj, pic):
        obj.setPixmap(pic)
        return

    def TimeCB(self):

        if self.timerCounting:
            if self.timeEnd > datetime.now():
                timeRemain = (self.timeEnd - datetime.now()).total_seconds()
                m, s = divmod(timeRemain, 60)
                h, m = divmod(m, 60)
                tStr = TUtil.BuildTimeStr("%02d:%02d:%02d" % (h, m, s))
                self.lbSignal.emit(self.lbTime, tStr)
                p = timeRemain / (self.timeEnd - self.timeStart).total_seconds()
                # print( str(p))
                self.progress.setValue(p * 100)
            else:
                self.StartTask(self.currentTaskId + 1)
        self.lbMusic.setText(self.mediaPlayer.currentMedia.name)
        self.timer = threading.Timer(0.1, self.TimeCB)
        self.timer.start()
        return

    def StartTask(self, taskId):
        self.mediaPlayer.controls.stop()
        self.mediaPlayer.currentPlaylist.clear()
        self.currentTaskId = taskId % len(TConfig.TASK_LIST)
        taskNode = TConfig.TASK_LIST[self.currentTaskId]
        if taskNode['type'] == TConfig.T_TASK_WORK:
            iList = [0]
            duration = taskNode["duration"]
            self.mediaPlayer.currentPlaylist.appendItem(self.mediaPlayer.newMedia(taskNode["music"][0]))
        elif taskNode['type'] == TConfig.T_TASK_REST:
            iList = random.sample(range(0, len(taskNode["music"]) - 1), taskNode["count"])
            duration = 0
            for v in iList:
                m = self.mediaPlayer.newMedia(taskNode["music"][v])
                duration += m.duration
                self.mediaPlayer.currentPlaylist.appendItem(m)
                pass
        else:
            duration = 1

        self.lbMusic.setText(self.mediaPlayer.currentMedia.name)
        self.mediaPlayer.settings.playCount = 999
        self.mediaPlayer.controls.play()
        self.StartCounter(TUtil.BuildMsgStr(taskNode["msg"]), duration)
        # 默认认为最后一个任务为休息任务
        if self.currentTaskId == len(TConfig.TASK_LIST) - 1:
            key = time.strftime("%Y-%m-%d")
            todayCount = LOCAL_SAVE.get(key, 0) + 1
            print("tomato + 1 Today: [%d]" % todayCount)
            LOCAL_SAVE[key] = todayCount
            TUtil.SaveLocal(LOCAL_SAVE)

        self.RefreshUI()
        return

    def RefreshUI(self):
        key = time.strftime("%Y-%m-%d")
        self.lbTodayCount.setText("今日番茄[%d]" % (LOCAL_SAVE.get(key, 0)))

        if self.timerCounting:
            self.btnPauseOrContinue.setText("II")
        else:
            self.btnPauseOrContinue.setText(">")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.Show()
    sys.exit(app.exec_())
