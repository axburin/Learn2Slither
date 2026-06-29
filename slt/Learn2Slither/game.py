from const import (NB_CELLS, ACTION_TO_DIR,
                   REWARD_GREEN, REWARD_RED, REWARD_STEP, REWARD_DEATH)
from helpers import random_snake_body, random_free_cell
from snake import Snake
from vision import get_vision, vision_to_state, print_vision


class Game:
    def __init__(self, nb_cells=NB_CELLS):
        self.nb_cells = nb_cells
        self.snake = None
        self.apples = []
        self.done = False
        self.max_length = 0
        self.steps = 0
        self.reset()

    # ── Setup ─────────────────────────────────────────────────────────────────

    def reset(self):
        body = random_snake_body(nb_cells=self.nb_cells)
        self.snake = Snake(body)
        self.apples = []
        self.done = False
        self.max_length = len(self.snake.body)
        self.steps = 0
        for apple_type, count in [('green', 2), ('red', 1)]:
            for _ in range(count):
                self._spawn_apple(apple_type)

    def _spawn_apple(self, apple_type):
        occupied = set(self.snake.body) | {a['pos'] for a in self.apples}
        pos = random_free_cell(occupied, self.nb_cells)
        self.apples.append({'type': apple_type, 'pos': pos})

    # ── State ─────────────────────────────────────────────────────────────────

    def get_vision(self):
        return get_vision(self.snake, self.apples, self.nb_cells)

    def get_state(self):
        return vision_to_state(self.get_vision())

    def print_state(self):
        print_vision(self.get_vision())

    # ── Step ──────────────────────────────────────────────────────────────────

    def step(self, action):
        """Apply action, return (reward, done)."""
        direction = ACTION_TO_DIR[action]
        next_head = self.snake.next_head(direction)

        # Wall collision
        x, y = next_head
        if not (0 <= x < self.nb_cells and 0 <= y < self.nb_cells):
            self.done = True
            return REWARD_DEATH, True

        # Self collision (includes tail: any occupied cell = death)
        if next_head in self.snake.body[1:]:
            self.done = True
            return REWARD_DEATH, True

        # Move: insert new head
        self.snake.body.insert(0, next_head)

        # Check apple at new head
        apple_index = self.snake.hits_apples(self.apples)
        if apple_index is not None:
            apple = self.apples.pop(apple_index)
            if apple['type'] == 'green':
                # Keep tail (snake grows)
                reward = REWARD_GREEN
                self._spawn_apple('green')
            else:
                # Remove tail (normal move) + one more (shrink)
                self.snake.body.pop()
                if self.snake.body:
                    self.snake.body.pop()
                reward = REWARD_RED
                self._spawn_apple('red')
                if not self.snake.body:
                    self.done = True
                    return REWARD_DEATH, True
        else:
            self.snake.body.pop()
            reward = REWARD_STEP

        self.steps += 1
        length = len(self.snake.body)
        if length > self.max_length:
            self.max_length = length

        return reward, False
