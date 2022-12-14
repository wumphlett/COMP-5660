from collections import defaultdict


def dominates(A, B):
    return (
        all(a_obj >= b_obj for a_obj, b_obj in zip(A.objectives, B.objectives))
        and any(a_obj > b_obj for a_obj, b_obj in zip(A.objectives, B.objectives))
    )


def non_domination_sort(population, yellow=False, **kwargs):
    fronts = defaultdict(set)

    for member in population:
        member.dominates = set()
        member.dominated_by = 0
        for opponent in population:
            if dominates(member, opponent):
                member.dominates.add(opponent)
            elif dominates(opponent, member):
                member.dominated_by += 1
        if member.dominated_by == 0:
            member.rank = 0
            fronts[member.rank].add(member)

    i = 0
    while fronts[i]:
        next_front = set()
        for member in fronts[i]:
            for opponent in member.dominates:
                opponent.dominated_by -= 1
                if opponent.dominated_by == 0:
                    opponent.rank = i + 1
                    next_front.add(opponent)
        i += 1
        fronts[i] = next_front

    for front, population in fronts.items():
        for member in population:
            member.fitness = -front

    if yellow:
        # yellow deliverable code goes here
        pass