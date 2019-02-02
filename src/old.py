import Graph
def  clique(U,size):
	global max
	U.print_graph()
	if U.length()==0:
		if size>max:
			max=size
		return
	while U.length():
		if size + U.length()<=max:
			return
		min=None
		for v in U.vertices:
			if min==None or v<min:
				min=v
		
		v_i = U.vertices[min]
		del U.vertices[min]
		new_U={}
		for v in v_i:
			if v in U.vertices:
				new_U[v]=[]
				for i in U.vertices[v]:
					if i in v_i:
						new_U[v].append(i)
				if new_U[v]==[]:
					del new_U[v]
		U.vertices=new_U			
		clique(U,size+1)
	return



graph = Graph.Graph("input1.json")
max=0
clique(graph,0)
print max