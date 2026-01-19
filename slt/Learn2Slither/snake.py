


class Snake :
	def __init__(self, body):
		self.body = body
		self.alive = True


	def head(self):
		return self.body[0]