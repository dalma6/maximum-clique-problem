import json

class Graph:
	def __init__(self, input_file):
		self.vertices = json.load(open(input_file, "r"))
		
	def print_graph(self):
		print self.vertices
		
	def length(self):
		return len(self.vertices)