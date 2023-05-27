from random import randint, uniform


def single_point_co(p1_genes: list, p2_genes: list) -> tuple:
    """Perform crossover between two parents to generate offspring.

    Args:
        p1_genes (list): Genes of parent 1
        p2_genes (list): Genes of parent 2

    Returns:
        tuple: Two offspring

    Example:
        p1_genes = [0, 1, 2, 3, 4, 5, 6, 7]
        p2_genes = [3, 7, 0, 2, 6, 5, 1, 4]
        crossover_point = 3
        offspring1 = [0, 1, 2, 2, 6, 5, 1, 4]
        offspring2 = [3, 7, 0, 3, 4, 5, 6, 7]
    """

    # Get the size of the parents
    size = len(p1_genes)

    # Randomly select a crossover point
    crossover_point = randint(1, size - 2)  # Exclude the last index to avoid empty offspring

    # Perform single-point crossover with fixed crossover point
    offspring1 = p1_genes[:crossover_point] + p2_genes[crossover_point:]
    offspring2 = p2_genes[:crossover_point] + p1_genes[crossover_point:]

    return offspring1, offspring2


def cycle_xo(p1_genes: list, p2_genes: list) -> tuple:
    """Perform cycle crossover between two parents to generate offspring.

    Args:
        p1_genes (list): Genes of parent 1
        p2_genes (list): Genes of parent 2

    Returns:
        tuple: Two offspring

    Example:
        p1_genes = [0, 1, 2, 3, 4, 5, 6, 7]
        p2_genes = [3, 7, 0, 2, 6, 5, 1, 4]
        offspring1 = [0, 7, 2, 3, 4, 5, 6, 1]
        offspring2 = [3, 1, 0, 2, 6, 5, 7, 4]
    """

    # Get the size of the parents
    size = len(p1_genes)

    # offspring placeholders
    offspring1 = [None] * size
    offspring2 = [None] * size

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1_genes[index]
        val2 = p2_genes[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1_genes[index]
            offspring2[index] = p2_genes[index]
            val2 = p2_genes[index]
            index = p1_genes.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2_genes[index]
                    offspring2[index] = p1_genes[index]

    return offspring1, offspring2


def pmx(p1_genes: list, p2_genes: list) -> tuple:
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes.

    Args:
        p1_genes (list): Genes of parent 1
        p2_genes (list): Genes of parent 2

    Returns:
        tuple: Two offspring

    Example:
        p1_genes = [0, 1, 2, 3, 4, 5, 6, 7]
        p2_genes = [3, 7, 0, 2, 6, 5, 1, 4]
        offspring1 = [0, 7, 2, 3, 4, 5, 6, 1]
        offspring2 = [3, 1, 0, 2, 6, 5, 7, 4]
    """
    # Get the size of the parents
    size = min(len(p1_genes), len(p2_genes))
    offspring1, offspring2 = [0] * size, [0] * size

    # Initialize the position of each index in the individuals
    for i in range(size):
        offspring1[p1_genes[i]] = i
        offspring2[p2_genes[i]] = i

    # Choose crossover points
    cx_point1 = randint(0, size)
    cx_point2 = randint(0, size - 1)

    # Ensure that crossover points are different
    if cx_point2 >= cx_point1:
        cx_point2 += 1
    else:  # Swap the two cx points
        cx_point1, cx_point2 = cx_point2, cx_point1

    # Apply crossover between cx points
    for i in range(cx_point1, cx_point2):
        # Keep track of the selected values
        temp1 = p1_genes[i]
        temp2 = p2_genes[i]

        # Swap the matched value
        p1_genes[i], p1_genes[offspring1[temp2]] = temp2, temp1
        p2_genes[i], p2_genes[offspring2[temp1]] = temp1, temp2

        # Position bookkeeping
        offspring1[temp1], offspring1[temp2] = offspring1[temp2], offspring1[temp1]
        offspring2[temp1], offspring2[temp2] = offspring2[temp2], offspring2[temp1]

    return p1_genes, p2_genes


def arithmetic_xo(p1_genes: list, p2_genes: list, discrete: bool = True) -> tuple:
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    @TODO Implement passing discrete as option in case of geometric crossover
    Args:
        p1_genes (list): Genes of parent 1
        p2_genes (list): Genes of parent 2
        discrete (bool, optional): Whether to round the offspring to the nearest integer. Defaults to True.

    Returns:
        tuple: Two offspring
    """
    # Get the size of the parents
    size = len(p1_genes)
    alpha = uniform(0, 1)
    offspring1 = [None] * size
    offspring2 = [None] * size

    for i in range(size):
        offspring1[i] = p1_genes[i] * alpha + (1 - alpha) * p2_genes[i]
        offspring2[i] = p2_genes[i] * alpha + (1 - alpha) * p1_genes[i]

        if discrete:
            offspring1[i] = round(offspring1[i])
            offspring2[i] = round(offspring2[i])

    return offspring1, offspring2

