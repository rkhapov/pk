import json
import os
from typing import Type

from models import *


def _to_value_of_enum(s: str, e: Type[enum.Enum]):
    for v in list(e):
        if v.name.lower() == s.lower():
            return v


def _read_teacher(name) -> Teacher:
    with open(os.path.join('teacher_info', name + '.json'), 'r') as file:
        text = file.read()
        d = json.loads(text)

        return Teacher(d['photo'], d['fact'], d['subjects'])


def _to_figure(f) -> Figure:
    rank = _to_value_of_enum(f['rank'], Rank)
    color = _to_value_of_enum(f['color'], Color)
    teacher = _read_teacher(f['teacher'])
    position = f['position']

    return Figure(rank, color, teacher, position)


def _to_cell(f) -> Cell:
    return Cell(_to_figure(f))


def _read_cells_list(figures_list) -> List[Cell]:
    cells = []

    for f in figures_list:
        cells.append(_to_cell(f))

    return cells


def _parse_text(text) -> Section:
    d = json.loads(text)

    title = d['title']
    cells = _read_cells_list(d['figures'])

    field = Field(cells)

    return Section(title, field)


def read_section(filename) -> Section:
    with open(os.path.join('sections', filename + '.json'), 'r') as file:
        text = file.read()

        return _parse_text(text)
