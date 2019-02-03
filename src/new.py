from Graph import Graph
import numpy as np

graph = Graph("input1.json")
max_size = 0
c = [0] * graph.length()
found = False

def clique(graph, size, param):
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
		min_j = None
		for v in graph.vertices:
			if min_j == None or v < min_j:
				min_j = v
				
		if size + c[param] <= max_size:
			return
				
		v_i = graph.vertices[min_j]
		del graph.vertices[min_j]
		new_graph = {}
		for v in v_i:
			if v in graph.vertices:
				new_graph[v] = []
				for i in graph.vertices[v]:
					if i in v_i:
						new_graph[v].append(i)
				if new_graph[v] == []:
					del new_graph[v]
		graph.vertices = new_graph			
		clique(graph, size+1, param)
		
		if found:
			return
	return

def new():
	global found
	global max_size
	global c
	
	for i in range(len(c)):
		found = False
		Si = Graph("", orig=graph)
		if i:
			del Si.vertices[str(i-1)]
		v_i = graph.vertices[str(i)]
		new_graph = {}
		for v in v_i:
			if v in Si.vertices:
				new_graph[v] = []
				for k in Si.vertices[v]:
					if k in v_i:
						new_graph[v].append(k)
				if not new_graph[v]:
					del new_graph[v]
		Si.vertices = new_graph
		clique(Si, 1, i)
		c[int(i)] = max_size
	
	return

if __name__ == "__main__":
	new()
	print max_size