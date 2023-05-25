from random import uniform, choice
from operator import attrgetter
from .charles import Individual


def fps(population) -> Individual:
    """Fitness proportionate selection implementation.

    Fitness proportionate selection(roulette wheel selection) It is a probabilistic selection method where
    individuals from a population are selected for reproduction based on their fitness values. The selection
    probability for each individual is proportional to its fitness value relative to the total fitness of the
    population.

    Steps:
    1. Calculate the total fitness of the population by summing up the fitness values of all individuals.
    2. Generate a random number, often called the "spin," between 0 and the total fitness.
    3. Iterate through the population and accumulate the fitness values.
        When the accumulated fitness surpasses the spin value, select the corresponding individual.
    4. Repeat the selection process until the desired number of individuals is selected.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual
    elif population.optim == "min":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += total_fitness - individual.fitness
            if position > spin:
                return individual
    else:
        raise Exception("No optimization specified (min or max).")


def tournament_selection(population, size=4) -> Individual:
    """Tournament selection implementation.

    In tournament selection, a small subset of individuals is randomly chosen from the population,
    and the one with the highest fitness value is selected as the parent.
    This process is repeated to select multiple parents.

    Steps: 1. Select Randomly subset of individuals from the population based on tournament size for participating in
    each tournament. 2. Select the individual with the highest (or lowest, depending on the optimization direction)
    fitness value as the winner of the tournament. 3. Return the selected individuals for the next generation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for _ in range(size)]

    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")


def rank_based_sel(population) -> Individual:
    """Rank-based selection implementation.

    Rank-Based Selection assigns selection probabilities based on the rank of individuals in the population,
    with higher ranks having higher probabilities.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual.
    """
    sorted_population = sorted(population.individuals, key=attrgetter("fitness"), reverse=population.optim == "max")
    total_rank = sum(range(1, len(sorted_population) + 1))
    spin = uniform(0, total_rank)
    position = 0

    for rank, individual in enumerate(sorted_population):
        position += rank + 1
        if position > spin:
            return individual


def stochastic_universal_sampling(population, num_parents) -> [Individual]:
    """Stochastic Universal Sampling (SUS) implementation.

     Stochastic Universal Sampling is a technique that selects parents
     by evenly distributing points along the cumulative probability distribution
     and selecting individuals that correspond to these points.

    Args:
        population (Population): The population we want to select from.
        num_parents (int): The number of parents to select.

    Returns:
        list: List of selected parents.
    """
    sorted_population = sorted(population.individuals, key=attrgetter("fitness"), reverse=population.optim == "max")
    total_fitness = sum(individual.fitness for individual in sorted_population)
    fitness_proportions = [individual.fitness / total_fitness for individual in sorted_population]

    # Calculate the cumulative probability distribution
    cumulative_probabilities = [sum(fitness_proportions[:i + 1]) for i in range(len(sorted_population))]

    # Determine the step size for selecting parents
    step_size = total_fitness / num_parents
    start_point = uniform(0, step_size)

    # Perform stochastic universal sampling
    parents = []
    current_position = start_point
    index = 0

    while len(parents) < num_parents:
        while current_position > cumulative_probabilities[index]:
            index = (index + 1) % len(sorted_population)
        parents.append(sorted_population[index])
        current_position += step_size

    return parents
