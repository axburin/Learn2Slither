from const import NB_CELLS, CELL_SIZE, GRID_H


def draw_grid(canvas):
	"""Draw the game grid lines."""
	for i in range(NB_CELLS + 1):
		canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_H, fill="white")
		canvas.create_line(0, i * CELL_SIZE, GRID_H, i * CELL_SIZE, fill="white")


def draw_cell(canvas, x, y, color):
	"""Draw a single filled cell."""
	canvas.create_rectangle(
		x * CELL_SIZE,
		y * CELL_SIZE,
		(x + 1) * CELL_SIZE,
		(y + 1) * CELL_SIZE,
		fill=color,
		outline="",
	)