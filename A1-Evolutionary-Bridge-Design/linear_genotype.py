import random

class LinearGenotype():
    def __init__(self):
        self.fitness = None
        self.gene = None

    def random_initialization(self, length, x_bounds, y_bounds):
        self.gene = [
            (random.uniform(x_bounds[0], x_bounds[1]), random.uniform(y_bounds[0], y_bounds[1]))
            for _ in range(length)
        ]

    def recombine(self, mate, method, **kwargs):
        child = LinearGenotype()
        
        assert method.casefold() in {'uniform', '1-point crossover', 'bonus'}
        if method.casefold() == 'uniform':
            child.gene = []
            for i in range(len(self.gene)):
                child.gene.append(random.choice((self.gene[i], mate.gene[i])))
        elif method.casefold() == '1-point crossover':
            child.gene = self.gene.copy()
            for i in range(random.randrange(1, len(self.gene)), len(self.gene)):
                child.gene[i] = mate.gene[i]
        elif method.casefold() == 'bonus':
            ''' 
            This is a red deliverable (i.e., bonus for anyone).
            Implement the bonus crossover operator as described in deliverable
            Red 1 of Assignment 1b.
            '''
            pass

        return child

    def mutate(self, x_bounds, y_bounds, bonus=None, **kwargs):
        copy = LinearGenotype()
        copy.gene = self.gene.copy()
        
        if bonus is None:
            for i, member in enumerate(copy.gene):
                # Creeps locus values with a triangular distribution, bounded by provided bounds and centered at
                # the current value
                copy.gene[i] = (random.triangular(*x_bounds, member[0]), random.triangular(*y_bounds, member[1]))
        else:
            ''' 
            This is a red deliverable (i.e., bonus for anyone).
            Implement the bonus crossover operator as described in deliverable
            Red 1 of Assignment 1b.
            '''
            pass

        return copy

    @classmethod
    def initialization(cls, mu, *args, **kwargs):
        population = [cls() for _ in range(mu)]
        for i in range(len(population)):
            population[i].random_initialization(*args, **kwargs)
        return population