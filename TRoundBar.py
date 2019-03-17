#!/usr/bin/python
# -*- coding: UTF-8 -*-

from qroundprogressbar import QRoundProgressBar
from PyQt5.QtGui import QIcon, QColor, QPalette, QBrush
from PyQt5.QtCore import *


class TRoundBar(QRoundProgressBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBarStyle(QRoundProgressBar.BarStyle.DONUT)

        palette = QPalette()
        brush = QBrush(QColor(170, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        # 填充进度条区域的背景色
        brush = QBrush(QColor(0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        brush = QBrush(QColor(0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        # 未填充部分背景颜色
        brush = QBrush(QColor(170, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(244, 244, 244))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)

        # brush = QBrush(QColor(50, 100, 150))
        # brush.setStyle(Qt.SolidPattern)
        # palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush)
        # 文本显示所在的中间圆环的背景（为圆环风格）
        brush = QBrush(QColor(50, 100, 150))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush)
        # 设置整个部件的背景（正常情况下，应该设置为：Qt::NoBrush）
        # brush = QBrush()
        # brush.setStyle(Qt.NoBrush)
        # palette.setBrush(QPalette.Active, QPalette.Window, brush)
        # # 未填充进度区域的背景（如果需要透明，应该设置为：Qt::NoBrush）
        # brush = QBrush(QColor(50, 100, 150))
        # brush.setStyle(Qt.SolidPattern)
        # palette.setBrush(QPalette.Base, QPalette.Highlight, brush)
        # # 文本显示所在的中间圆环的背景（为圆环风格）
        # brush = QBrush(QColor(50, 100, 150))
        # brush.setStyle(Qt.SolidPattern)
        # palette.setBrush(QPalette.AlternateBase, QPalette.Highlight, brush)
        # # 未填充区域的前景色（即：边框色）
        # brush = QBrush(QColor(50, 100, 150))
        # brush.setStyle(Qt.SolidPattern)
        # palette.setBrush(QPalette.Shadow, QPalette.Highlight, brush)
        #
        # brush = QBrush(QColor(50, 100, 150))
        # brush.setStyle(Qt.SolidPattern)
        # palette.setBrush(QPalette.Window, QPalette.Highlight, brush)

        self.setPalette(palette)
        # self.resetFormat()
        self.setNullPosition(QRoundProgressBar.PositionTop)
        pass
