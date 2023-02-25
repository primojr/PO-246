import numpy as np

class BRKGA:
    def __init__(self, n, p, pe, pm, rhoe, decode, evaluate):
        self.n = n  # Tamanho da população
        self.p = p  # Tamanho da elite
        self.pe = pe  # Fração de pais da elite
        self.pm = pm  # Taxa de mutação
        self.rhoe = rhoe  # Taxa de atualização do melhor cromossomo
        self.decode = decode  # Função de decodificação do cromossomo
        self.evaluate = evaluate  # Função de avaliação da solução

        self.population = np.zeros((n, len(decode(0))), dtype=np.float64)
        self.prob = np.zeros(n, dtype=np.float64)
        self.indexes = np.zeros(n, dtype=np.int32)
        self.best = np.zeros(len(decode(0)), dtype=np.float64)
        self.best_fitness = float("-inf")

    def initialize_population(self):
        self.population = np.random.rand(self.n, len(self.population[0]))
        self.best = self.population[0].copy()

    def evolve(self, generations):
        for _ in range(generations):
            # Ordena a população pelo valor de fitness
            fitness = np.array([self.evaluate(self.decode(chromosome)) for chromosome in self.population])
            sorted_indexes = np.argsort(-fitness)
            self.population = self.population[sorted_indexes]
            fitness = fitness[sorted_indexes]

            # Atualiza o melhor cromossomo
            if fitness[0] > self.best_fitness:
                self.best_fitness = fitness[0]
                self.best = self.population[0].copy()

            # Seleciona os pais
            elite_size = int(self.p * self.n)
            non_elite_size = self.n - elite_size
            elite = self.population[:elite_size]
            non_elite = self.population[elite_size:]
            elite_fitness = fitness[:elite_size]
            non_elite_fitness = fitness[elite_size:]

            elite_prob = np.exp(elite_fitness - np.max(elite_fitness))
            elite_prob /= np.sum(elite_prob)

            non_elite_prob = np.exp(non_elite_fitness - np.max(non_elite_fitness))
            non_elite_prob /= np.sum(non_elite_prob)

            self.prob[:elite_size] = self.pe * elite_prob + (1 - self.pe) * non_elite_prob
            self.prob[elite_size:] = (1 - self.pe) * non_elite_prob

            self.indexes = np.random.choice(self.n, size=self.n, replace=True, p=self.prob)

            # Cria a nova geração
            offspring = np.empty_like(self.population)
            for i in range(self.n):
                parent1 = self.population[self.indexes[i]]
                if np.random.rand() < self.pm:
                    parent2 = self.best
                else:
                    parent2 = elite[np.random.randint(0, elite_size)]
                mask = np.random.rand(len(parent1)) < self.rhoe
                offspring[i] = parent1 * mask + parent2 * (1 - mask)

            self.population = offspring

    def get_best_solution(self):
        return self.best, self.best_fitness
