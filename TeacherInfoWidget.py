import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame, QVBoxLayout

from PhotoViewer import PhotoViewer
from models import Teacher


class TeacherInfoWidget(QWidget):
    def __init__(self, teacher: Teacher, size, parent=None):
        super().__init__(parent)
        self.__size = size

        self.photo_viewer = PhotoViewer(os.path.join('teacher_info', teacher.photo_path), size)
        self.text_viewer = QLabel(teacher.fact + '\n\nПредметы:\n' + "\n".join(teacher.subjects))

        self.text_viewer.setFont(QFont('Ubuntu Mono', size * 0.1))
        self.text_viewer.setAlignment(QtCore.Qt.AlignCenter)

        vlayout = QVBoxLayout()

        self.name = QLabel('<b>' + teacher.name + '</b>')
        self.name.setFont(QFont('Ubuntu Mono', size * 0.11))
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        vlayout.addWidget(self.name)
        vlayout.addSpacerItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        layout = QHBoxLayout()

        layout.addSpacerItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addWidget(self.photo_viewer)
        layout.addSpacerItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addWidget(self.text_viewer)
        layout.addSpacerItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        vlayout.addLayout(layout)

        self.setLayout(vlayout)

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(250, 205, 140))

        self.setPalette(p)

        # self.frame = QFrame(self)
        self.setStyleSheet("border-style: outset; border-width: 6px; border-radius: 10px; border-color: #732125;")
