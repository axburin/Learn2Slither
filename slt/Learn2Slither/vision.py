from const import NB_CELLS


def get_vision(snake, apples, nb_cells=NB_CELLS):
    apples_map = {a['pos']: a['type'] for a in apples}

    dir_map = {
        'UP':    (0, -1),
        'DOWN':  (0,  1),
        'LEFT':  (-1, 0),
        'RIGHT': (1,  0),
    }

    body_set = set(snake.body[1:])
    vision = {}
    for name, (dx, dy) in dir_map.items():
        ray = ['H']
        hx, hy = snake.head()
        px, py = hx + dx, hy + dy

        while 0 <= px < nb_cells and 0 <= py < nb_cells:
            pos = (px, py)
            if pos in body_set:
                ray.append('S')
            elif pos in apples_map:
                ray.append('G' if apples_map[pos] == 'green' else 'R')
            else:
                ray.append('0')
            px += dx
            py += dy

        ray.append('W')
        vision[name] = ray

    return vision


def vision_to_state(vision):
    """Encode vision as a 12-bit tuple for the Q-table.

    For each of 4 directions: (danger_near, has_green, has_red)
    danger_near = next cell is W or S (immediate threat)
    """
    state = []
    for dir_name in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        ray = vision[dir_name]   # ['H', ..., 'W']
        cells = ray[1:]          # exclude 'H'

        danger = 1 if cells and cells[0] in ('W', 'S') else 0
        has_green = 1 if 'G' in cells else 0
        has_red = 1 if 'R' in cells else 0

        state.extend([danger, has_green, has_red])

    return tuple(state)


def print_vision(vision):
    """Print snake vision in terminal as shown in the subject."""
    up = vision['UP'][::-1]      # reversed: W ... H
    down = vision['DOWN']        # H ... W
    left = vision['LEFT'][::-1]  # reversed: W ... H
    right = vision['RIGHT']      # H ... W

    left_str = ''.join(left[:-1])    # W...0 (excluding H)
    right_str = ''.join(right[1:])   # 0...W (excluding H)
    col = len(left_str)

    for cell in up[:-1]:             # W down to one above H
        print(' ' * col + cell)

    print(f"{left_str}H{right_str}")

    for cell in down[1:]:            # one below H down to W
        print(' ' * col + cell)
