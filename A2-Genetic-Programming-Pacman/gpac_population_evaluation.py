from itertools import cycle
import random
from statistics import mean

from fitness import *


def basic_population_evaluation(population, parsimony_coefficient, **fitness_kwargs):
    for member in population:
        fitness, log = play_GPac(member.gene, **fitness_kwargs)
        member.raw_fitness, member.fitness, member.log = fitness, fitness - parsimony_coefficient * member.gene.count(), log


def competitive_population_evaluation(
        pac_population, ghost_population, pac_parsimony_coefficient, ghost_parsimony_coefficient, **fitness_kwargs
):
    num_evals = max(len(pac_population), len(ghost_population))

    for species in (pac_population, ghost_population):
        for member in species:
            member.raw_fitness = []
            member.fitness = []
            member.log = []

    random.shuffle(pac_population)
    random.shuffle(ghost_population)

    for _, pac, ghost in zip(range(num_evals), cycle(pac_population), cycle(ghost_population)):
        fitness, log = play_GPac(pac.gene, ghost.gene, **fitness_kwargs)

        ghost_fitness = int(log[-1].split()[1]) - fitness

        pac.raw_fitness.append(fitness)
        ghost.raw_fitness.append(ghost_fitness)

        pac.log.append(log)
        ghost.log.append(log)

        pac.fitness.append(fitness - pac_parsimony_coefficient * pac.gene.count())
        ghost.fitness.append(ghost_fitness - ghost_parsimony_coefficient * ghost.gene.count())

    for species in (pac_population, ghost_population):
        for member in species:
            member.log = member.log[max((i for i in range(len(member.log))), key = lambda x: member.raw_fitness[x])]
            member.raw_fitness = mean(member.raw_fitness)
            member.fitness = mean(member.fitness)

    return num_evals

