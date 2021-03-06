from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject, pyqtSignal
import settings

from PyQt4.QtCore import pyqtSignal, QSize, Qt
from PyQt4.QtGui import *


class MimeGenerator(QObject):
    signalItemDragged = pyqtSignal(str, name='itemDragged')

    def __init__(self, parent):
        super(MimeGenerator, self).__init__(parent=parent)
        self.parent = parent
        self.signalItemDragged.connect(self.itemDragged)
        self.text = ""
        pass

    def itemDragged(self, itemID):
        print "Dragged"
        self.metaData = settings.pathCache[
            settings.currentCategory][str(itemID)]
        self.category = settings.currentCategory
        self.itemID = str(itemID)  # might be QString

        drag = QtGui.QDrag(self.parent)
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.generateNukeTCL())
        drag.setMimeData(mimeData)

        drag.setPixmap(QtGui.QPixmap.fromImage(self.createPixmap()))
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def generateNukeTCL(self):
        formatStr = "{} {} 1".format(
            self.metaData['width'], self.metaData['height'])
        sourcePath = settings.sourcePath(self.category, self.itemID)
        proxyPath = settings.proxyPath(self.category, self.itemID)
        command = ""
        command += """Read {{
            inputs 0
            file \"{4}\"
            proxy \"{5}\"
            origfirst {0}
            origlast {1}
            first {0}
            last {1}
            format \"{2}\"
            proxy_format \"{2}\"
            label \"ElementsbrowserID# {3}\"
            }}""".format(self.metaData['startFrame'],
                         self.metaData['startFrame'] +
                         self.metaData['numOfFrames'],
                         formatStr,
                         self.metaData['id'],
                         sourcePath,
                         proxyPath)
        return command

    def createPixmap(self):
        """Creates the pixmap shown when this label is dragged."""
        font_metric = QtGui.QFontMetrics(QtGui.QFont())
        text_size = font_metric.size(QtCore.Qt.TextSingleLine, self.text)
        image = QtGui.QImage(text_size.width() + 4, text_size.height() + 4,
                             QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.qRgba(240, 140, 120, 255))

        painter = QtGui.QPainter()
        painter.begin(image)
        painter.setFont(QtGui.QFont())
        painter.setBrush(QtCore.Qt.black)
        painter.drawText(QtCore.QRect(QtCore.QPoint(2, 2), text_size), QtCore.Qt.AlignCenter,
                         self.text)
        painter.end()
        return image
