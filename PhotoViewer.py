from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QWidget


class PhotoViewer(QWidget):
    def __init__(self, image_path, size, parent=None):
        super().__init__(parent)
        self.__size = size
        self.__image = QImage(image_path)

        # if self.__image.height() != self.__image.width():
        #     raise ValueError(f'image {image_path} isnt square image')

        self.__ratio = self.__size / self.__image.height()

        self.__update_timer = QtCore.QTimer()

        self.__update_timer.timeout.connect(self.update)

        self.__update_timer.start(1000 // 60)

        self.setFixedSize(size, size)

    def paintEvent(self, e) -> None:
        qp = QPainter()
        qp.begin(self)

        qp.save()
        qp.scale(self.__ratio, self.__ratio)
        qp.drawImage(0, 0, self.__image)
        qp.restore()

        qp.end()