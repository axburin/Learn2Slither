from snake import Snake
import random as rd
import tkinter as tk


# Constants

NB_CELLS = 10
CELL_SIZE = 20
GRID_W = NB_CELLS * CELL_SIZE
GRID_H = NB_CELLS * CELL_SIZE

# Helpers

def random_free_cell(occupied):
	"""Return a random (x, y) cell not in occupied."""
	while True:
		x = rd.randint(0, NB_CELLS - 1)
		y = rd.randint(0, NB_CELLS - 1)
		if (x, y) not in occupied:
			return (x, y)

# Drawing

def draw_grid(canvas):
	for i in range(NB_CELLS + 1):
		canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_H, fill="white")
		canvas.create_line(0, i * CELL_SIZE, GRID_W, i * CELL_SIZE, fill="white")

def draw_cell(canvas, x, y, color):
	canvas.create_rectangle(
		x * CELL_SIZE,
		y * CELL_SIZE,
		(x + 1) * CELL_SIZE,
		(y + 1) * CELL_SIZE,
		fill=color,
		outline="",
	)

def draw_snake(canvas, snake):
	for (x, y) in snake.body:
		draw_cell(canvas, x, y, "blue")

def draw_apples(canvas, green1, green2, red):
	draw_cell(canvas, *green1, "green")
	draw_cell(canvas, *green2, "green")
	draw_cell(canvas, *red, "red")

# random

DIRECTIONS = [
	(1,0,),
	(-1,0,),
	(0,1,),
	(0,-1,),
]

def random_snake_body(length=3):
	while True:
		dx, dy = rd.choice(DIRECTIONS)

		x = rd.random(0, NB_CELLS - 1)
		y = rd.randint(0, NB_CELLS - 1)

		body = [(x - i * dx, y - i * dy) for i in range(length)]
		if all(0 <= bx < NB_CELLS and 0 <= by < NB_CELLS for bx, by in body)
			return body


	

# Main

def main():
	snake = Snake([(5, 5), (4, 5), (3, 5)])

	root = tk.Tk()
	root.title("grid")

	canvas = tk.Canvas(root, width=GRID_W, height=GRID_H, bg="black")
	canvas.pack()

	draw_grid(canvas)

	occupied = set()

	occupied.update(snake.body)

	green1 = random_free_cell(occupied)
	occupied.add(green1)

	green2 = random_free_cell(occupied)
	occupied.add(green2)

	red = random_free_cell(occupied)
	occupied.add(red)

	draw_snake(canvas, snake)
	draw_apples(canvas, green1, green2, red)

	root.mainloop()

if __name__ == "__main__":
	main()