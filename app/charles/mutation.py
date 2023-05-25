from random import random, randint, sample

from .charles import Individual


def binary_mutation(individual) -> Individual:
    """Binary mutation for a GA individual. Flips the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_index = randint(0, len(individual) - 1)

    if individual[mut_index] == 0:
        individual[mut_index] = 1
    elif individual[mut_index] == 1:
        individual[mut_index] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")
    return individual


def swap_mutation(individual) -> Individual:
    """Swap mutation for a GA individual. Swaps the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual


def inversion_mutation(individual) -> Individual:
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


def random_position_mutation(individual) -> Individual:
    """
    Mutate the individual by randomly changing the positions of its elements.

    This mutation function randomly selects elements from the individual's representation and changes their positions
    to new random positions within the valid range.

    Args:
        individual (Individual): A GA individual from charles.py

    Example:
        >>> individual = Individual(representation=[0, 1, 2, 3, 4, 5, 6, 7])
        >>> sol_size = 8
        >>> mutatated_individual = Individual(representation=[1, 4, 6, 5, 2, 3, 0, 7])

    Returns:
        Individual: Mutated Individual
    """
    sol_size = len(individual.representation)

    for i in range(sol_size):
        # Randomly select a new position for the element
        new_position = randint(0, sol_size - 1)

        # Change the position of the element
        individual.representation[i] = new_position

    return individual
















