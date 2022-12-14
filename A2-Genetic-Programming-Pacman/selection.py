from itertools import accumulate
import random

# Parent selection functions---------------------------------------------------
def uniform_random_selection(population, n, **kwargs):
    return random.choices(population, k=n)

def k_tournament_with_replacement(population, n, k, **kwargs):
    return [max(random.sample(population, k), key=lambda x: x.fitness) for _ in range(n)]

def fitness_proportionate_selection(population, n, **kwargs):
    min_fitness = min(population, key=lambda x: x.fitness).fitness
    if min_fitness <= 0:
        if all(member.fitness == 0 for member in population):
            return random.choices(population, k=n)
        else:
            return random.choices(
                population, weights=[member.fitness - 1.5 * min_fitness for member in population], k=n
            )
    else:
        return random.choices(population, weights=[member.fitness for member in population], k=n)


# Survival selection functions-------------------------------------------------
def truncation(population, n, **kwargs):
    return sorted(population, key=lambda x: x.fitness, reverse=True)[:n]

def k_tournament_without_replacement(population, n, k, **kwargs):
    survivors = []
    population = population.copy()
    for _ in range(n):
        survivor = max(random.sample(population, k), key=lambda x: x.fitness)
        survivors.append(survivor)
        population.remove(survivor)
    return survivors

# Yellow deliverable parent selection function---------------------------------
def stochastic_universal_sampling(population, n, **kwargs):
    min_fitness = min(population, key=lambda x: x.fitness).fitness
    if min_fitness <= 0:
        if all(member.fitness == 0 for member in population):
            weights = [1 for _ in range(len(population))]
        else:
            weights = [member.fitness - 1.5 * min_fitness for member in population]
    else:
        weights = [member.fitness for member in population]

    cum_weights = list(accumulate(weights))
    cum_weights = [weight / cum_weights[-1] for weight in cum_weights]

    i = 0
    r = random.uniform(0, 1 / n)
    parents = []

    while len(parents) < n:
        while r <= cum_weights[i]:
            parents.append(population[i])
            r += 1 / n
        i += 1

    return parents
