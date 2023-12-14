from nowy import GameTheory
import random
import json
from copy import deepcopy

class GeneticAlgorithm:
    def __init__(self,gameTheory: GameTheory,max_iterations=40) -> None:
        self.gameTheory = gameTheory
        self.K = gameTheory.K #roww 3
        self.M = gameTheory.M # column 5
        self.p = gameTheory.lista_podzadań
        self.population_size = 50
        self.max_iterations = max_iterations
        self.population = []
        self.parents = []
        self.children = []
        self.best_result = ()
        self.mutation_rate = 0.1

    def initialize_population(self):
        dictionary_of_vectors = {}
        for i in range(self.K):
            dictionary_of_vectors[i] = []
            for _ in range(self.population_size):
                dictionary_of_vectors[i].append(self.generate_random_vectors(self.p[i]))
        
        for i in range(self.population_size):
            temp = [[] for _ in range(self.K)]
            for j in range(self.K):
                temp[j]= dictionary_of_vectors[j][i]  
            funkcja_celu = self.gameTheory.Funkcja_celu_Z(temp)
            if funkcja_celu[2]:
                self.population.append((self.gameTheory.Funkcja_celu_Z(temp)))
        
        
            
        self.population = sorted(self.population, key=lambda x: x[0])
        self.best_result = deepcopy(self.population[0])
        
    
    def generate_random_vectors(self,i):
        vector = [0] * self.M
        indices = random.sample(range(self.M),i)

        for i in indices:
            vector[i] = 1
        
        return vector
    def choose_parents(self,):
        self.parents = []
        amount_of_parents = (len(self.population)*2//3)
        self.parents = deepcopy(self.population[:amount_of_parents])
        if not len(self.parents) % 2 == 0:
            self.parents.append(self.population[amount_of_parents])
        self.population = deepcopy(self.population[:amount_of_parents])

        random.shuffle(self.parents)
        self.parents = [(self.parents[i],self.parents[i+1]) for i in range(0,len(self.parents),2)]
        
    def crossover(self,parent1,parent2):
        #single point crossover
        point = random.randint(0,len(parent1[0]))
        child = [parent1[i][:point] + parent2[i][point:] for i in range(len(parent1))]
        self.children.append(child)

    def mutate(self,child):
        mutation_point = random.randint(0,len(child[0])-1)
        for row in child:
            mutation = random.uniform(0,1)
            if mutation > self.mutation_rate: 
                row[mutation_point] = 1 - row[mutation_point]

    def fix_kid(self,child):
        for i, row in enumerate(child):
            
            
            while sum(row) != self.p[i]:
                if sum(row) > self.p[i]:
                    indices_of_ones = [index for index, value in enumerate(row) if value == 1]
                    random_choice = random.choice(indices_of_ones)
                    row[random_choice] = 0

                elif sum(row) < self.p[i]:
                    indices_of_ones = [index for index, value in enumerate(row) if value == 0]
                    random_choice = random.choice(indices_of_ones)
                    row[random_choice] = 1
        healthy_kid = self.gameTheory.Funkcja_celu_Z(child)
        self.population.append(healthy_kid)    
        

    def run(self):
        self.initialize_population()
        for i in range(self.max_iterations):
            self.choose_parents()
            self.children = []
            for i in self.parents:
                self.crossover(i[0][1],i[1][1])
            
            for i in self.children:
                self.mutate(i)
            for i in self.children:
                self.fix_kid(i)
            if not self.population_size == len(self.population):
                del(self.population[ (len(self.population)*2//3)])
            self.population = sorted(self.population, key=lambda x: x[0])
            self.best_result = deepcopy(self.population[0])
            #sprawdzenie
            # print(self.best_result, self.gameTheory.Funkcja_celu_Z(self.best_result[1])) 
            # print(self.population)
            # print("***************************")

gra = GameTheory(
    3,
    5,
    [2, 3, 4],
    [1, 1.2, 1.5, 1.8, 2],
    [[6, 5, 4, 3.5, 3], [5, 4.2, 3.6, 3, 2.8], [4, 3.5, 3.2, 2.8, 2.4]],
    50,
    50,
    0.5,
    0.5,
    1,
)
a = GeneticAlgorithm(gra)

a.run()
# B = [[0, 1, 1, 0, 0], [0, 1, 1, 0, 1], [1, 0, 1, 1, 1]]
# print(gra.Funkcja_celu_Z(B))
