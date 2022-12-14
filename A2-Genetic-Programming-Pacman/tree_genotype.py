from abc import ABC, abstractmethod
from copy import deepcopy
from functools import cache
import random


@cache
def manhattan_distance(start, *end):
    return min(sum(abs(coord[0] - coord[1]) for coord in zip(list(start), list(end_pt))) for end_pt in end)


class Node(ABC):
    name = None
    depth = None
    height = None
    size = None

    def __init__(self, depth):
        self.depth = depth

    @abstractmethod
    def print(self, depth: int):
        pass

    @abstractmethod
    def eval(self, state: dict):
        pass


class NodeWrapper:
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __getattr__(self, attr):
        return getattr(self._wrapped, attr)

    def __setattr__(self, attr, value):
        if attr != "_wrapped":
            setattr(self._wrapped, attr, value)
        else:
            self.__dict__["_wrapped"] = value

    def __deepcopy__(self, memo: dict):
        return self.__class__(deepcopy(self._wrapped, memo))


class InternalNode(Node, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        return manhattan_distance(state['players']['m'], *[state['players'][ghost] for ghost in ghosts])


class PillNode(LeafNode):
    name = "P"

    def eval(self, state: dict):
        return manhattan_distance(state['players']['m'], *state['pills'])


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
    operators: list
    inputs: list

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.root = None
        self.operators = [AddNode, SubNode, MultNode, DivNode, RandNode]
        self.inputs = [GhostNode, PillNode, WallNode, FruitNode, FloatNode]

    def print(self):
        """The string representation of the tree."""
        return self.root.print(0).strip()

    def eval(self, state: dict):
        """Evaluate the tree."""
        return self.root.eval(state)

    def full_init(self):
        """Randomly initialize the tree using the full method."""
        self.root = self._full_init_helper(0)
        return self

    def _full_init_helper(self, depth):
        """Recursive helper for full method."""
        if depth == self.max_depth:
            return NodeWrapper(random.choice(self.inputs)(depth))
        else:
            curr_node = NodeWrapper(random.choice(self.operators)(depth))
            curr_node.left = self._full_init_helper(depth + 1)
            curr_node.right = self._full_init_helper(depth + 1)
            return curr_node

    def grow_init(self):
        """Randomly initialize the tree using the grow method."""
        self.root = self._grow_init_helper(0)
        return self

    def _grow_init_helper(self, depth):
        """Recursive helper for grow method"""
        if depth == self.max_depth:
            return NodeWrapper(random.choice(self.inputs)(depth))
        elif depth == 0:
            node = NodeWrapper(random.choice(self.operators)(depth))
            node.left = self._grow_init_helper(depth + 1)
            node.right = self._grow_init_helper(depth + 1)
            return node
        else:
            node = NodeWrapper(random.choice(self.inputs + self.operators)(depth))
            if isinstance(node._wrapped, InternalNode):
                node.left = self._grow_init_helper(depth + 1)
                node.right = self._grow_init_helper(depth + 1)
            return node

    def node_iter(self):
        """Iterate over all nodes in the tree."""
        return self._node_iter_helper(self.root)

    def _node_iter_helper(self, node: Node):
        """Recursive helper for tree iterator."""
        if isinstance(node._wrapped, InternalNode):
            yield from self._node_iter_helper(node.left)
            yield from self._node_iter_helper(node.right)
        yield node

    def count(self):
        """Obtain the number of nodes in the tree."""
        return self._count_helper(self.root)

    def _count_helper(self, node: Node):
        """Recursive helper for the node counter."""
        if isinstance(node._wrapped, InternalNode):
            node.size = self._count_helper(node.left) + self._count_helper(node.right) + 1
        else:
            node.size = 1
        return node.size

    def height(self):
        """Obtain the height of every node in the tree."""
        return self._height_helper(self.root)

    def _height_helper(self, node: Node):
        """Recursive helper for the node height finder."""
        if isinstance(node._wrapped, InternalNode):
            node.height = max(self._height_helper(node.left), self._height_helper(node.right)) + 1
        else:
            node.height = 0
        return node.height

    def select(self, idx: int):
        """Select a node from the tree given an index."""
        return self._select_helper(self.root, idx)

    def _select_helper(self, node: Node, nth: int):
        """Recursive helper for select node."""
        left_size = node.left.size if isinstance(node._wrapped, InternalNode) else 0

        if nth == left_size:
            return node
        elif nth < left_size:
            return self._select_helper(node.left, nth)
        else:
            return self._select_helper(node.right, nth - left_size - 1)


class TreeGenotype:
    def __init__(self):
        self.fitness = None
        self.gene = None

    def print(self):
        return self.gene.print()

    def recombine(self, mate, **kwargs):
        child = self.__class__()
        child.gene = deepcopy(self.gene)

        rand_node = child.gene.select(random.randrange(child.gene.count()))

        # find height for each node to enforce max depth
        mate.gene.height()
        potential_nodes = [
            node for node in mate.gene.node_iter() if rand_node.depth + node.height <= mate.gene.max_depth
        ]
        if potential_nodes:
            recomb_node = random.choice(
                [node for node in mate.gene.node_iter() if rand_node.depth + node.height <= kwargs["depth_limit"]]
            )

            rand_node._wrapped = deepcopy(recomb_node._wrapped)

        return child

    def mutate(self, **kwargs):
        copy = self.__class__()
        copy.gene = deepcopy(self.gene)

        copy.gene.max_depth = kwargs["depth_limit"]

        # get random node in place
        rand_node = copy.gene.select(random.randrange(copy.gene.count()))
        # re-generate tree from and including the randomly selected node
        rand_node._wrapped = copy.gene._grow_init_helper(rand_node.depth)._wrapped

        return copy

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
