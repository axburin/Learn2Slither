import random

class Agent:

	def get_action(self, vision):
		return random.choice(['Up', 'Down', 'Left', 'Right'])