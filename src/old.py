import Graph
from datetime import datetime

def  clique(U,size):
	dt = datetime.now()
	time_start = dt.microsecond
	global max
	if U.length() == 0:
		if size > max:
			max = size
		return
	while U.length():
		U.print_graph()
		if size + U.length() <= max:
			return
		min_v = None
		for v in U.vertices:
			if min_v == None or int(v) < int(min_v):
				min_v = v
		
		v_i = []
		for v in U.vertices[min_v]:
			v_i.append(v)

		del U.vertices[min_v]
		new_U={}
		for v in v_i:
			if v in U.vertices:
				new_U[v] = []
				for i in U.vertices[v]:
					if i in U.vertices:
						new_U[v].append(i)
				if new_U[v]==[]:
					del new_U[v]
		U.vertices=new_U
		clique(U,size+1)
		
	global time_elapsed
	dt = datetime.now()
	time_stop = dt.microsecond
	time_elapsed = time_stop-time_start
		
	return



graph = Graph.Graph("input2.json")
max=0
clique(graph,1)
print max
print "Time elapsed: " + str(time_elapsed) + " microseconds"
