import os
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont, QImage, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout

import reader
from models import Section, CellStatus, Teacher


class PhotoViewer(QWidget):
    def __init__(self, image_path, size, parent=None):
        super().__init__(parent)
        self.__size = size
        self.__image = QImage(image_path)

        if self.__image.height() != self.__image.width():
            raise ValueError(f'image {image_path} isnt square image')

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


class TeacherInfoWidget(QWidget):
    def __init__(self, teacher: Teacher, size, parent=None):
        super().__init__(parent)
        self.__size = size

        self.photo_viewer = PhotoViewer(os.path.join('teacher_info', teacher.photo_path), size)
        self.text_viewer = QLabel(teacher.fact + '\n\nПредметы:\n' + "\n".join(teacher.subjects))

        self.text_viewer.setFont(QFont('Ubuntu Mono', size * 0.1))
        self.text_viewer.setAlignment(QtCore.Qt.AlignCenter)

        layout = QHBoxLayout()

        layout.addStretch(1)

        layout.addWidget(self.photo_viewer)
        layout.addWidget(self.text_viewer)

        self.setLayout(layout)

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(250, 205, 140))

        self.setPalette(p)


class GameFieldWidget(QWidget):
    def __init__(self, cell_size, board_size, section: Section, parent=None):
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
                    p.setWidth(self.__cell_size * 0.3)
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


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    section = reader.read_section(sys.argv[1])

    w = GameFieldWidget(100, 20, section)

    # w = TeacherInfoWidget(Teacher('alekseev.png', 'loves cft', ['subject1', 'subject2']), 400)

    w.show()

    # w.setStyleSheet("border: 2px solid red")

    app.exec_()
