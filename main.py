import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QLabel

import reader
from GameFieldWidget import GameFieldWidget
from TeacherInfoWidget import TeacherInfoWidget
from models import Section, Teacher

GAME_FIELD_SIZE = 150
GAME_FIELD_BOARD_SIZE = 30
TEACHER_INFO_SIZE = 600


class MainWidget(QWidget):
    def __init__(self, section: Section):
        super().__init__()

        self.__screen_size = QDesktopWidget().screenGeometry(-1)

        self.__title = QLabel(section.title, self)
        self.__title.setFont(QFont('Ubuntu Mono', self.__screen_size.height() * 0.08))
        self.__title.move(self.__screen_size.width() / 2 - 200, self.__title.height() - 20)
        self.__title.show()

        self.__field = GameFieldWidget(GAME_FIELD_SIZE, GAME_FIELD_BOARD_SIZE, section, self.show_teacher_info, self)
        self.__field.move(self.__screen_size.center() - self.__field.rect().center())

        self.__current_teacher_widget = None

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(250, 205, 140))

        self.setPalette(p)

    def mousePressEvent(self, _) -> None:
        if self.__current_teacher_widget is None:
            return

        self.__current_teacher_widget.setParent(None)
        self.__current_teacher_widget = None
        self.__field.show()

    def show_teacher_info(self, teacher: Teacher):
        self.__current_teacher_widget = TeacherInfoWidget(teacher, TEACHER_INFO_SIZE, self)

        self.__field.hide()
        # magic constants from actual TeacherInfoWidgetSize
        self.__current_teacher_widget.show()
        self.__current_teacher_widget.move(
            self.__screen_size.center() - self.__current_teacher_widget.rect().center())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    section = reader.read_section(sys.argv[1])

    w = MainWidget(section)

    w.showMaximized()

    app.exec_()
