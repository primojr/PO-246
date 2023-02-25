import numpy as np
from numpy.random import RandomState
from operator import itemgetter

# Define a função objetivo do KP
def kp_objective_function(weights, values, capacity, solution):
    weight = np.sum(solution * weights)
    if weight > capacity:
        return -np.inf
    else:
        return np.sum(solution * values)

# Define a função de decodificação
def decode_chromosome(chromosome, elite_proportion, num_items):
    elite_size = int(np.round(num_items * elite_proportion))
    elite_items = sorted(range(num_items), key=lambda i: chromosome[i], reverse=True)[:elite_size]
    solution = np.zeros(num_items, dtype=int)
    solution[elite_items] = 1
    return solution

# Define a função BRKGA
def brkga(num_items, weights, values, capacity, num_generations, population_size, elite_proportion, mutant_proportion, random_seed):
    # Inicializa o gerador de números aleatórios
    rng = RandomState(random_seed)

    # Define o tamanho das subpopulações
    p = int(np.round(population_size / 2))
    q = population_size - p

    # Gera a população inicial
    population = np.zeros((population_size, num_items), dtype=float)
    for i in range(population_size):
        population[i] = rng.uniform(size=num_items)

    # Define as probabilidades de cópia para as subpopulações elite e não-elite
    elite_crossover = 0.7
    mutant_crossover = 0.4

    # Define as probabilidades de mutação
    insertion_probability = 0.1
    flip_probability = 0.05

    # Executa as gerações
    for generation in range(num_generations):
        # Decodifica as soluções da população
        solutions = [decode_chromosome(chromosome, elite_proportion, num_items) for chromosome in population]

        # Avalia as soluções
        fitness_values = [kp_objective_function(weights, values, capacity, solution) for solution in solutions]

        # Ordena a população pelo fitness
        population = population[np.argsort(fitness_values)[::-1]]

        # Gera as subpopulações elite e não-elite
        elite_population = population[:p]
        non_elite_population = population[p:]

        # Gera as subpopulações mutante e não-mutante
        mutant_population = np.zeros((q, num_items), dtype=float)
        for i in range(q):
            # Seleciona um indivíduo da subpopulação elite
            elite_index = rng.randint(p)
            elite_chromosome = elite_population[elite_index]

            # Gera o cromossomo mutante
            mutant_chromosome = elite_chromosome.copy()
            for j in range(num_items):
                if rng.uniform() < flip_probability:
                    mutant_chromosome[j] = 1 - mutant_chromosome[j]
            for j in range(num_items):
                if rng.uniform() < insertion_probability:
                    k = rng.randint(num_items)
                    mutant_chromosome[j], mutant_chromosome[k] = mutant_chromosome[k], mutant_chromosome[j]

            mutant_population[i] = mutant_chromosome

        non_mutant_population = non_elite_population[:q]

        # Combina as subpopulações elite e mutante
        elite_chromosomes = sorted(elite_population, key=lambda x: -kp_objective_function(weights, values, capacity

