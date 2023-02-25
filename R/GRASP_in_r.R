library(TSP)
library(ggplot2)

# Define a função objetivo do TSP
tsp_objective_function <- function(dist_matrix, solution) {
  sum(dist_matrix[solution[-length(solution)], solution[-1]]) + dist_matrix[solution[length(solution)], solution[1]]
}

# Define a função de construção da solução inicial
greedy_construction <- function(dist_matrix, alpha) {
  n <- nrow(dist_matrix)
  candidates <- 1:n
  solution <- sample(candidates, 1)
  candidates <- candidates[-solution]
  while (length(candidates) > 0) {
    dist_values <- dist_matrix[solution[length(solution)], candidates]
    max_dist <- max(dist_values)
    min_dist <- quantile(dist_values, alpha)
    eligible <- candidates[which(dist_matrix[solution[length(solution)], candidates] <= min_dist)]
    next_node <- sample(eligible, 1)
    solution <- c(solution, next_node)
    candidates <- candidates[-which(candidates == next_node)]
  }
  return(solution)
}

# Define a função de busca local
two_opt <- function(dist_matrix, solution) {
  n <- length(solution)
  best_distance <- tsp_objective_function(dist_matrix, solution)
  improved <- TRUE
  while (improved) {
    improved <- FALSE
    for (i in 1:(n-2)) {
      for (j in (i+1):n) {
        if (j - i == 1) {
          next
        }
        new_solution <- solution
        new_solution[i:(j-1)] <- rev(solution[i:(j-1)])
        new_distance <- tsp_objective_function(dist_matrix, new_solution)
        if (new_distance < best_distance) {
          solution <- new_solution
          best_distance <- new_distance
          improved <- TRUE
        }
      }
    }
  }
  return(solution)
}

# Define a função GRASP
grasp <- function(dist_matrix, alpha, max_iterations) {
  best_solution <- NULL
  best_distance <- Inf
  for (i in 1:max_iterations) {
    candidate <- greedy_construction(dist_matrix, alpha)
    candidate <- two_opt(dist_matrix, candidate)
    candidate_distance <- tsp_objective_function(dist_matrix, candidate)
    if (candidate_distance < best_distance) {
      best_solution <- candidate
      best_distance <- candidate_distance
    }
  }
  return(list(solution=best_solution, distance=best_distance))
}

# Define a matriz de distâncias
dist_matrix <- as.matrix(
    dist(
      cbind(
        c(0, 10, 15, 20),
        c(10, 0, 35, 25),
        c(15, 35, 0, 30),
        c(20, 25, 30, 0)
        )
      )
    )

# Define os parâmetros do GRASP
alpha <- 0.3
max_iterations <- 100

# Executa o algoritmo GRASP
result <- grasp(dist_matrix, alpha, max_iterations)

# Plota o resultado
solution_df <- data.frame(
    x=c(0, 10, 15, 20)[result$solution],
    y=c(0, 10, 15, 20)[result$solution]
    )

ggplot(solution_df, aes(x, y)) + geom_path() + geom_point
