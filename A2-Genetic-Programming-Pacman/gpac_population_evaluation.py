from fitness import *


def basic_population_evaluation(population, parsimony_coefficient, **fitness_kwargs):
    for member in population:
        fitness, log = play_GPac(member.gene, **fitness_kwargs)
        member.raw_fitness, member.fitness, member.log = fitness, fitness - parsimony_coefficient * member.gene.count(), log

# 2c TODO:  evaluate input Pac-Man and Ghost populations and assign fitness, raw_fitness, 
#           and log as described in the Assignment 2c notebook
def competitive_population_evaluation(  pac_population, ghost_population, 
                                        pac_parsimony_coefficient,
                                        ghost_parsimony_coefficient, **fitness_kwargs):
    # TODO: perform matchmaking
    pass

    # TODO: evaluate matches with play_GPac
    # Hint: play_GPac(pac_controller, ghost_controller, **fitness_kwargs)
    pass

    # TODO: calculate and assign fitness (don't forget the per-species parsimony penalty)
    pass