import numpy as np
import matplotlib.pyplot as plt

# Define a função objetivo do TSP
def tsp_objective_function(dist_matrix, solution):
    return np.sum(dist_matrix[solution[:-1], solution[1:]]) + dist_matrix[solution[-1], solution[0]]

# Define a função de construção da solução inicial
def greedy_construction(dist_matrix, alpha):
    n = dist_matrix.shape[0]
    candidates = list(range(n))
    solution = [np.random.choice(candidates)]
    candidates.remove(solution[0])
    while candidates:
        dist_values = dist_matrix[solution[-1], candidates]
        max_dist = np.max(dist_values)
        min_dist = np.percentile(dist_values, alpha * 100)
        eligible = [c for c in candidates if dist_matrix[solution[-1], c] <= min_dist]
        next_node = np.random.choice(eligible)
        solution.append(next_node)
        candidates.remove(next_node)
    return np.array(solution)

# Define a função de busca local
def two_opt(dist_matrix, solution):
    n = dist_matrix.shape[0]
    best_distance = tsp_objective_function(dist_matrix, solution)
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 2):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue
                new_solution = solution.copy()
                new_solution[i:j] = solution[j-1:i-1:-1]
                new_distance = tsp_objective_function(dist_matrix, new_solution)
                if new_distance < best_distance:
                    solution = new_solution
                    best_distance = new_distance
                    improved = True
        solution = np.array(solution)
    return solution

# Define a função GRASP
def grasp(dist_matrix, alpha, max_iterations):
    best_solution = None
    best_distance = np.inf
    for i in range(max_iterations):
        candidate = greedy_construction(dist_matrix, alpha)
        candidate = two_opt(dist_matrix, candidate)
        candidate_distance = tsp_objective_function(dist_matrix, candidate)
        if candidate_distance < best_distance:
            best_solution = candidate
            best_distance = candidate_distance
    return best_solution, best_distance

# Define a matriz de distâncias
dist_matrix = np.array([[0, 10, 15, 20],
                        [10, 0, 35, 25],
                        [15, 35, 0, 30],
                        [20, 25, 30, 0]])

# Define os parâmetros do GRASP
alpha = 0.8
max_iterations = 100

# Executa o algoritmo GRASP
solution, distance = grasp(dist_matrix, alpha, max_iterations)

# Plota o resultado
x = np.array([0, 10, 15, 20])
y = np.array([0, 10, 15, 20])
plt.plot(x[solution], y[solution], 'o-r')
plt.show()

print(f'Melhor solução: {solution}')
print(f'Melhor distância: {distance}')
