import random

from base_evolution import BaseEvolutionPopulation


class GeneticProgrammingPopulation(BaseEvolutionPopulation):
    def generate_children(self):
        children = []

        for _ in range(self.num_children):
            if random.random() < self.mutation_rate:
                parent = self.parent_selection(self.population, n=1, **self.parent_selection_kwargs)[0]
                children.append(parent.mutate(**self.mutation_kwargs))
            else:
                parent, mate = self.parent_selection(self.population, n=2, **self.parent_selection_kwargs)
                children.append(parent.recombine(mate, **self.recombination_kwargs))

        return children
