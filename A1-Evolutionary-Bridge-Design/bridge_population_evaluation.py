from bridge_fitness import *

# 1b TODO: evaluate the population and assign fitness and bridge as described in the Assignment 1b notebook
def basic_population_evaluation(population, **fitness_kwargs):
    for genotype in population:
        genotype.fitness, genotype.bridge = basic_simulation(genotype.gene, **fitness_kwargs)

# 1c TODO: evaluate the population and assign fitness, raw_fitness, and bridges as described in the constraint satisfaction segment of Assignment 1c
def constraint_satisfaction_population_evaluation(population, penalty_coefficient, yellow = None, **fitness_kwargs):
    if yellow == None:
        for genotype in population:
            (
                genotype.raw_fitness,
                unpenalized_fitness,
                violations,
                genotype.bridge,
            ) = constraint_satisfaction_simulation(genotype.gene, **fitness_kwargs)

            genotype.penalized_fitness = unpenalized_fitness - penalty_coefficient * violations
    else:
        # YELLOW deliverable logic goes here
        pass

# 1c TODO: evaluate the population and assign objectives and bridges as described in the multi-objective segment of Assignment 1c
def multi_objective_population_evaluation(population, yellow = None, red = None, **fitness_kwargs):
    for genotype in population:
        genotype.objectives, genotype.bridge = multi_objective_simulation(genotype.gene, **fitness_kwargs)