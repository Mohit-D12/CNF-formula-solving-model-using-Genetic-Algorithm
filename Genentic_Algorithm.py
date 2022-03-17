from random import choices, randint, random, randrange
from time import time

class Genetic_Algorithm:
    
    #returns a randomly generated model 
    def generate_sample_model(self, model_size):
        return choices([0, 1], k = model_size)

    #returns a population array that contains randomly generated models
    def generate_population(self, population_size, model_size):
        return [self.generate_sample_model(model_size) for _ in range(population_size)]

    #calculates and returns fitness value for a model
    def calculate_fitness_value(self, sentence, model):

        total_clauses = len(sentence)
        true_clauses = 0

        for clause in sentence:
            for variable in clause:
                if (variable > 0 and model[variable-1]) or (variable < 0 and not model[-variable-1]):
                    true_clauses += 1
                    break

        return (true_clauses * 100)/total_clauses

    #returns 2 parents for crossing over based on fitness value as weight
    def selection_pair(self, sentence, population):
        
        #chooses 5 parents using their fitness value as there weights, then returns any 2 of them at random
        return choices(
            population = choices(
                population=population, 
                weights = [self.calculate_fitness_value(sentence, model) for model in population],
                k = 5
                ),
            k = 2)    

    #performs 1 point crossover of 2 models
    def single_point_crossover(self, parent_1, parent_2):

        #calculating range of crossover point
        lower_index, upper_index = 1, len(parent_1) - 1

        #randomly generating point of crossover
        p = randint(lower_index, upper_index)

        #generating childs after the crossover
        child1 = parent_1[:p] + parent_2[p:]
        child2 = parent_2[:p] + parent_1[p:]

        return child1, child2

    #mutates a random bit in model with a probability
    def mutate(self, model, probability):

        #randomly generate bit for mutation
        mutate_index = randrange(len(model))

        #mutate the selected bit according to given probability
        if random() < probability:
            model[mutate_index] = 1 - model[mutate_index]
        
        return model

    #performs genetic algorithm
    def evolve(self, sentence, population_size, model_size, mutation_probability, fitness_limit, time_limit, epoch_limit_convergance):

        #initialize variables
        population = self.generate_population(population_size, model_size)
        start_time = time.time()
        duration = 0
        epochs = 0

        converge_counter, converge_fitness = 0, 0
        best_fitness, best_model = 0, []

        while duration < time_limit:
            epochs += 1

            #sort population according to their fitness value
            population = sorted(population, key = lambda model: self.calculate_fitness_value(sentence, model), reverse=True)
            current_fitness = self.calculate_fitness_value(sentence, population[0])          #denotes best fitness in current population

            #check for convergence
            if converge_fitness == current_fitness:
                converge_counter += 1
            else:
                converge_counter = 1
                converge_fitness = current_fitness

            #storing best result so far
            if current_fitness >= best_fitness:
                best_fitness, best_model = current_fitness, population[0]

            if best_fitness >= fitness_limit or converge_counter > epoch_limit_convergance:
                break
            
            #generating next generation
            
            #next generation has 2 best parents from current generation and rest of the generated by single point crossover
            next_generation = population[0:2]
            for _ in range(len(population)//2 -1):
                parent_1, parent_2 = self.selection_pair(sentence, population)
                child_a, child_b = self.single_point_crossover(parent_1, parent_2)
                child_a = self.mutate(child_a, mutation_probability)
                child_b = self.mutate(child_b, mutation_probability)
                next_generation += [child_a, child_b]

                duration = time.time() - start_time
                if duration > time_limit:
                    break
            
            #update the current generation as next generation
            population = next_generation

            #debug
            #print(epochs, current_fitness)
        
        #perform fitness check on the last  set of population (as the loop broke before checking this batch)
        population = sorted(population, key = lambda model: self.calculate_fitness_value(sentence, model), reverse=True)
        current_fitness = self.calculate_fitness_value(sentence, population[0])
        if current_fitness >= best_fitness:
            best_fitness, best_model = current_fitness, population[0]

        #print the final result to console
        self.print_result(sentence, self.convert_to_printable(best_model), best_fitness, duration)
