import sys
import os

sys.path.append(os.path.abspath("."))
from app.charles import Individual, Population
import argparse
from datetime import datetime
from app.nqueens.utils import calculate_fitness_score, _create_chessboard, OPERATORS_MAPPING
from app.nqueens.utils import N_QUEEN_CONST, MUTATION_PROBABILITY_CONST, CROSSOVER_PROBABILITY_CONST, \
    INITIAL_POPULATION_CONST, \
    GENERATIONS_CONST, SELECT_CONST, MUTATE_CONST, CROSSOVER_CONST


class NQueensGeneticAlgorithm:
    """A class to represent the N-Queens Genetic Algorithm.

    Attributes:
        population (Population): A population of individuals.
        dimension (int): The dimension of the board.

    It is initialized with a population of individuals. Each individual represents a configuration of queens on board.
    """
    population: Population = None
    dimension: int = N_QUEEN_CONST
    best_fitness: int = 0
    num_gens: int = 0

    def __init__(self, population_size: int, dimension: int) -> None:
        # Initial population
        self.duration = 0
        self.crossover_func = None
        self.mutate_func = None
        self.selection_func = None

        # Override Individual class get_fitness using Monkey Patching (Duck Typing) technique.
        Individual.get_fitness = calculate_fitness_score
        self.population = Population(size=population_size,
                                     optim="max",
                                     sol_size=dimension,
                                     valid_set=range(dimension),
                                     distinct=True)

        # Calculate the best fitness score (the maximum number of non-attacking queen pairs)
        self.best_fitness = dimension * (dimension - 1) // 2
        self.population_size = population_size

    def run(self,
            generations: int,
            crossover_probability: float,
            mutation_probability: float,
            mutation_operator: str,
            selection_operator: str,
            crossover_operator: str):
        self.num_gens = generations
        self.selection_func = OPERATORS_MAPPING[selection_operator]
        self.mutate_func = OPERATORS_MAPPING[mutation_operator]
        self.crossover_func = OPERATORS_MAPPING[crossover_operator]

        # Evolve the population for the given number of generations
        start_time = datetime.now()
        self.population.evolve(
            gens=generations,
            xo_prob=crossover_probability,
            mut_prob=mutation_probability,
            select=self.selection_func,
            mutate=self.mutate_func,
            crossover=self.crossover_func,
            elitism=True
        )
        end_time = datetime.now()
        duration = end_time - start_time
        milliseconds = int(duration.total_seconds() * 1000)
        self.duration = milliseconds

    def report(self):
        """ Returns a report of the best individual in the population. """

        generations = self.num_gens
        best_fitness = self.population.best_indv.fitness
        best_fitness_percentage = (best_fitness * 100) / self.best_fitness
        best_representation = self.population.best_indv.representation
        worst_fitness = self.population.worst_indv.fitness
        worst_representation = self.population.worst_indv.representation
        mean_fitness = self.population.mean_fitness
        selection_func = self.selection_func.__name__
        mutate_func = self.mutate_func.__name__
        crossover_func = self.crossover_func.__name__
        duration = self.duration

        return {
            "generations": generations,
            "duration": duration,
            "best_fitness": best_fitness,
            "best_fitness_percentage": best_fitness_percentage,
            "best_representation": best_representation,
            "worst_fitness": worst_fitness,
            "worst_representation": worst_representation,
            "mean_fitness": mean_fitness,
            "selection_operator": selection_func,
            "mutate_operator": mutate_func,
            "crossover_operator": crossover_func
        }

    def print_report(self):
        """ Prints a report of the best individual in the population. """
        representation = ""
        representation += "N-Queens Genetic Algorithm\n"
        representation += "==========================\n"
        representation += "Dimension: {}\n".format(self.dimension)
        representation += "Population size: {}\n".format(self.population_size)
        representation += "Generations: {}\n".format(self.report()["generations"])
        representation += "Duration: {} ms\n".format(self.duration)
        representation += "==========================\n"
        representation += "Best fitness: {}\n".format(self.report()["best_fitness"])
        representation += "Best fitness percentage: {}\n".format(self.report()["best_fitness_percentage"])
        representation += "Best representation: {}\n".format(self.report()["best_representation"])
        representation += "Worst fitness: {}\n".format(self.report()["worst_fitness"])
        representation += "Worst representation: {}\n".format(self.report()["worst_representation"])
        representation += "Mean fitness: {}\n".format(self.report()["mean_fitness"])
        representation += "==========================\n"
        representation += "Selection operator: {}\n".format(self.report()["selection_operator"])
        representation += "Mutate operator: {}\n".format(self.report()["mutate_operator"])
        representation += "Crossover operator: {}\n".format(self.report()["crossover_operator"])
        representation += _create_chessboard(self.dimension, self.report()["best_representation"])
        representation += "\n"

        return representation


def main():
    parser = argparse.ArgumentParser(description='Genetic Algorithm')
    parser.add_argument('-n', '--n-queen', type=int, default=N_QUEEN_CONST,
                        help='Number of queens')
    parser.add_argument('-p', '--population', type=int, default=INITIAL_POPULATION_CONST,
                        help='Population size')
    parser.add_argument('-c', '--crossover-probability', type=float, default=CROSSOVER_PROBABILITY_CONST,
                        help='Crossover probability')
    parser.add_argument('-m', '--mutation-probability', type=float, default=MUTATION_PROBABILITY_CONST,
                        help='Mutation probability')
    parser.add_argument('-g', '--generations', type=int, default=GENERATIONS_CONST,
                        help='Number of generations')
    parser.add_argument('-s', '--selection', type=str, default=SELECT_CONST,
                        help='Selection Algorithm')
    parser.add_argument('-xo', '--crossover', type=str, default=CROSSOVER_CONST,
                        help='Crossover Algorithm')
    parser.add_argument('-mut', '--mutation', type=str, default=MUTATE_CONST,
                        help='Mutation Algorithm')
    args = parser.parse_args()

    nQueensGA = None
    try:
        nQueensGA = NQueensGeneticAlgorithm(population_size=args.population, dimension=args.n_queen)
        nQueensGA.run(
            generations=args.generations,
            crossover_probability=args.crossover_probability,
            mutation_probability=args.mutation_probability,
            selection_operator=args.selection,
            mutation_operator=args.mutation,
            crossover_operator=args.crossover
        )
    except KeyboardInterrupt:
        print("\nInterrupted", end="\n")
    finally:
        print(nQueensGA.print_report())


if __name__ == '__main__':
    main()
