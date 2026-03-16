import tkinter as tk
from game import Game


def main():
	root = tk.Tk()
	game = Game(root)
	game.autoplay()
	root.mainloop()


if __name__ == "__main__":
	main()