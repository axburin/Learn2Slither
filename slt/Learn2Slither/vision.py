
from const import NB_CELLS

def get_vision(snake, apples):
	# construit la vision du snake dans les 4 dir
	apples_map = {a['pos']: a['type'] for a in apples}

	directions = {
		'UP': (0, -1),
		'DOWN': (0, 1),
		'LEFT': (-1, 0),
		'RIGHT': (1, 0),
	}

	vision = {}
	for name, directions in directions.items():
		ray = ['H']
		pos = snake.next_head(directions)

		while not snake.hits_wall(pos, NB_CELLS):
			if snake.hits_self(pos):
				ray.append("S")
			elif pos in apples_map:
				ray.append("G" if apples_map[pos] == 'green' else 'R')
			else:
				ray.append('0')
			x, y = pos
			dx, dy = directions
			pos = (x + dx, y + dy)

		ray.append('W')
		vision[name] = ray

	return(vision)

def print_vision(vision):
	up    = vision['UP'][::-1]    # on inverse : W ... H
	down  = vision['DOWN']        # H ... W
	left  = vision['LEFT'][::-1]  # on inverse : W ... H
	right = vision['RIGHT']       # H ... W

	# largeur du segment gauche (sans le H)
	left_str  = ' '.join(left[:-1])
	right_str = ' '.join(right[1:])
	col = len(left_str) + 1  # position du H sur la ligne

	# colonne du haut (sans le H)
	for cell in up[:-1]:
		print(' ' * col + cell)

	# ligne du milieu
	print(f"{left_str} H {right_str}")

    # colonne du bas (sans le H)
	for cell in down[1:]:
		print(' ' * col + cell)