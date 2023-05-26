import sys
import os
sys.path.append(os.path.abspath(".."))
from app.charles import Individual, Population, tournament_selection, single_point_co, random_position_mutation, pmx, \
    swap_mutation
import argparse
from datetime import datetime
from utils import calculate_fitness_score, _create_chessboard
from utils import N_QUEEN_CONST, MUTATION_PROBABILITY_CONST, CROSSOVER_PROBABILITY_CONST, INITIAL_POPULATION_CONST, \
    GENERATIONS_CONST

# Add the fitness function to the Individual class as a method using Monkey Patching (Duck Typing) technique.
Individual.get_fitness = calculate_fitness_score


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
        self.population = Population(size=population_size,
                                     optim="max",
                                     sol_size=dimension,
                                     valid_set=range(dimension),
                                     distinct=True)

        # Calculate the best fitness score (the maximum number of non-attacking queen pairs)
        self.best_fitness = dimension * (dimension - 1) // 2

    def run(self, generations: int, xo_prob: float, mutation_prob: float):
        self.num_gens = generations

        # Evolve the population for the given number of generations
        self.population.evolve(
            gens=generations,
            xo_prob=xo_prob,
            mut_prob=mutation_prob,
            select=tournament_selection,
            mutate=swap_mutation,
            crossover=pmx,
            elitism=True
        )

    def report(self):
        """ Returns a report of the best individual in the population. """

        generations = self.num_gens
        best_fitness = self.population.best_indv.fitness
        best_fitness_percentage = (best_fitness * 100) / self.best_fitness
        best_representation = self.population.best_indv.representation
        worst_fitness = self.population.worst_indv.fitness
        worst_representation = self.population.worst_indv.representation
        mean_fitness = self.population.mean_fitness

        return {
            "generations": generations,
            "best_fitness": best_fitness,
            "best_fitness_percentage": best_fitness_percentage,
            "best_representation": best_representation,
            "worst_fitness": worst_fitness,
            "worst_representation": worst_representation,
            "mean_fitness": mean_fitness
        }


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
    args = parser.parse_args()

    nQueensGA = None
    start_time = datetime.now()
    try:
        start_time = datetime.now()
        nQueensGA = NQueensGeneticAlgorithm(population_size=args.population, dimension=args.n_queen)
        nQueensGA.run(
            generations=args.generations,
            xo_prob=args.crossover_probability,
            mutation_prob=args.mutation_probability
        )
    except KeyboardInterrupt:
        print("\nInterrupted", end="\n")
    finally:
        end_time = datetime.now()
        representation = ""
        representation += "N-Queens Genetic Algorithm\n"
        representation += "==========================\n"
        representation += "Dimension: {}\n".format(nQueensGA.dimension)
        representation += "Population size: {}\n".format(args.population)
        representation += "Generations: {}\n".format(nQueensGA.report()["generations"])
        representation += "Duration: {}\n".format(end_time - start_time)
        representation += "Best fitness: {}\n".format(nQueensGA.report()["best_fitness"])
        representation += "Best fitness percentage: {}\n".format(nQueensGA.report()["best_fitness_percentage"])
        representation += "Best representation: {}\n".format(nQueensGA.report()["best_representation"])
        representation += "Worst fitness: {}\n".format(nQueensGA.report()["worst_fitness"])
        representation += "Worst representation: {}\n".format(nQueensGA.report()["worst_representation"])
        representation += "Mean fitness: {}\n".format(nQueensGA.report()["mean_fitness"])
        representation += "\n"
        representation += _create_chessboard(args.n_queen, nQueensGA.report()["best_representation"])

        print(representation)


if __name__ == '__main__':
    main()
