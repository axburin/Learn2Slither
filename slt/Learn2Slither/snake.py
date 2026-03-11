


class Snake :
	def __init__(self, body):
		self.body = body
		self.alive = True

	def head(self):
		return self.body[0]
	
	def next_head(self, direction):
		head_x, head_y = self.head()
		dx, dy = direction
		return(head_x + dx, head_y + dy)
	
	def move(self, direction):
		new_head = tuple(p + d for p, d in zip(self.body[0], direction))
		self.body.insert(0, new_head)
		self.body.pop()

	def hits_wall(self, pos, board_size):
		x, y = pos
		return not (0 <= x < board_size and 0 <= y < board_size)

	def hits_self(self, pos=None):
		if pos is None:
			pos = self.head()
		return pos in self.body[1:]

	def hits_apples(self, apples):
		head = self.head()
		for i, apple in enumerate(apples):
			if apple["pos"] == head:
				return i
		return None