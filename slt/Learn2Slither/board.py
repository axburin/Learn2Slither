from snake import Snake
import random as rd
import tkinter as tk


# Constants

NB_CELLS = 10
CELL_SIZE = 20
GRID_W = NB_CELLS * CELL_SIZE
GRID_H = NB_CELLS * CELL_SIZE

DIRECTIONS = [
	(1, 0),
	(-1, 0),
	(0, 1),
	(0, -1),
]

ACTIONS = {
	0: (0, -1),   # UP
	1: (-1, 0),   # LEFT
	2: (0, 1),    # DOWN
	3: (1, 0),    # RIGHT
}

# Helpers

def random_free_cell(occupied):
	"""Return a random (x, y) cell not in occupied."""
	while True:
		x = rd.randint(0, NB_CELLS - 1)
		y = rd.randint(0, NB_CELLS - 1)
		if (x, y) not in occupied:
			return (x, y)


def random_snake_body(length=3):
	"""Generate a random snake body within bounds."""
	while True:
		dx, dy = rd.choice(DIRECTIONS)
		x = rd.randint(0, NB_CELLS - 1)
		y = rd.randint(0, NB_CELLS - 1)

		body = [(x - i * dx, y - i * dy) for i in range(length)]
		if all(0 <= bx < NB_CELLS and 0 <= by < NB_CELLS for bx, by in body):
			return body


# Drawing

def draw_grid(canvas):
	"""Draw the game grid."""
	for i in range(NB_CELLS + 1):
		canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_H, fill="white")
		canvas.create_line(0, i * CELL_SIZE, GRID_W, i * CELL_SIZE, fill="white")


def draw_cell(canvas, x, y, color):
	"""Draw a single cell."""
	canvas.create_rectangle(
		x * CELL_SIZE,
		y * CELL_SIZE,
		(x + 1) * CELL_SIZE,
		(y + 1) * CELL_SIZE,
		fill=color,
		outline="",
	)

def erase_cell(canvas, x, y, color):
	canvas.create_rectangle(
		x * CELL_SIZE,
		y * CELL_SIZE,
		(x + 1) * CELL_SIZE,
		(y + 1 * CELL_SIZE),
		fill=None,
		outline="",
	)


# Game Class

class Game:
	"""Main game controller."""

	def __init__(self, root):
		self.root = root
		self.root.title("Learn2Slither")

		self.canvas = tk.Canvas(root, width=GRID_W, height=GRID_H, bg="grey")
		self.canvas.pack()

		self.snake = None
		self.apples = []  # List of dicts: {'type': 'green'/'red', 'pos': (x, y)}
		self.occupied = set()

		self.direction = (1, 0)

		self._init_game()

	def _init_game(self):
		"""Initialize snake and apples."""
		draw_grid(self.canvas)

		# Create snake
		snake_body = random_snake_body()
		self.snake = Snake(snake_body)
		self.occupied.update(self.snake.body)

		# Create apples: 2 green, 1 red
		apple_config = [
			{'type': 'green', 'count': 2},
			{'type': 'red', 'count': 1},
		]

		for config in apple_config:
			for _ in range(config['count']):
				pos = random_free_cell(self.occupied)
				self.occupied.add(pos)
				self.apples.append({'type': config['type'], 'pos': pos})
		self.draw()

	def draw(self):
		"""Redraw the entire game state."""
		self.canvas.delete("all")
		draw_grid(self.canvas)

		# Draw snake
		for (x, y) in self.snake.body:
			draw_cell(self.canvas, x, y, "blue")

		# Draw apples
		for apple in self.apples:
			color = "green" if apple['type'] == 'green' else "red"
			x, y = apple['pos']
			draw_cell(self.canvas, x, y, color)

	def move_snake(self):
		self.snake.move(self.direction)
		self.draw()
		
	def autoplay(self):
		self.move_snake()
		self.root.after(200, self.autoplay)
		


# Main

def main():
	root = tk.Tk()
	game = Game(root)
	game.autoplay()
	root.mainloop()
	

if __name__ == "__main__":
	main()