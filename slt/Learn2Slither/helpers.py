import random as rd
from const import NB_CELLS, DIRECTIONS


def random_free_cell(occupied, nb_cells=NB_CELLS):
    while True:
        x = rd.randint(0, nb_cells - 1)
        y = rd.randint(0, nb_cells - 1)
        if (x, y) not in occupied:
            return (x, y)


def random_snake_body(length=3, nb_cells=NB_CELLS):
    while True:
        dx, dy = rd.choice(DIRECTIONS)
        x = rd.randint(0, nb_cells - 1)
        y = rd.randint(0, nb_cells - 1)
        body = [(x - i * dx, y - i * dy) for i in range(length)]
        in_bounds = all(0 <= bx < nb_cells and 0 <= by < nb_cells
                        for bx, by in body)
        no_duplicates = len(body) == len(set(body))
        if in_bounds and no_duplicates:
            return body
