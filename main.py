from CNF_Creator import CNF_Creator
from Genentic_Algorithm import Genetic_Algorithm
from Print_Result import Print_Result

#constants
MODEL_SIZE = 50
POPULATION_SIZE = 20
M = 100

#contraints
MAX_FITNESS = 100
MAX_TIME = 45
MAX_EPOCHS_CONVERGANCE = 1000
INITIAL_MUTATION_PROBABILITY = 0.4

#generate sentence
cnfC = CNF_Creator(n = MODEL_SIZE)
#sentence = cnfC.CreateRandomSentence(M) 

#read sentence
sentence = cnfC.ReadCNFfromCSVfile()

#Genetic Algorithm
best_model, best_fitness, duration = Genetic_Algorithm.evolve(sentence, POPULATION_SIZE, MODEL_SIZE, INITIAL_MUTATION_PROBABILITY, MAX_FITNESS, MAX_TIME, MAX_EPOCHS_CONVERGANCE)
Print_Result.print_result(sentence, best_model, best_fitness, duration)