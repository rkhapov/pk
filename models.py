import enum


class Teacher:
    def __init__(self, photo_path, fact, subjects):
        self.__photo_path = photo_path
        self.__fact = fact
        self.__subjects = subjects

    @property
    def photo_path(self):
        return self.__photo_path

    @property
    def fact(self):
        return self.__fact

    @property
    def subjects(self):
        return self.__subjects


class CellStatus(enum.IntEnum):
    OPEN = 0,
    CLOSE = 1


class Cell:
    pass


class Field:
    pass
