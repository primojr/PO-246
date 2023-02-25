import numpy as np
from numpy.random import RandomState
from operator import itemgetter

# Define a função objetivo
def objective_function(chromosome, weights, cover_matrix):
    total_weight = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_weight += weights[i]
            for j in range(cover_matrix.shape[1]):
                if cover_matrix[i, j] == 1:
                    chromosome[j] = 0
    return total_weight

# Define a função de decodificação
def decode_chromosome(chromosome):
    return [i for i, x in enumerate(chromosome) if x == 1]

# Define a função BRKGA
def brkga(num_genes, num_chromosomes, num_elite, num_mutants, num_generations, weights, cover_matrix, random_seed):
    # Inicializa o gerador de números aleatórios
    rng = RandomState(random_seed)

    # Gera a população inicial
    population = rng.randint(2, size=(num_chromosomes, num_genes))

    # Executa as gerações
    for generation in range(num_generations):
        # Avalia as soluções
        fitness_values = [objective_function(chromosome, weights, cover_matrix) for chromosome in population]

        # Ordena a população pelo fitness
        sorted_indices = np.argsort(fitness_values)[::-1]
        population = population[sorted_indices]

        # Gera a subpopulação elite
        elite_population = population[:num_elite]

        # Gera a subpopulação mutante
        mutant_population = np.zeros((num_mutants, num_genes), dtype=int)
        for i in range(num_mutants):
            # Seleciona dois cromossomos aleatórios da subpopulação elite
            elite_indices = rng.choice(num_elite, size=2, replace=False)
            elite_chromosomes = elite_population[elite_indices]

            # Realiza o crossover entre os cromossomos selecionados
            crossover_point = rng.randint(num_genes)
            mutant_chromosome = np.concatenate((elite_chromosomes[0][:crossover_point], elite_chromosomes[1][crossover_point:]))

            # Realiza a mutação no cromossomo
            for j in range(num_genes):
                if rng.uniform() < 1 / num_genes:
                    mutant_chromosome[j] = 1 - mutant_chromosome[j]

            mutant_population[i] = mutant_chromosome

        # Gera a nova população combinando a subpopulação elite e a subpopulação mutante
        population = np.concatenate((elite_population, mutant_population))

    # Decodifica a melhor solução encontrada
    best_chromosome = population[0]
    best_cover = decode_chromosome(best_chromosome)
    best_weight = objective_function(best_chromosome, weights, cover_matrix)

    return best_cover, best_weight

# 
# Para aplicar o BRKGA ao Problema do Recobrimento Máximo Ponderado,
# basta passar como entrada o número de genes (ou variáveis de decisão),
# o número de cromossomos, o número de cromossomos elite, 
# o número de cromossomos mutantes, o número de gerações, 
# os pesos de cada elemento e a matriz de cobertura. 
# O resultado da execução é a melhor solução encontrada
