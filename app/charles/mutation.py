from random import randint, sample


def binary_mutation(genes) -> list:
    """Binary mutation for a GA individual. Flips a bit.

    Args:
        genes (list): Genes of an individual

    Returns:
        list: Mutated genes

    Example:
        genes = [0, 1, 0, 1, 1, 0, 1, 0]
        mutated_genes = [0, 1, 0, 1, 1, 0, 1, 1]
    """

    mut_index = randint(0, len(genes) - 1)

    if genes[mut_index] == 0:
        genes[mut_index] = 1
    elif genes[mut_index] == 1:
        genes[mut_index] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {genes}. But it's not binary.")
    return genes


def swap_mutation(genes) -> list:
    """Swap mutation for a GA individual. Swaps two genes.

    Args:
        genes (list): Genes of an individual

    Returns:
        list: Mutated genes

    Example:
       genes = [1, 2, 3, 4, 5, 6, 7, 8]
       mutated_genes = [1, 2, 3, 4, 5, 8, 7, 6]
    """

    mut_indexes = sample(range(0, len(genes)), 2)
    genes[mut_indexes[0]], genes[mut_indexes[1]] = genes[mut_indexes[1]], genes[mut_indexes[0]]
    return genes


def inversion_mutation(genes) -> list:
    """Inversion mutation for a GA individual. Inverts a subset of genes.

    Args:
        genes (list): Genes of an individual

    Returns:
        list: Mutated genes

    Example:
        genes = [1, 2, 3, 4, 5, 6, 7, 8]
        mutated_genes = [1, 2, 3, 4, 7, 6, 5, 8]
    """

    mut_indexes = sample(range(0, len(genes)), 2)
    mut_indexes.sort()
    genes[mut_indexes[0]:mut_indexes[1]] = genes[mut_indexes[0]:mut_indexes[1]][::-1]
    return genes


def random_position_mutation(genes) -> list:
    """Random position mutation for a GA individual. Randomly changes the position of an element.
        Mutate the individual by randomly changing the positions of its elements.
            This mutation function randomly selects elements from the individual's representation and changes their positions
            to new random positions within the valid range.
    Args:
        genes (list): Genes of an individual

    Returns:
        list: Mutated genes

    Example:
        genes = [1, 2, 3, 4, 5, 6, 7, 8]
        mutated_genes = [1, 2, 3, 4, 7, 6, 5, 8]
    """

    sol_size = len(genes)

    for i in range(sol_size):
        # Randomly select a new position for the element
        new_position = randint(0, sol_size - 1)

        # Change the position of the element
        genes[i], genes[new_position] = genes[new_position], genes[i]

    return genes
