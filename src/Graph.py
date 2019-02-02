import json

class Graph:
	def __init__(self, input_file, orig=None):
		if not orig:
			self.vertices = json.load(open(input_file, "r"))
		else:
			self.vertices = orig.vertices
		
	def print_graph(self):
		print self.vertices
		
	def length(self):
		return len(self.vertices)
	
	def __getitem__(self, item):
		return getattr(self, item)
	
