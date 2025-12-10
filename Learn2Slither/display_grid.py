
import tkinter as tk
import random as rd

NB_cases = 10
size_cases = 20
grid_W = NB_cases*size_cases
grid_H = NB_cases*size_cases

def random_free_cell_for_elem(occupied):
	x = rd.randint(0, NB_cases - 1)
	y = rd.randint(0, NB_cases - 1)
	if(x, y) not in occupied:
		return(x, y)



root = tk.Tk()
root.title("grid")

canvas = tk.Canvas(root, width = NB_cases*size_cases, height= NB_cases*size_cases, bg="black")

for i in range(NB_cases + 1):

	canvas.create_line(i*size_cases, 0, i*size_cases, NB_cases*size_cases, fill="white")
	canvas.create_line(0, i*size_cases, NB_cases*size_cases, i*size_cases, fill="white")
canvas.pack()

occupied = set()

snake_head = random_free_cell_for_elem(occupied)
occupied.add(snake_head)

apple_green = random_free_cell_for_elem(occupied)
occupied.add(apple_green)

apple_red = random_free_cell_for_elem(occupied)
occupied.add(apple_red)

def draw_cell(x, y, color):
	canvas.create_rectangle(x*size_cases, y*size_cases,
		(x+1)*size_cases, (y+1)*size_cases,
		fill=color)

	
draw_cell(*snake_head, "blue")

draw_cell(*apple_green, "green")

draw_cell(*apple_red, "red")


root.mainloop()
