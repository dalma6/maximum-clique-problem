import random, string
import numpy as np
import sys, os
from Graph import Graph

class GeneticAlgorithm:
	def __init__(self, graph):
		self._graph = graph 
		self._allowed_gene_values = set([0, 1])
		
		self._iterations = 1000
		self._generation_size = 50
		self._mutation_rate = 0.5	  
		self._reproduction_size = 1000  
		self._current_iteration = 0	 
		self._top_chromosome = None
		
		if self._graph.length() < 10:
			self._max_cut_points = self._graph.length() - 1
		else:
			self._max_cut_points = 10

		self._min_cut_points = 2
		self._num_cut_points = self._max_cut_points


	def optimize(self):
		chromosomes = self.initial_population()

		while not self.stop_condition():
			for_reproduction = self.selection(chromosomes)
			chromosomes = self.create_generation(for_reproduction)
			self._current_iteration += 1
		if self._top_chromosome:
			return Chromosome(self._top_chromosome, self.fitness(self._top_chromosome))
		else:
			return max(chromosomes, key=lambda chromo: chromo.fitness)


	def create_generation(self, for_reproduction):
		new_generation = []
		if self._num_cut_points > self._min_cut_points and self._current_iteration%20 == 0:
				self._num_cut_points -= 2
		while len(new_generation) < self._generation_size:
			parents = random.sample(for_reproduction, 2)
			child1, child2 = self.crossover(parents[0].content, parents[1].content)

			child1 = self.mutation(child1)
			child2 = self.mutation(child2)

			new_generation.append(Chromosome(child1, self.fitness(child1)))
			new_generation.append(Chromosome(child2, self.fitness(child2)))

		return new_generation


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


	def the_goal_function(self, chromosome):
		if chromosome == self._target:
			self._top_chromosome = chromosome


	def fitness(self, chromosome):
		return sum(chromosome)


	def take_random_element(self, fromHere):
		i = random.randrange(0, len(fromHere))
		return fromHere[i]

	def connected(self, A, v):
		for u in A:
			if v not in A[u]:
				return False
		return True

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
		return self._current_iteration > self._iterations or self._top_chromosome != None

class Chromosome:
	def __init__(self, content, fitness):
		self.content = content
		self.fitness = fitness
	def __str__(self): return "%s f=%d" % (self.content, self.fitness)
	def __repr__(self): return "%s f=%d" % (self.content, self.fitness)


if __name__ == "__main__":
	graph = Graph("input1.json")
	genetic = GeneticAlgorithm(graph)
	solution = genetic.optimize()
	print("Solution: %s fitness: %d" % (solution.content, solution.fitness))