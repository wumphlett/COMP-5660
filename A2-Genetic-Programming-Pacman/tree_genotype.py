from abc import ABC, abstractmethod
import random


def manhattan_distance(start, end):
    return sum(abs(coord[0] - coord[1]) for coord in zip(list(start), list(end)))


class Node(ABC):
    name = None

    @abstractmethod
    def eval(self, state: dict):
        pass


class InternalNode(Node, ABC):
    def __init__(self):
        self.left = None
        self.right = None

    def print(self, depth):
        return f"\n{'|' * depth}{self.name}" + self.left.print(depth + 1) + self.right.print(depth + 1)


class LeafNode(Node, ABC):
    def print(self, depth):
        return f"\n{'|' * depth}{self.name}"


class AddNode(InternalNode):
    name = "+"

    def eval(self, state):
        return self.left.eval(state) + self.right.eval(state)


class SubNode(InternalNode):
    name = "-"

    def eval(self, state):
        return self.left.eval(state) - self.right.eval(state)


class MultNode(InternalNode):
    name = "*"

    def eval(self, state):
        return self.left.eval(state) * self.right.eval(state)


class DivNode(InternalNode):
    name = "/"

    def eval(self, state):
        denominator = self.right.eval(state)
        numerator = self.left.eval(state)

        if denominator == 0.:
            return 100 if numerator >= 0 else -100
        return numerator / denominator


class RandNode(InternalNode):
    name = "RAND"
    
    def eval(self, state):
        return random.uniform(self.left.eval(state), self.right.eval(state))


class GhostNode(LeafNode):
    name = "G"

    def eval(self, state: dict):
        ghosts = list(key for key in state['players'] if 'm' not in key)
        return min(manhattan_distance(state['players']['m'], state['players'][ghost]) for ghost in ghosts)


class PillNode(LeafNode):
    name = "P"

    def eval(self, state: dict):
        return min(manhattan_distance(state['players']['m'], pill) for pill in state['pills'])


class WallNode(LeafNode):
    name = "W"

    def eval(self, state: dict):
        wall_count = 0
        board = state['walls']
        pacman = state['players']['m']
        for x, y in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            try:
                if board[pacman[0] - x][pacman[1] - y] == 1:
                    wall_count += 1
            except IndexError:
                wall_count += 1
        return wall_count


class FruitNode(LeafNode):
    name = "F"

    def eval(self, state: dict):
        if state['fruit'] is None:
            return 100
        return manhattan_distance(state['players']['m'], state['fruit'])


class FloatNode(LeafNode):
    name = "#.#"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = random.uniform(-10., 10.)
        self.name = str(self.value)

    def eval(self, state: dict):
        return self.value


class ValueFunction:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.root = None
        self.operators = [AddNode, SubNode, MultNode, DivNode, RandNode]
        self.inputs = [GhostNode, PillNode, WallNode, FruitNode, FloatNode]

    def full_init(self):
        self.root = self.full_init_helper(1)
        return self

    def full_init_helper(self, depth):
        if depth == self.max_depth:
            return random.choice(self.inputs)()
        else:
            curr_node = random.choice(self.operators)()
            curr_node.left = self.full_init_helper(depth + 1)
            curr_node.right = self.full_init_helper(depth + 1)
            return curr_node

    def grow_init(self):
        self.root = self.grow_init_helper(1)
        return self

    def grow_init_helper(self, depth):
        if depth == self.max_depth:
            return random.choice(self.inputs)()
        else:
            curr_node = random.choice(self.inputs + self.operators)()
            if isinstance(curr_node, InternalNode):
                curr_node.left = self.grow_init_helper(depth + 1)
                curr_node.right = self.grow_init_helper(depth + 1)
            return curr_node

    def print(self):
        return self.root.print(0).strip()

    def eval(self, state: dict):
        return self.root.eval(state)



class TreeGenotype:
    def __init__(self):
        self.fitness = None
        self.gene = None

    def recombine(self, mate, **kwargs):
        child = self.__class__()

        # TODO: recombine genes of self and mate and assign to child's gene member variable
        pass

        return child

    def mutate(self, **kwargs):
        copy = self.__class__()

        # TODO: copy self.gene to copy.gene
        pass

        # TODO: mutate gene of copy
        pass

        return copy

    def print(self):
        return self.gene.print()

    @classmethod
    def initialization(cls, mu, *args, **kwargs):
        population = [cls() for _ in range(mu)]
        depth_limit = kwargs['depth_limit']
        idx = 0
        while idx < mu:
            for depth in range(2, depth_limit + 1):
                for method in ('full_init', 'grow_init'):
                    population[idx].gene = getattr(ValueFunction(depth), method)()
                    idx += 1
                    if idx == mu:
                        return population

        return population
