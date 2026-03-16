import tkinter as tk
from const import GRID_W, GRID_H, NB_CELLS, KEY_BINDINGS, OPPOSITES
from helpers  import random_snake_body, random_free_cell
from drawing  import draw_grid, draw_cell
from snake    import Snake
from vision import get_vision, print_vision
from agent import Agent


class Game:
	"""Main game controller."""

	def __init__(self, root):
		self.root = root
		self.root.title("Learn2Slither")

		self.canvas = tk.Canvas(root, width=GRID_W, height=GRID_H, bg="grey")
		self.canvas.pack()

		self.snake = None
		self.apples = []
		self.occupied = set()
		self.direction = (0, 1)
		self.agent = Agent()

		self.root.bind("<KeyPress>", self._on_key)
		self._init_game()

	# ── Setup ─────────────────────────────────────────────────────────────────

	def _init_game(self):
		"""Initialize snake and apples."""
		snake_body = random_snake_body()
		self.snake = Snake(snake_body)
		self.occupied.update(self.snake.body)

		for apple_type, count in [('green', 2), ('red', 1)]:
			for _ in range(count):
				self._spawn_apple(apple_type)

		self.draw()

	def _spawn_apple(self, apple_type):
		"""Spawn a new apple of given type on a free cell."""
		occupied = set(self.snake.body) | {a['pos'] for a in self.apples}
		pos = random_free_cell(occupied)
		self.occupied.add(pos)
		self.apples.append({'type': apple_type, 'pos': pos})

	# ── Input ─────────────────────────────────────────────────────────────────

	def _on_key(self, event):
		"""Handle keyboard input to change direction."""
		new_dir = KEY_BINDINGS.get(event.keysym)
		if new_dir and new_dir != OPPOSITES.get(self.direction):
			self.direction = new_dir

	# ── Drawing ───────────────────────────────────────────────────────────────

	def draw(self):
		"""Redraw the entire game state."""
		self.canvas.delete("all")
		draw_grid(self.canvas)

		for (x, y) in self.snake.body:
			draw_cell(self.canvas, x, y, "blue")

		for apple in self.apples:
			color = "green" if apple['type'] == 'green' else "red"
			draw_cell(self.canvas, *apple['pos'], color)

	# ── Logic ─────────────────────────────────────────────────────────────────

	def _handle_apple(self, apple_index):
		"""Apply the effect of eating an apple."""
		apple = self.apples[apple_index]

		if apple['type'] == 'green':
			self.snake.body.append(self.snake.body[-1])  # grow
		elif apple['type'] == 'red':
			if len(self.snake.body) > 1:
				self.snake.body.pop()                    # shrink

		self.occupied.discard(apple['pos'])
		self.apples.pop(apple_index)
		self._spawn_apple(apple['type'])

	def move_snake(self):
		"""Move the snake and handle apple collisions."""
		self.snake.move(self.direction)

		apple_index = self.snake.hits_apples(self.apples)
		if apple_index is not None:
			self._handle_apple(apple_index)

		self.draw()

	def _game_over(self, reason):
		"""Stop the game and print the reason."""
		print(f"Game Over : {reason}")
		self.root.destroy()

	# ── Game loop ─────────────────────────────────────────────────────────────

	def autoplay(self):
		"""Main game loop: check collisions, move, repeat."""
		if len(self.snake.body) == 0:
			self._game_over("le snake a disparu")
			return
		
		if self.snake.hits_wall(self.snake.next_head(self.direction), NB_CELLS):
			self._game_over("le snake a touché un mur")
			return
		if self.snake.hits_self():
			self._game_over("le snake s'est mordu")
			return
		
		vision = get_vision(self.snake, self.apples)
		print_vision(vision)
		action = self.agent.get_action(vision)
		self.direction = KEY_BINDINGS[action]
		self.move_snake()
		self.root.after(200, self.autoplay)