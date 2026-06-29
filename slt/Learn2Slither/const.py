NB_CELLS = 10
CELL_SIZE = 50
GRID_W = NB_CELLS * CELL_SIZE
GRID_H = NB_CELLS * CELL_SIZE

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# 0=UP 1=DOWN 2=LEFT 3=RIGHT
ACTION_TO_DIR = {
    0: (0, -1),
    1: (0, 1),
    2: (-1, 0),
    3: (1, 0),
}

ACTION_NAMES = {0: 'UP', 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}

KEY_BINDINGS = {
    'Up':    0,
    'Down':  1,
    'Left':  2,
    'Right': 3,
    'z':     0,
    's':     1,
    'q':     2,
    'd':     3,
}

OPPOSITES = {
    0: 1,
    1: 0,
    2: 3,
    3: 2,
}

# Rewards
REWARD_GREEN = 10.0
REWARD_RED = -5.0
REWARD_STEP = -0.1
REWARD_DEATH = -100.0
