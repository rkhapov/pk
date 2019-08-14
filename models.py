import enum
from typing import List, Union


class Teacher:
    def __init__(self, name, photo_path, fact, subjects):
        self.__name = name
        self.__photo_path = photo_path
        self.__fact = fact
        self.__subjects = subjects

    @property
    def name(self):
        return self.__name

    @property
    def photo_path(self):
        return self.__photo_path

    @property
    def fact(self):
        return self.__fact

    @property
    def subjects(self):
        return self.__subjects


# numeration is important for figures drawing
class Rank(enum.IntEnum):
    KING = 4
    QUEEN = 3
    ROOK = 0
    BISHOP = 2
    HORSE = 1
    PAWN = 5


# numeration is important for figures drawing
class Color(enum.IntEnum):
    BLACK = 1
    WHITE = 0


class Figure:
    def __init__(self, rank: Rank, color: Color, teacher: Teacher, position: str):
        self.__rank = rank
        self.__color = color
        self.__teacher = teacher
        self.__position = position

    @property
    def rank(self):
        return self.__rank

    @property
    def color(self):
        return self.__color

    @property
    def teacher(self):
        return self.__teacher

    @property
    def position(self):
        return self.__position


class CellStatus(enum.IntEnum):
    OPEN = 0,
    CLOSE = 1


class Cell:
    def __init__(self, figure: Figure):
        self.__figure = figure
        self.__state = CellStatus.CLOSE

    def open(self):
        self.__state = CellStatus.OPEN

    @property
    def figure(self):
        return self.__figure

    @property
    def status(self):
        return self.__state


def string_to_cord(s: str):
    if len(s) != 2:
        raise ValueError('unknown format of cord')

    return int(s[1]) - 1, (ord(s[0]) - ord('a'))


class Field:
    def __init__(self, nonempty_cells: List[Cell]):
        self.__cord_to_cell = {string_to_cord(cell.figure.position): cell for cell in nonempty_cells}
        self.__nonempty = nonempty_cells

    def get_cell_in(self, y, x) -> Union[Cell, None]:
        c = y, x

        if c in self.__cord_to_cell:
            return self.__cord_to_cell[c]

        return None

    def __iter__(self):
        return iter(self.__nonempty)


class Section:
    def __init__(self, title: str, field: Field):
        self.__title = title
        self.__field = field

    @property
    def title(self):
        return self.__title

    @property
    def field(self):
        return self.__field
