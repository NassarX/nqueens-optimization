from random import choice, sample, random
from operator import attrgetter
from copy import deepcopy


class Population:
    """Class representing a population of individuals.
    Population object is a collection of individuals. It is initialized by generating a list of individuals.

    :param size (int): The number of individuals in the population.
    :param optim (str): The type of optimization (min or max).
    :param kwargs: Individual parameters (see Individual class).
    """

    def __init__(self, size: int, optim: str, **kwargs) -> None:
        # Initialize the individuals in the population
        self.individuals = [
            Individual(
                size=kwargs["sol_size"],
                distinct=bool(kwargs["distinct"]),
                valid_set=kwargs["valid_set"],
            )
            # Create a list of Individual objects
            for _ in range(size)
        ]
        self.size = size
        self.optim = optim

    def evolve(self, gens: int, xo_prob: float, mut_prob: float, select, mutate, crossover, elitism: bool):
        """ Evolve the population over a given number of generations.

            :param gens: The number of generations. (e.g., 100)
            :param xo_prob: The probability of crossover. (e.g., 0.8)
                Crossover probability determines the likelihood of crossover occurring during reproduction.
                It represents the probability that a crossover operation will be applied to two selected parent individuals.
            :param mut_prob: The probability of mutation for each individual. (e.g., 0.1)
                Each element in the representation has a mutation probability chance of being mutated.
                Mutation probability determines the likelihood of mutation occurring.
                Higher mutation probability increases the chance of exploration by introducing more random changes to the population,
                while lower mutation probability encourages exploitation by maintaining more of the existing solutions.
            :param select: The selection function. It defines how individuals are selected for reproduction.
                The selection function should take a population as input and return a selected individual.
            :param mutate: The mutation function. It defines how individuals are mutated.
                The mutation function should take an individual and the mutation probability as input and modify the individual.
            :param crossover: The crossover function. It defines how individuals are crossed over to create offspring.
                The crossover function should take two parent individuals as input and return two offspring individuals.
            :param elitism: A boolean indicating whether to use elitism.
                If elitism is True, the best individual from the current generation is automatically carried over to the next generation,
                regardless of whether it is better than the offspring generated through reproduction.
            :return: None
        """

        assert (callable(select)), "select function must be callable"
        assert (callable(mutate)), "mutate function must be callable"
        assert (callable(crossover)), "crossover function must be callable"

        for _ in range(gens):
            new_population = []

            # Perform elitism by copying the best individual from the current population
            elite = deepcopy(self.best_indv)

            while len(new_population) < self.size:
                # Select parents from the current population
                parent1, parent2 = select(self), select(self)
                while parent2 == parent1:  # Ensure distinct parents
                    parent2 = select(self)

                # Set the generation of the parents
                parent1.generation = _ + 1
                parent2.generation = _ + 1

                # Perform crossover with a certain probability
                offspring1, offspring2 = (crossover(parent1, parent2) if random() < xo_prob else (parent1, parent2))

                # Perform mutation with a certain probability
                offspring1 = mutate(offspring1) if random() < mut_prob else offspring1
                offspring2 = mutate(offspring2) if random() < mut_prob else offspring2

                # Add offspring to the new population
                new_population.append(offspring1)
                if len(new_population) < self.size:
                    new_population.append(offspring2)

            if elitism:
                # Replace the worst individual in the new population with the elite individual
                worst = min(new_population, key=attrgetter("fitness")) if self.optim == "max" else max(
                    new_population, key=attrgetter("fitness"))

                if (self.optim == "max" and elite.fitness > worst.fitness) or (
                        self.optim == "min" and elite.fitness < worst.fitness):
                    new_population.remove(worst)
                    new_population.append(elite)

            # Replace the current population with the new population
            self.individuals = new_population

        # Print the best individual in the current population
        # print(
        #    f"Best Individual in gen: {self.best_indv}, Representation: {self.best_indv.representation}")

    @property
    def best_indv(self):
        """Return the best individual in the population."""

        if self.optim == "max":
            return max(self.individuals, key=attrgetter("fitness"))
        else:
            return min(self.individuals, key=attrgetter("fitness"))

    @property
    def worst_indv(self):
        """Return the worst individual in the population."""

        if self.optim == "max":
            return min(self.individuals, key=attrgetter("fitness"))
        else:
            return max(self.individuals, key=attrgetter("fitness"))

    @property
    def mean_fitness(self):
        """Return the mean fitness of the population."""

        return sum([i.fitness for i in self.individuals]) / self.size

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]


class Individual:
    """Class representing possible solution.

    Individual object is one of the solutions to the problem
    (ex. possible arrangement of the puzzle's pieces).

    :param representation (list or None): The representation of an individual's chromosome.
                If None, a random representation will be generated.
    :param size (int or None): The size or length of the individual's representation.
    :param distinct (bool): A boolean indicating whether elements can be chosen with distinct.
    :param valid_set (iterable or None): A collection of valid values used to compose the representation.
    """

    def __init__(
            self,
            representation=None,
            size=None,
            distinct=True,
            valid_set=None,
            generation=0,
    ):
        if representation is None:
            if distinct is False:
                self.representation = [choice(valid_set) for i in range(size)]
            else:
                # Selected elements are guaranteed to be distinct.
                self.representation = sample(valid_set, size)
        else:
            self.representation = representation

        self.fitness = self.get_fitness()
        self.generation = generation

    def get_fitness(self):
        """Return the fitness of the Individual."""
        raise NotImplementedError("Fitness function not implemented.")

    def get_neighbours(self, func, **kwargs):
        """Return a list of neighbours of the Individual."""
        raise NotImplementedError("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        """Return first index of value."""
        return self.representation.index(value)

    def __len__(self):
        """Return the length of the Individual's representation."""
        return len(self.representation)

    def __getitem__(self, position):
        """Return the value at the given position in the Individual's representation."""
        return self.representation[position]

    def __setitem__(self, position, value):
        """Set the value at the given position in the Individual's representation."""
        self.representation[position] = value

    def __repr__(self):
        """Return a string representation of the Individual."""
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}; Generation: {self.generation}"
