import tkinter as tk
from tkinter import *
import numpy as np

class NotWindow(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)
		self.title("Instructions")
		self.geometry("560x250")  
		self.text = tk.Text(self, wrap="word", font=("Arial", 12))
		self.text.pack(fill="both", expand=True)

		self.text.insert("end", "This graph cannot be 3-colored, here are some possible reasons:\n")
		self.text.insert("end", "1. The input graph is triangle free but non-planar (cannot be drawn in a way such that no edges cross)\n")
		self.text.insert("end", "2. The input graph is planar but contains triangles and therefore may require > 3 colors\n\n")

		self.text.insert("end", "The graph only has a guaranteed 3-coloring if:\n")
		self.text.insert("end", "1. The graph is triangle free and planar\n")
		self.text.insert("end", "2. Every vertex in the graph has degree < 3\n")
		self.text.insert("end", "3. There are <= 3 vertices total in the graph\n\n")
		self.text.insert("end", "*NOTE: The graph may be 3-colorable in other circumstances but its not guaranteed\n\n")

class InstructionsWindow(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)
		self.title("Instructions")
		self.geometry("450x450")  
		self.text = tk.Text(self, wrap="word", font=("Arial", 12))
		self.text.pack(fill="both", expand=True)

		self.switch_button = tk.Button(self, text="Background", command=self.switch_screen)
		self.switch_button.place(relx=0.5, rely=0.95, anchor='center')

		# Flag to keep track of the current screen
		self.current_screen = 1

		self.show_screen()

	def show_screen(self):
			# Delete the existing text
			self.text.delete("1.0", "end")
			self.screen1_content()

	def screen1_content(self):
		self.text.delete("1.0", "end")
		self.text.insert("end", "Instructions:\n\n")

		self.text.insert("end", "1. Graph Construction and Deletion:\n")
		self.text.insert("end", "- Left click to add vertices\n")
		self.text.insert("end", "- Right click on a start vertex, then right click on an end vertex to create an edge\n")
		self.text.insert("end", "- Click the clear button to clear the whole graph\n")
		self.text.insert("end", "- Click the clear mode button to clear individual vertices and edges\n")
		self.text.insert("end", "- In clear mode, left click on a vertex to remove the vertex and its incident edges\n\n")

		self.text.insert("end", "2. Coloring:\n")
		self.text.insert("end", "- Click the color button to 3-color all the vertices at once\n")
		self.text.insert("end", "- Click the next button to move one step forward into the coloring process\n")
		self.text.insert("end", "- Click the back button to move one step backwards in the coloring process\n\n")
		self.text.insert("end", "NOTE: You must close the instructional window to proceed with the main application\n")

		self.text.insert("end", "NOTE: If the graph cannot be colored, the vertex will remain black and you will receive a terminal output\n\n")

		self.text.insert("end", "Preset graphs:\n\n")
		self.text.insert("end", "TF E1 - Triangle Free example 1 (can be 3-colored)\n")
		self.text.insert("end", "TF E2 - Triangle Free example 2 (can be 3-colored)\n")
		self.text.insert("end", "TF 4C - Triangle Free example 3 (requires 4 colors)\n")
		self.text.insert("end", "Triangle - Graph with triangles example 1 (can be 3-colored)\n")
		self.text.insert("end", "Simple - Simple graph with triangles example 2 (can be 3-colored)\n")

	def screen2_content(self):
			self.text.delete("1.0", "end")

			self.text.insert("end", "Algorithm Background:\n\n")
			self.text.insert("end", "- The problem of vertex coloring is to find an assignment of colors for each vertex such that no two")
			self.text.insert("end", " adjacent vertices share the same color\n")
			self.text.insert("end", "- The goal of this GUI is to display a 3-coloring (only use 3-colors at max) to color the input graph\n")
			self.text.insert("end", "- This procedure is done using a brute force algorithm such that all three colorings are tried until a valid one is found\n\n")
			

			self.text.insert("end", "Coloring Background\n\n")
			self.text.insert("end", "- All planar triangle free graphs can be 3-colored (Grötzsch's theorem)\n")
			self.text.insert("end", "- Not all planar graphs can be 3-colored (they can be 4 or 5 colored however)\n\n")

			self.text.insert("end", "Research Background\n\n")
			self.text.insert("end", "- The best runtime for the problem of coloring a triangle free planar graph is linear\n")
			self.text.insert("end", "- There are also many quadratic and logarithmic algorithms\n")

	def switch_screen(self):
		if self.current_screen == 1:
				self.screen2_content()
				self.switch_button.config(text="Instructions")
				self.current_screen = 2
		else:
				self.screen1_content()
				self.switch_button.config(text="Background")
				self.current_screen = 1
				
class GraphEditor:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Graph Editor")
		self.canvas = tk.Canvas(self.root, width=600, height=600)
		self.canvas.pack()
		self.vertices = []
		self.edges = []
		self.graph = {} 
		self.coloring_step = 0
		self.vertex_index = 0
		self.graph_to_draw = 0
		self.colored = False
		self.start_vertex = None
		self.instructions_window = None
		self.end_vertex = None
		self.clear_mode_state = "off"
		self.canvas.bind("<Button-1>", self.add_vertex)
		self.canvas.bind("<Button-2>", self.start_add_edge)
		self.create_widgets()
		self.root.mainloop()	

	def add_vertex(self, event=None, x=None, y=None):
		if x is None and y is None:
			x, y = event.x, event.y

		vertex = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='black', tags=self.vertex_index)

		self.canvas.tag_lower(vertex)  
		self.vertices.append((x, y, vertex))
		self.vertex_index+=1

		if vertex not in self.graph:
			self.graph[vertex] = set()

		if self.colored == True:
			self.remove_coloring()

	def start_add_edge(self, event=None, x=None, y=None):
		if x is None and y is None:
			x, y = event.x, event.y

		for vertex in self.vertices:
			if abs(vertex[0]-x) < 15 and abs(vertex[1]-y) < 15:
				self.start_vertex = vertex[2]
				self.canvas.bind("<Button-2>", self.end_add_edge)
				break

	def end_add_edge(self, event=None, x=None, y=None):
		if x is None and y is None:
			x, y = event.x, event.y

		for vertex in self.vertices:
			if abs(vertex[0]-x) < 15 and abs(vertex[1]-y) < 15:
				self.end_vertex = vertex[2]
				if self.start_vertex and self.end_vertex and self.start_vertex != self.end_vertex:
					for edge in self.edges:
						if (edge[0] == self.start_vertex and edge[1] == self.end_vertex) or (edge[0] == self.end_vertex and edge[1] == self.start_vertex):
							return
					x1, y1 = self.canvas.coords(self.start_vertex)[0], self.canvas.coords(self.start_vertex)[1]
					x2, y2 = self.canvas.coords(self.end_vertex)[0], self.canvas.coords(self.end_vertex)[1]
					vertex_width = 20
					x1 += vertex_width/2
					y1 += vertex_width/2
					x2 += vertex_width/2
					y2 += vertex_width/2
					edge = self.canvas.create_line(x1, y1, x2, y2)
					self.edges.append((self.start_vertex, self.end_vertex, edge))
					self.canvas.tag_lower(edge)  # set the edge to be at the bottom of the canvas

					if self.end_vertex not in self.graph[self.start_vertex]:
						self.graph[self.start_vertex].add(self.end_vertex)

					if self.start_vertex not in self.graph[self.end_vertex]:
						self.graph[self.end_vertex].add(self.start_vertex)

				self.start_vertex = None
				self.end_vertex = None
				self.canvas.bind("<Button-2>", self.start_add_edge)

		if self.colored == True:
			self.remove_coloring()

	def three_color(self):
		def try_3_coloring(vertices_left, colors, coloring_order):
			if not vertices_left:
				return colors, coloring_order

			vertex = vertices_left[0]
			neighbor_colors = set(colors.get(neighbor, -1) for neighbor in self.graph[vertex])

			for color in ['red', 'green', 'blue']:
				if color not in neighbor_colors:
					colors[vertex] = color
					coloring_order.append((vertex, color))
					self.canvas.itemconfig(vertex, fill=color)

					result, coloring_order = try_3_coloring(vertices_left[1:], colors, coloring_order)
					if result is not None:
							return result, coloring_order

					del colors[vertex]
					coloring_order.pop()

			return None, coloring_order

		vertices_to_color = list(self.graph.keys())[:self.coloring_step]
		colors, coloring_order = try_3_coloring(vertices_to_color, {}, [])

		if colors is not None:
			for vertex, color in colors.items():
				self.canvas.itemconfig(vertex, fill=color)
				self.canvas.update()

			for vertex in self.graph:
				if vertex not in colors:
					self.canvas.itemconfig(vertex, fill='black')
					self.canvas.update()

		else:
			self.show_not_colorable()

		return coloring_order

	def remove_vertex(self, event):
		x, y = event.x, event.y
		to_remove = None
		for vertex in self.vertices:
				if abs(vertex[0]-x) < 15 and abs(vertex[1]-y) < 15:
						to_remove = vertex
						break
		if to_remove is not None:
				self.vertices.remove(to_remove)
				self.graph.pop(to_remove[2], None)
				for edge in self.edges:
						if edge[0] == to_remove[2] or edge[1] == to_remove[2]:
								self.canvas.delete(edge[2])
				self.edges = [edge for edge in self.edges if edge[0] != to_remove[2] and edge[1] != to_remove[2]]
				self.canvas.delete(to_remove[2])

		if self.colored == True:
			self.remove_coloring()

	def remove_coloring(self):
		if self.colored == True:
			for vertex in self.graph:
				self.canvas.itemconfig(vertex, fill='black')

			self.colored = False

		self.coloring_step = 0

	def check_if_colored(self):
		for vertex in self.graph:
			vertex_color = self.canvas.itemcget(vertex, 'fill')

			if vertex_color != 'black':
				return True
		return False

	def print_graph(self):
		output = ""
		for vertex, neighbors in self.graph.items():
			output += f"{vertex}: {', '.join(str(n) for n in neighbors)}\n"
		return output

	def draw_graph_nested_square(self):
		self.clearGraph()
		#x increases to the left, y increases going down

		#outer vertices
		self.add_vertex(x=124, y=124)
		self.add_vertex(x=396, y=124)
		self.add_vertex(x=124, y=376)
		self.add_vertex(x=260, y=376)
		self.add_vertex(x=396, y=376)

		#inner vertices
		self.add_vertex(x=200, y=200)
		self.add_vertex(x=260, y=200)
		self.add_vertex(x=200, y=250)
		self.add_vertex(x=260, y=250)
		self.add_vertex(x=320, y=250)
		self.add_vertex(x=200, y=300)
		self.add_vertex(x=260, y=300)
		self.add_vertex(x=320, y=300)

		#edges
		self.start_add_edge(x=124, y=124)
		self.end_add_edge(x=200, y=200)

		self.start_add_edge(x=200, y=200)
		self.end_add_edge(x=260, y=200)

		self.start_add_edge(x=260, y=200)
		self.end_add_edge(x=396, y=124)

		self.start_add_edge(x=124, y=124)
		self.end_add_edge(x=124, y=376)

		self.start_add_edge(x=200, y=200)
		self.end_add_edge(x=200, y=250)

		self.start_add_edge(x=200, y=250)
		self.end_add_edge(x=200, y=300)

		self.start_add_edge(x=200, y=300)
		self.end_add_edge(x=124, y=376)

		self.start_add_edge(x=200, y=300)
		self.end_add_edge(x=260, y=300)

		self.start_add_edge(x=200, y=250)
		self.end_add_edge(x=260, y=250)

		self.start_add_edge(x=260, y=250)
		self.end_add_edge(x=320, y=250)

		self.start_add_edge(x=320, y=250)
		self.end_add_edge(x=396, y=124)

		self.start_add_edge(x=320, y=250)
		self.end_add_edge(x=320, y=300)

		self.start_add_edge(x=320, y=300)
		self.end_add_edge(x=260, y=300)

		self.start_add_edge(x=124, y=376)
		self.end_add_edge(x=260, y=376)

		self.start_add_edge(x=260, y=376)
		self.end_add_edge(x=396, y=376)

		self.start_add_edge(x=260, y=300)
		self.end_add_edge(x=260, y=376)

		self.start_add_edge(x=260, y=250)
		self.end_add_edge(x=260, y=300)

		self.start_add_edge(x=260, y=250)
		self.end_add_edge(x=260, y=200)

		self.start_add_edge(x=320, y=300)
		self.end_add_edge(x=396, y=376)

		self.start_add_edge(x=124, y=124)
		self.end_add_edge(x=396, y=124)

		self.start_add_edge(x=396, y=376)
		self.end_add_edge(x=396, y=124)

	def draw_graph_pentagon(self):
		self.clearGraph()

		#outer vertices
		self.add_vertex(x=130, y=280)
		self.add_vertex(x=290, y=170)
		self.add_vertex(x=450, y=280)
		self.add_vertex(x=205, y=440)
		self.add_vertex(x=290, y=440)
		self.add_vertex(x=375, y=440)

		#inner vertices
		self.add_vertex(x=220, y=280)
		self.add_vertex(x=360, y=280)
		self.add_vertex(x=245, y=330)
		self.add_vertex(x=335, y=330)

		#add edges
		self.start_add_edge(x=130, y=280)
		self.end_add_edge(x=290, y=170)

		self.start_add_edge(x=450, y=280)
		self.end_add_edge(x=290, y=170)

		self.start_add_edge(x=220, y=280)
		self.end_add_edge(x=290, y=170)

		self.start_add_edge(x=360, y=280)
		self.end_add_edge(x=290, y=170)

		self.start_add_edge(x=360, y=280)
		self.end_add_edge(x=335, y=330)

		self.start_add_edge(x=220, y=280)
		self.end_add_edge(x=245, y=330)

		self.start_add_edge(x=335, y=330)
		self.end_add_edge(x=245, y=330)

		self.start_add_edge(x=205, y=440)
		self.end_add_edge(x=245, y=330)

		self.start_add_edge(x=335, y=330)
		self.end_add_edge(x=375, y=440)

		self.start_add_edge(x=205, y=440)
		self.end_add_edge(x=130, y=280)

		self.start_add_edge(x=205, y=440)
		self.end_add_edge(x=290, y=440)

		self.start_add_edge(x=375, y=440)
		self.end_add_edge(x=290, y=440)

		self.start_add_edge(x=375, y=440)
		self.end_add_edge(x=450, y=280)

	def draw_graph_bad(self):
		self.clearGraph()

		#outer vertices
		self.add_vertex(x=300, y=90)
		self.add_vertex(x=540, y=200)
		self.add_vertex(x=60, y=200)
		self.add_vertex(x=110, y=480)
		self.add_vertex(x=490, y=480)

		#inner vertices
		self.add_vertex(x=300, y=180)
		self.add_vertex(x=440, y=250)
		self.add_vertex(x=160, y=250)
		self.add_vertex(x=230, y=380)
		self.add_vertex(x=370, y=380)

		#center vertex
		self.add_vertex(x=300, y=300)

		#add outer edges
		self.start_add_edge(x=60, y=200)
		self.end_add_edge(x=300, y=90)

		self.start_add_edge(x=540, y=200)
		self.end_add_edge(x=300, y=90)

		self.start_add_edge(x=540, y=200)
		self.end_add_edge(x=490, y=480)

		self.start_add_edge(x=490, y=480)
		self.end_add_edge(x=110, y=480)

		self.start_add_edge(x=60, y=200)
		self.end_add_edge(x=110, y=480)

		#middle layer star edges
		self.start_add_edge(x=160, y=250)
		self.end_add_edge(x=110, y=480)

		self.start_add_edge(x=370, y=380)
		self.end_add_edge(x=110, y=480)

		self.start_add_edge(x=370, y=380)
		self.end_add_edge(x=540, y=200)

		self.start_add_edge(x=160, y=250)
		self.end_add_edge(x=300, y=90)

		self.start_add_edge(x=440, y=250)
		self.end_add_edge(x=300, y=90)

		self.start_add_edge(x=440, y=250)
		self.end_add_edge(x=490, y=480)

		self.start_add_edge(x=230, y=380)
		self.end_add_edge(x=490, y=480)

		self.start_add_edge(x=230, y=380)
		self.end_add_edge(x=60, y=200)

		self.start_add_edge(x=300, y=180)
		self.end_add_edge(x=60, y=200)

		self.start_add_edge(x=300, y=180)
		self.end_add_edge(x=540, y=200)

		#inner most star
		self.start_add_edge(x=370, y=380)
		self.end_add_edge(x=300, y=300)

		self.start_add_edge(x=230, y=380)
		self.end_add_edge(x=300, y=300)

		self.start_add_edge(x=160, y=250)
		self.end_add_edge(x=300, y=300)

		self.start_add_edge(x=300, y=180)
		self.end_add_edge(x=300, y=300)

		self.start_add_edge(x=440, y=250)
		self.end_add_edge(x=300, y=300)

	def draw_graph_triangle(self):
		self.clearGraph()

		#outermost triangle
		self.add_vertex(x=300, y=80)
		self.add_vertex(x=510, y=540)
		self.add_vertex(x=90, y=540)

		#middle triangle
		self.add_vertex(x=300, y=170)
		self.add_vertex(x=440, y=450)
		self.add_vertex(x=160, y=450)

		#innermost triangle
		self.add_vertex(x=300, y=260)
		self.add_vertex(x=370, y=360)
		self.add_vertex(x=230, y=360)

		#edges outermost
		self.start_add_edge(x=300, y=80)
		self.end_add_edge(x=90, y=540)

		self.start_add_edge(x=510, y=540)
		self.end_add_edge(x=90, y=540)

		self.start_add_edge(x=510, y=540)
		self.end_add_edge(x=300, y=80)

		#edges middle
		self.start_add_edge(x=300, y=170)
		self.end_add_edge(x=160, y=450)

		self.start_add_edge(x=160, y=450)
		self.end_add_edge(x=440, y=450)

		self.start_add_edge(x=440, y=450)
		self.end_add_edge(x=300, y=170)

		#edges innermost 
		self.start_add_edge(x=300, y=260)
		self.end_add_edge(x=230, y=360)

		self.start_add_edge(x=370, y=360)
		self.end_add_edge(x=230, y=360)

		self.start_add_edge(x=370, y=360)
		self.end_add_edge(x=300, y=260)

		#edges between triangles
		self.start_add_edge(x=300, y=80)
		self.end_add_edge(x=300, y=170)

		self.start_add_edge(x=300, y=170)
		self.end_add_edge(x=300, y=260)

		self.start_add_edge(x=160, y=450)
		self.end_add_edge(x=230, y=360)

		self.start_add_edge(x=160, y=450)
		self.end_add_edge(x=90, y=540)

		self.start_add_edge(x=370, y=360)
		self.end_add_edge(x=440, y=450)

		self.start_add_edge(x=440, y=450)
		self.end_add_edge(x=510, y=540)

	def draw_graph_simple(self):
		self.clearGraph()

		self.add_vertex(x=190, y=240)
		self.add_vertex(x=410, y=240)
		self.add_vertex(x=190, y=460)
		self.add_vertex(x=410, y=460)

		self.start_add_edge(x=190, y=240)
		self.end_add_edge(x=410, y=240)

		self.start_add_edge(x=410, y=460)
		self.end_add_edge(x=410, y=240)

		self.start_add_edge(x=190, y=460)
		self.end_add_edge(x=410, y=240)

		self.start_add_edge(x=190, y=240)
		self.end_add_edge(x=190, y=460)

		self.start_add_edge(x=410, y=460)
		self.end_add_edge(x=190, y=460)


	def create_widgets(self):
			instructions_button = tk.Button(self.root, text="Information", command=self.show_instructions)
			instructions_button.place(relx=0.10, rely=0.98, anchor='center')

			back_button = Button(self.root, text="Back", command=self.backStep)
			back_button.place(relx=0.30, rely=0.98, anchor='center')

			start_coloring = Button(self.root, text="Color", command=self.startColor)
			start_coloring.place(relx=0.42, rely=0.98, anchor='center')

			clear_button = Button(self.root, text="Clear", command=self.clearGraph)
			clear_button.place(relx=0.54, rely=0.98, anchor='center')

			next_button = Button(self.root, text="Next", command=self.nextStep)
			next_button.place(relx=0.66, rely=0.98, anchor='center')

			clear_mode_button = Button(self.root, text="Clear Mode", command=self.clear_mode)
			clear_mode_button.place(relx=0.86, rely=0.98, anchor='center')

			triangle_free_e1 = Button(self.root, text="TF E1", command=self.draw_graph_nested_square)
			triangle_free_e1.place(relx=0.10, rely=0.05, anchor='center')

			triangle_free_e2 = Button(self.root, text="TF E2", command=self.draw_graph_pentagon)
			triangle_free_e2.place(relx=0.30, rely=0.05, anchor='center')

			triangle_free_bad = Button(self.root, text="TF 4C", command=self.draw_graph_bad)
			triangle_free_bad.place(relx=0.50, rely=0.05, anchor='center')

			triangle_e1 = Button(self.root, text="Triangle", command=self.draw_graph_triangle)
			triangle_e1.place(relx=0.70, rely=0.05, anchor='center')

			simple = Button(self.root, text="Simple", command=self.draw_graph_simple)
			simple.place(relx=0.90, rely=0.05, anchor='center')


			self.all_buttons = [back_button, start_coloring, next_button, triangle_free_e1, triangle_free_e2, triangle_free_bad, triangle_e1, simple]

	def show_instructions(self):
		instructions_window = InstructionsWindow(self.root)
		instructions_window.grab_set()

	def show_not_colorable(self):
		not_window = NotWindow(self.root)
		not_window.grab_set()
				
	def startColor(self):
		self.coloring_step = len(self.graph.keys())
		self.three_color()

		self.colored = True

	def nextStep(self):
		if self.coloring_step < len(self.graph.keys()) and len(self.graph.keys()) != 0:
			self.coloring_step+=1
			self.three_color()

		self.colored = self.check_if_colored()

	def clear_mode(self):
		if self.clear_mode_state == "off":
			self.clear_mode_state = "on"
		else:
			self.clear_mode_state = "off"

		if self.clear_mode_state == "on":
			self.canvas.unbind("<Button-1>")
			self.canvas.bind("<Button-1>", self.remove_vertex)

			for button in self.all_buttons:
				button.config(state=tk.DISABLED)
		else:
			self.canvas.unbind("<Button-1>")
			self.canvas.bind("<Button-1>", self.add_vertex)

			for button in self.all_buttons:
				button.config(state=tk.NORMAL)

	def clearGraph(self):
		for vertex in self.vertices:
			self.canvas.delete(vertex[2])
		for edge in self.edges:
			self.canvas.delete(edge[2])

		self.vertices = []
		self.edges = []
		self.graph = {}
		self.vertex_index = 0
		self.coloring_step = 0
		self.colored = False

	def backStep(self):
		if self.coloring_step > 0 and len(self.graph.keys()) != 0:
			self.coloring_step-=1
			self.three_color()

		self.colored = self.check_if_colored()

if __name__ == '__main__':
	app = GraphEditor()
