NB_CELLS  = 10
CELL_SIZE = 20
GRID_W    = NB_CELLS * CELL_SIZE
GRID_H    = NB_CELLS * CELL_SIZE

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

KEY_BINDINGS = {
	"Up":    (0, -1),
	"Left":  (-1, 0),
	"Down":  (0, 1),
	"Right": (1, 0),
	"z":     (0, -1),
	"q":     (-1, 0),
	"s":     (0, 1),
	"d":     (1, 0),
}

OPPOSITES = {
	(0, -1): (0,  1),
	(0,  1): (0, -1),
	(-1, 0): (1,  0),
	(1,  0): (-1, 0),
}