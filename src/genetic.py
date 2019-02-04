import random, string
import numpy as np
import sys, os
from Graph import Graph
from datetime import datetime

class GeneticAlgorithm:
	def __init__(self, graph):
		self._graph = graph 
		self._allowed_gene_values = set([0, 1])
		
		self._iterations = 10
		self._generation_size = 50
		self._mutation_rate = 0.5	  
		self._reproduction_size = 1000  
		self._current_iteration = 0
		self._stagnancy_parameter=20
		self._stagnancy_counter=0
		self._offspring_selection_mutation_prob = 0.2
		
		if self._graph.length() < 10:
			self._max_cut_points = self._graph.length() - 1
		else:
			self._max_cut_points = 10

		self._min_cut_points = 2
		self._num_cut_points = self._max_cut_points


	def local_optimize(self, child1, child2):
		child1, child2 = self.clique_extraction(child1,child2)
		child1, child2 = self.clique_improvement(child1,child2)
		return child1, child2
	
	def clique_extraction(self, child1, child2):
		graph1 = self.create_subgraph(self._graph.vertices,child1)
		graph2 = self.create_subgraph(self._graph.vertices,child2)
		while (not self.is_clique(graph1)) and graph1 != {}:
			array = self.find_smallest_two_degrees(graph1)
			child1, graph1 = self.delete_random_and_update(array,child1,graph1)
		while (not self.is_clique(graph2)) and graph2 != {}:
			array = self.find_smallest_two_degrees(graph2)
			child2, graph2 = self.delete_random_and_update(array,child2,graph2)
		return child1, child2

	def clique_improvement(self, child1, child2):
		i1 = self.take_random_element(child1)
		i2 = self.take_random_element(child2)
		
		for j in range(i1, len(child1)):
			if not child1[j]:
				if self.connected(self.create_subgraph(self._graph.vertices,child1), j):
					child1[j] = 1
		for j in range(i1):
			if not child1[j]:
				if self.connected(self.create_subgraph(self._graph.vertices,child1), j):
					child1[j] = 1
		for j in range(i2, len(child2)):
			if not child2[j]:
				if self.connected(self.create_subgraph(self._graph.vertices,child2), j):
					child2[j] = 1
		for j in range(i2):
			if not child2[j]:
				if self.connected(self.create_subgraph(self._graph.vertices,child2), j):
					child1[j] = 1
		return child1, child2

	def create_subgraph(self, graph, child):
		subgraph = {}
		for i in range(len(child)):
			if child[i]:
				subgraph[str(i)] = []
				for v in graph[str(i)]:
					subgraph[str(i)].append(v)
		empty_list = []
		for i in subgraph:
			for v in subgraph[i]:
				if not child[int(v)]:
					subgraph[i].remove(v)
			if subgraph[i] == []:
				empty_list.append(i)
		for i in empty_list:
			del subgraph[str(i)]
		return subgraph

	def is_clique(self, graph):
		if not graph:
			return False
		
		for v in graph:
			if not self.connected(graph,v):
				return False
		return True

	def connected(self, A, v):
		for u in A:
			if u != v:
				if v not in A[u]:
					return False
		return True


	def find_smallest_two_degrees(self, graph):	
		min1 = random.choice(graph.keys())
		min2 = min1
		while min1 == min2:
			min2 = random.choice(graph.keys())
		
		min1_len = len(graph[min1])
		min2_len = len(graph[min2])
		array = []
		if min1_len > min2_len:
			s = False
		else:
			s = True

		for i in graph:
			if i != min1 and i != min2:
				if s and len(graph[i]) < min2_len:
					min2_len = len(graph[i])
					if min2_len < min1_len:
						s = False
				elif (not s) and len(graph[i])<min1_len:
					min1_len = len(graph[i])
					if min1_len < min2_len:
						s = True
		for i in graph:
			if len(graph[i]) == min1_len or len(graph[i]) == min2_len:
				array.append(int(i))
		return array

	def delete_random_and_update(self, array, child, graph):
		removed = self.take_random_element(array)
		child[removed] = 0
		new_graph = self.create_subgraph(self._graph.vertices, child)
		return child, new_graph

	def optimize(self):
		chromosomes = self.initial_population()
		s=0
		while not self.stop_condition():
			for_reproduction = self.selection(chromosomes)
			print "Current iteration "+str(self._current_iteration)
			
			chromosomes,s_new = self.create_generation(for_reproduction)
			if s_new==s:
				self._stagnancy_counter+=1
			else:
				s=s_new
			self._current_iteration += 1
		
		return max(chromosomes, key=lambda chromo: chromo.fitness)


	def create_generation(self, for_reproduction):
		new_generation = []
		s_new=0
		if self._num_cut_points > self._min_cut_points and self._current_iteration%20 == 0:
				self._num_cut_points -= 2
		while len(new_generation) < self._generation_size:
			parents = random.sample(for_reproduction, 2)
			child1, child2 = self.crossover(parents[0].content, parents[1].content)
			child1, child2 = self.local_optimize(child1, child2)
			p = random.random()
			if p < self._offspring_selection_mutation_prob:
				child1 = self.mutation(child1)
				child2 = self.mutation(child2)
			print child1, child2
			if self.fitness(child1)>s_new:
				s_new=self.fitness(child1)
			if self.fitness(child2)>s_new:
				s_new=self.fitness(child2)
			new_generation.append(Chromosome(child1, self.fitness(child1)))
			new_generation.append(Chromosome(child2, self.fitness(child2)))

		return new_generation,s_new


	def take_n_random_elements(self, n, limit):
		array = range(limit)
		random.shuffle(array)
		array = array[:n]
		array.sort()
		return array 


	def crossover(self, a, b):
		n = self._num_cut_points
		cross_points = self.take_n_random_elements(n, len(a))
		previous = 0
		ind = True
		ab = []
		ba = []
		for i in range(n):
			if ind:
				ab += a[previous:cross_points[i]]
				ba += b[previous:cross_points[i]] 
			else:
				ab += b[previous:cross_points[i]]
				ba += a[previous:cross_points[i]]
			previous = cross_points[i]
			ind = not ind
		
		if ind:
			ab += a[previous:]
			ba += b[previous:]
		else:
			ab += b[previous:]
			ba += a[previous:]
			
		return (ab, ba)

	def mutation(self, chromosome):
		if not self._current_iteration % 20:
			self._mutation_rate -= 0.05
		mutation_param = random.random()
		if mutation_param <= self._mutation_rate:
			mutated_gene = int(random.choice(chromosome))
			chromosome[mutated_gene] = np.abs(int(chromosome[mutated_gene]) - 1)
			
		return chromosome

	def selection(self, chromosomes):
		the_sum = sum(chromosome.fitness for chromosome in chromosomes)
		selected_chromos = []

		selected_chromos = [
			self.selection_roulette_pick_one(chromosomes, the_sum)
			for i in range(self._reproduction_size)]

		return selected_chromos


	def selection_roulette_pick_one(self, chromosomes, the_sum):
		pick = random.uniform(0, the_sum)
		value = 0
		i = 0
		for chromosome in chromosomes:
			i += 1
			value += chromosome.fitness
			if value > pick:
				return chromosome

	def fitness(self, chromosome):
		return sum(chromosome)


	def take_random_element(self, fromHere):
		i = random.randrange(0, len(fromHere))
		return fromHere[i]

	def initial_population(self):
		init_pop = []
		param = 3
		for i in range(self._generation_size):
			A = {}
			v_i_ajdlist = []
			# we don't want an isolated vertex because it's not part of a clique
			while not v_i_ajdlist:
				v_i = random.choice(self._graph.vertices.keys()[:param])
				v_i_ajdlist = self._graph.vertices[v_i]
				
			A[v_i] = v_i_ajdlist
			used = np.zeros(self._graph.length())
			while sum(used.tolist()) != len(v_i_ajdlist):
				v_j = random.choice(v_i_ajdlist)
				if used[int(v_j)]:
					continue
				if(self.connected(A, v_j)):
					A[v_j] = self._graph.vertices[v_j]
				used[int(v_j)] = 1
				
			content = [0] * self._graph.length()
			for v in A:
				content[int(v)] = 1
			chromo = Chromosome(content, self.fitness(content))
			init_pop.append(chromo)
		
		return init_pop

	def stop_condition(self):
		return self._current_iteration > self._iterations or self._stagnancy_counter>=self._stagnancy_parameter

class Chromosome:
	def __init__(self, content, fitness):
		self.content = content
		self.fitness = fitness
	def __str__(self): return "%s f=%d" % (self.content, self.fitness)
	def __repr__(self): return "%s f=%d" % (self.content, self.fitness)


if __name__ == "__main__":
	graph = Graph("input3.json")
	graph.print_graph()
	genetic = GeneticAlgorithm(graph)
	dt = datetime.now()
	time_start = dt.microsecond
	solution = genetic.optimize()
	global time_elapsed
	dt = datetime.now()
	time_stop = dt.microsecond
	time_elapsed = time_stop-time_start
	print("Solution: %s fitness: %d" % (solution.content, solution.fitness))
	print "Time elapsed: " + str(time_elapsed) + " microseconds"