import sys

from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication

import reader
from models import Section, CellStatus


class CommInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class GameFieldWidget(QWidget):
    def __init__(self, cell_size, board_size, section: Section, parent=None):
        super().__init__(parent)

        self.__cell_size = cell_size
        self.__board_size = board_size
        self.__section = section

        self.setFixedSize(cell_size * 5 + board_size * 2, cell_size * 5 + board_size * 2)

        self.__figures_image = QPixmap('resources/figures.png')

        self.__white = QColor(94, 85, 71)
        self.__red = QColor(45, 12, 12)
        self.__black = QColor(71, 52, 38)

    def paintEvent(self, e) -> None:
        qp = QPainter()
        qp.begin(self)
        self._draw_screen(qp)
        qp.end()

    def _draw_screen(self, qp: QPainter):
        qp.fillRect(0, 0, self.width(), self.height(), self.__red)
        qp.fillRect(self.__board_size,
                    self.__board_size,
                    self.__cell_size * 5,
                    self.__cell_size * 5,
                    self.__white)

        qp.setPen(self.__white)

        qp.setFont(QFont('Ubuntu Mono', self.__cell_size * 0.2))

        for i, l in enumerate(['a', 'b', 'c', 'd', 'e']):
            qp.drawText(self.__board_size + self.__cell_size * i + self.__cell_size * 0.4,
                        self.__board_size * 0.7 + self.__cell_size * 5,
                        self.__cell_size,
                        self.__cell_size,
                        0,
                        l)

        for i in range(5):
            qp.drawText(0,
                        self.__board_size + self.__cell_size * i + self.__cell_size * 0.3,
                        self.__cell_size,
                        self.__cell_size,
                        0,
                        str(6 - i - 1))

        for y in range(5):
            for x in range(5):
                if (y + x) % 2 == 0:  # black cell
                    qp.fillRect(x * self.__cell_size + self.__board_size,
                                y * self.__cell_size + self.__board_size,
                                self.__cell_size,
                                self.__cell_size,
                                self.__black)

                cell = self.__section.field.get_cell_in(4 - y, x)

                if cell is None:
                    continue

                if cell.status == CellStatus.OPEN:
                    continue

                color = cell.figure.color
                rank = cell.figure.rank

                qp.save()

                ratio = self.__cell_size / 132

                qp.scale(ratio, ratio)

                qp.drawPixmap((x * self.__cell_size + self.__board_size) / ratio,
                              (y * self.__cell_size + self.__board_size) / ratio,
                              self.__figures_image,
                              int(rank) * 132,
                              int(color) * 132,
                              132,
                              132)

                qp.restore()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    section = reader.read_section(sys.argv[1])

    w = GameFieldWidget(100, 20, section)

    w.show()

    app.exec_()
