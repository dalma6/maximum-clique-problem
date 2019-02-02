from Graph import Graph
import numpy as np

graph = Graph("input1.json")
max_size = 0
c = np.zeros(graph.length())
found = False

def clique(graph, size):
	global found
	global max_size
	global c
	
	if not graph.length():
		if size > max_size:
			max_size = size # new record, save it
			found = True
			return
	while graph:
		if size + graph.length() <= max_size:
			return
		min_vertex = None
		for v in graph.vertices:
			if not i or v < min_size:
				i = v
		if size + c[i] <= max_size:
			return
		v_i = graph.vertices[i]
		del graph.vertices[i]
		new_graph = {}
		for v in v_i:
			if v in graph.vertices:
				new_graph[v] = []
				for i in graph.vertices[v]:
					if i in v_i:
						new_graph[v].append(i)
				if not new_graph[v]:
					del new_graph[v]
		graph.vertices = new_graph			
		clique(graph, size+1)
		
		if found:
			return
	return

def new():
	global found
	global max_size
	global c
	
	for i in range(len(c), 0, -1):
		Si = Graph("", orig=graph)
		for j in range(len(c)-i):
			del Si.vertices[str(j)]
		v_i = graph.vertices[str(i)]
		new_graph = {}
		for v in v_i:
			if v in Si.vertices:
				new_graph[v] = []
				for i in Si.vertices[v]:
					if i in v_i:
						new_graph[v].append(i)
				if not new_graph[v]:
					del new_graph[v]
		Si.vertices = new_graph
		clique(Si, 1)
		c[int(i)-1] = max_size
		return

if __name__ == "__main__":
	new()
	print max_size