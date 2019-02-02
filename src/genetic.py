import random, string
import sys, os
from Graph import Graph

class GeneticAlgorithm:
    def __init__(self, target):
        self._target = target 
        self._target_size = len(target)
        self._allowed_gene_values = set([0, 1])
        
        self._iterations = 1000   
        self._generation_size = 5000    
        self._mutation_rate = 0.01      
        self._reproduction_size = 1000  
        self._current_iteration = 0     
        self._top_chromosome = None    


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
        while len(new_generation) < self._generation_size:
            parents = random.sample(for_reproduction, 2)
            child1, child2 = self.crossover(parents[0].content, parents[1].content)

            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            new_generation.append(Chromosome(child1, self.fitness(child1)))
            new_generation.append(Chromosome(child2, self.fitness(child2)))

        return new_generation


    def crossover(self, a, b):
		pass

    def mutation(self, chromosome):
		pass

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
		pass


    def take_random_element(self, fromHere):
        i = random.randrange(0, len(fromHere))
        return fromHere[i]


    def initial_population(self):
		pass

    def stop_condition(self):
        return self._current_iteration > self._iterations or self._top_chromosome != None


class Chromosome:
    def __init__(self, content, fitness):
        self.content = content
        self.fitness = fitness
    def __str__(self): return "%s f=%d" % (self.content, self.fitness)
    def __repr__(self): return "%s f=%d" % (self.content, self.fitness)


if __name__ == "__main__":
    genetic = GeneticAlgorithm(graph)
    solution = genetic.optimize()
    print("Solution: %s fitness: %d" % (solution.content, solution.fitness))