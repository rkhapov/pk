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
        layout.addLayout(self._get_info_layout(teacher, size))
        layout.addSpacerItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        vlayout.addLayout(layout)

        vlayout.addSpacerItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(250, 205, 140))

        self.setPalette(p)

        container = QWidget(self)
        container.setLayout(vlayout)

        frame = QFrame(container)
        frame.setStyleSheet("border-style: outset; border-width: 6px; border-radius: 10px; border-color: #732125;")

        container.show()
        frame.setFixedSize(container.size())

    def _get_info_layout(self, teacher: Teacher, size):
        self.facts_viewer = QLabel(teacher.fact)
        self.facts_viewer.setWordWrap(True)
        self.facts_viewer.setFont(QFont('Ubuntu Mono', size * 0.06))
        self.facts_viewer.setAlignment(QtCore.Qt.AlignCenter)

        self.subjects_viewer = QLabel('<b>Предметы:</b><br>' + "<br>".join(teacher.subjects))
        self.subjects_viewer.setFont(QFont('Ubuntu Mono', size * 0.06))
        self.subjects_viewer.setAlignment(QtCore.Qt.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(self.facts_viewer)
        layout.addWidget(self.subjects_viewer)

        return layout

