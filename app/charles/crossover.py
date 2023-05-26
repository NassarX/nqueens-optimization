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
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.

    Args:
        p1 (Individual): The first individual participating in the crossover.
        p2 (Individual): The second individual participating in the crossover.

    Returns:
    :returns: A tuple of two individuals.

    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes.
    """
    ind1 = p1.representation.copy()
    ind2 = p2.representation.copy()

    size = min(len(ind1), len(ind2))
    offspring1, offspring2 = [0] * size, [0] * size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        offspring1[ind1[i]] = i
        offspring2[ind2[i]] = i

    # Choose crossover points
    cxpoint1 = randint(0, size)
    cxpoint2 = randint(0, size - 1)

    # Ensure that crossover points are different
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]

        # Swap the matched value
        ind1[i], ind1[offspring1[temp2]] = temp2, temp1
        ind2[i], ind2[offspring2[temp1]] = temp1, temp2

        # Position bookkeeping
        offspring1[temp1], offspring1[temp2] = offspring1[temp2], offspring1[temp1]
        offspring2[temp1], offspring2[temp2] = offspring2[temp2], offspring2[temp1]

    # Create new individual from the offspring
    ind1 = Individual(representation=ind1)
    ind2 = Individual(representation=ind2)

    return ind1, ind2


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
