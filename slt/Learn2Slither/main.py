import argparse
import os
import sys
import time

from const import CELL_SIZE, ACTION_NAMES
from game import Game
from agent import Agent


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description='Learn2Slither')
    p.add_argument('-sessions', type=int, default=1,
                   help='Number of training sessions')
    p.add_argument('-save', type=str, default=None,
                   help='Save model to file after training')
    p.add_argument('-load', type=str, default=None,
                   help='Load model from file before training')
    p.add_argument('-visual', choices=['on', 'off'], default='on',
                   help='Enable graphical display')
    p.add_argument('-dontlearn', action='store_true',
                   help='Disable Q-table updates (exploitation only)')
    p.add_argument('-step-by-step', action='store_true', dest='step_by_step',
                   help='Advance one step per key press (Space/Enter)')
    p.add_argument('-speed', type=float, default=0.15,
                   help='Seconds between steps when visual is on')
    return p.parse_args()


# ── Renderer (optional tkinter) ───────────────────────────────────────────────

class Renderer:
    def __init__(self, game):
        import tkinter as tk
        self.game = game
        self.tk = tk
        self.root = tk.Tk()
        self.root.title('Learn2Slither')
        self.root.resizable(False, False)

        nb = game.nb_cells
        cs = CELL_SIZE
        w, h = nb * cs, nb * cs

        self.canvas = tk.Canvas(self.root, width=w, height=h, bg='#1a1a2e')
        self.canvas.pack()

        # Session info label
        self.info_var = tk.StringVar(value='Session 0')
        tk.Label(self.root, textvariable=self.info_var,
                 bg='#1a1a2e', fg='white').pack()

        self._closed = False
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

        self._step_ready = False
        self.root.bind('<space>', lambda e: self._set_step())
        self.root.bind('<Return>', lambda e: self._set_step())

    def _set_step(self):
        self._step_ready = True

    def _on_close(self):
        self._closed = True
        self.root.destroy()

    def render(self, session=None, score=None):
        if self._closed:
            return
        nb = self.game.nb_cells
        cs = CELL_SIZE
        c = self.canvas
        c.delete('all')

        # Grid
        for i in range(nb + 1):
            c.create_line(i * cs, 0, i * cs, nb * cs, fill='#333355')
            c.create_line(0, i * cs, nb * cs, i * cs, fill='#333355')

        # Apples
        for apple in self.game.apples:
            ax, ay = apple['pos']
            color = '#00e676' if apple['type'] == 'green' else '#ff1744'
            c.create_rectangle(ax * cs + 2, ay * cs + 2,
                                (ax + 1) * cs - 2, (ay + 1) * cs - 2,
                                fill=color, outline='')

        # Snake
        body = self.game.snake.body
        for idx, (bx, by) in enumerate(body):
            color = '#00bcd4' if idx == 0 else '#0288d1'
            c.create_rectangle(bx * cs + 1, by * cs + 1,
                                (bx + 1) * cs - 1, (by + 1) * cs - 1,
                                fill=color, outline='')

        if session is not None:
            info = f'Session {session}  |  Length {len(body)}'
            if score is not None:
                info += f'  |  Max {score}'
            self.info_var.set(info)

        self.root.update()

    def wait_step(self):
        """Block until Space or Enter is pressed."""
        self._step_ready = False
        while not self._step_ready and not self._closed:
            self.root.update()
            time.sleep(0.02)

    def is_closed(self):
        return self._closed

    def close(self):
        if not self._closed:
            self._closed = True
            self.root.destroy()


# ── Training loop ─────────────────────────────────────────────────────────────

def run(args):
    game = Game()
    agent = Agent(learning=not args.dontlearn)

    if args.load:
        if not os.path.isfile(args.load):
            print(f'Error: model file not found: {args.load}', file=sys.stderr)
            sys.exit(1)
        agent.load(args.load)
        print(f'Load trained model from {args.load}')

    renderer = None
    if args.visual == 'on':
        renderer = Renderer(game)

    overall_max_length = 0
    overall_max_duration = 0

    for session in range(1, args.sessions + 1):
        game.reset()

        if renderer and renderer.is_closed():
            break

        while not game.done:
            if renderer and renderer.is_closed():
                break

            state = game.get_state()
            action = agent.get_action(state)

            if args.visual == 'on':
                game.print_state()
                print(ACTION_NAMES[action])
                print()

            reward, done = game.step(action)

            if not args.dontlearn:
                next_state = game.get_state() if not done else state
                agent.update(state, action, reward, next_state, done)

            if renderer:
                renderer.render(session=session,
                                score=overall_max_length)
                if args.step_by_step:
                    renderer.wait_step()
                else:
                    time.sleep(args.speed)

        agent.decay_epsilon()

        if game.max_length > overall_max_length:
            overall_max_length = game.max_length
        if game.steps > overall_max_duration:
            overall_max_duration = game.steps

    print(f'Game over, max length = {overall_max_length},'
          f' max duration = {overall_max_duration}')

    if args.save:
        agent.save(args.save)
        print(f'Save learning state in {args.save}')

    if renderer:
        renderer.close()


if __name__ == '__main__':
    run(parse_args())
