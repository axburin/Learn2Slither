import random as rd
from const import NB_CELLS, DIRECTIONS


def random_free_cell(occupied):
	"""Return a random (x, y) cell not in occupied."""
	while True:
		x = rd.randint(0, NB_CELLS - 1)
		y = rd.randint(0, NB_CELLS - 1)
		if (x, y) not in occupied:
			return (x, y)


def random_snake_body(length=3):
	"""Generate a random valid snake body within bounds."""
	while True:
		dx, dy = rd.choice(DIRECTIONS)
		x = rd.randint(0, NB_CELLS - 1)
		y = rd.randint(0, NB_CELLS - 1)
		body = [(x - i * dx, y - i * dy) for i in range(length)]
		in_bounds     = all(0 <= bx < NB_CELLS and 0 <= by < NB_CELLS for bx, by in body)
		no_duplicates = len(body) == len(set(body))
		if in_bounds and no_duplicates:
			return body