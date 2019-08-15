import os

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont, QPen
from PyQt5.QtWidgets import QWidget

from models import Section, CellStatus


class GameFieldWidget(QWidget):
    def __init__(self, cell_size, board_size, section: Section, show_teacher_info, parent=None):
        super().__init__(parent)

        self.__cell_size = cell_size
        self.__board_size = board_size
        self.__section = section

        self.setFixedSize(cell_size * 5 + board_size * 2, cell_size * 5 + board_size * 2)

        self.__figures_image = QPixmap(os.path.join('resources', 'figures.png'))

        self.__white = QColor(240, 218, 181)
        self.__red = QColor(115, 33, 37)
        self.__black = QColor(181, 135, 99)

        self.__teacher_to_image = {t: QPixmap(os.path.join('teacher_info', t.photo_path)) for t in
                                   map(lambda c: c.figure.teacher, list(section.field))}

        self.__update_timer = QtCore.QTimer()

        self.__update_timer.timeout.connect(self.update)

        self.__update_timer.start(1000 // 60)

        self.__show_teacher_info = show_teacher_info

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

        qp.setFont(QFont('Ubuntu Mono', self.__cell_size * 0.35))

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

        for y in range(5):
            for x in range(5):
                cell = self.__section.field.get_cell_in(4 - y, x)

                if cell is None:
                    continue

                if cell.status == CellStatus.OPEN:
                    qp.save()

                    teacher_image = self.__teacher_to_image[cell.figure.teacher]

                    width = teacher_image.width()

                    ratio = self.__cell_size / width

                    qp.scale(ratio, ratio)

                    qp.drawPixmap(
                        (x * self.__cell_size + self.__board_size) / ratio,
                        (y * self.__cell_size + self.__board_size) / ratio,
                        teacher_image,
                        0,
                        0,
                        width,
                        width)

                    p = QPen(QColor(0, 0, 0))
                    p.setWidth(self.__cell_size * 0.2)
                    qp.setPen(p)

                    qp.drawRect(
                        (x * self.__cell_size + self.__board_size) / ratio,
                        (y * self.__cell_size + self.__board_size) / ratio,
                        width, width
                    )

                    qp.restore()

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

    def mousePressEvent(self, e):
        x = e.x()
        y = e.y()

        if x < self.__board_size or x > self.width() - self.__board_size:
            return

        if y < self.__board_size or y > self.height() - self.__board_size:
            return

        x -= self.__board_size
        y -= self.__board_size

        x //= self.__cell_size
        y //= self.__cell_size

        y = 4 - y

        cell = self.__section.field.get_cell_in(y, x)

        if cell is None or cell.status == CellStatus.OPEN:
            return

        cell.open()

        self.__show_teacher_info(cell.figure.teacher)
