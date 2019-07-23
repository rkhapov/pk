import sys

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication


class CommInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class GameFieldWidget(QWidget):
    def __init__(self, cell_height, cell_width, parent=None):
        super().__init__(parent)
        self.__cell_height = cell_height
        self.__cell_width = cell_width

    def paintEvent(self, e) -> None:
        qp = QPainter()
        qp.begin(self)
        self._draw_screen(qp)
        qp.end()

    def _draw_screen(self, qp: QPainter):
        qp.drawText(10, 10, 'LOOOH')


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    # sys.argv[1] - name of target json

    app = QApplication(sys.argv)

    w = GameFieldWidget(10, 10)

    w.showMaximized()

    app.exec_()
