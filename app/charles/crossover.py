from .charles import Individual
from random import randint, sample, uniform


def single_point_co(p1: Individual, p2: Individual):
    """Perform crossover between two parents to generate offspring.

    Args:
        p1 (Individual): First parent.
        p2 (Individual): Second parent.

    Example:
        >>> p1 = Individual(representation=[0, 1, 2, 3, 4, 5, 6, 7])
        >>> p2 = Individual(representation=[3, 7, 0, 2, 6, 5, 1, 4])
        >>> crossover_point = 3
        >>> offspring1 = [0, 1, 2, 2, 6, 5, 1, 4]
        >>> offspring2 = [3, 7, 0, 3, 4, 5, 6, 7]
    Returns:
        Individual: Offspring generated through crossover.
    """
    size = len(p1)

    # Randomly select a crossover point
    crossover_point = randint(1, size - 2)  # Exclude the last index to avoid empty offspring

    # Perform single-point crossover with fixed crossover point
    offspring1 = p1[:crossover_point] + p2[crossover_point:]
    offspring2 = p2[:crossover_point] + p1[crossover_point:]

    # Create new individual from the offspring
    offspring1 = Individual(representation=offspring1)
    offspring2 = Individual(representation=offspring2)

    return offspring1, offspring2


def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    # Create new individual from the offspring
    offspring1 = Individual(representation=offspring1)
    offspring2 = Individual(representation=offspring2)

    return offspring1, offspring2


def pmx(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(p1)), 2)
    # xo_points = [3,6]
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * len(x)
        # offspring2
        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]]
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] is not None:
                temp = index
                index = y.index(x[temp])
            o[index] = i

        # numbers that doesn't exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    offspring1, offspring2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return offspring1, offspring2


def arithmetic_xo(p1, p2):
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    alpha = uniform(0, 1)
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)
    for i in range(len(p1)):
        offspring1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        offspring2[i] = p2[i] * alpha + (1 - alpha) * p1[i]

    # Create new individual from the offspring
    offspring1 = Individual(representation=offspring1)
    offspring2 = Individual(representation=offspring2)

    return offspring1, offspring2
