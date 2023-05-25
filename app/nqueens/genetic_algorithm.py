import argparse
from datetime import datetime
from app.charles.charles import Individual, Population
from app.charles.selection import tournament_selection
from app.charles.crossover import single_point_co
from app.charles.mutation import random_position_mutation
from utils import N_QUEEN_CONST, MUTATION_PROBABILITY_CONST, CROSSOVER_PROBABILITY_CONST, INITIAL_POPULATION_CONST, \
    GENERATIONS_CONST, _create_chessboard


def calculate_fitness_score(self):
    """Calculate the fitness score of the individual.

    The fitness score represents the number of non-attacking queen pairs on the board.
    A higher fitness score indicates a better configuration with fewer queen collisions.

    In this fitness function, we iterate through each pair of queens on the board and check if they are attacking
    each other. We count the number of collisions and subtract it from the maximum possible pairs to calculate the
    fitness score. A higher fitness score indicates a better configuration with fewer queen collisions.

    Steps:
        1. Iterate through each pair of queens on the board.
        2. Checks for collisions between queens. It compares
            the positions of queens in terms of row and column to determine if they are attacking each other.
            If queens are on the same column (board[i] == board[j])
            or on diagonals (abs(board[i] - board[j]) == abs(i - j)),
            it increments num_collisions by 1.
        3. After counting all the collisions, the function calculates the maximum possible number of
            non-attacking queen pairs using the formula num_queens * (num_queens - 1) // 2.
            This represents the total number of unique pairs of queens that can be formed on the board.
        4. Finally, the function calculates the fitness score by subtracting the number of collisions (num_collisions)
            from the maximum possible pairs (max_pairs).
        The resulting value represents the number of non-attacking queen pairs.

    Example: >>> board = [1, 3, 0, 2] In this example, there are no collisions between any pair of queens. So,
    the fitness score would be the maximum possible number of non-attacking queen pairs, which is (4 * (4 - 1)) / 2 = 6.

    Returns:
        int: Fitness score representing the number of non-attacking queen pairs.
    """
    board = self.representation
    num_queens = len(board)
    num_collisions = 0

    for i in range(num_queens):
        for j in range(i + 1, num_queens):
            # Check if queens on the same column are attacking each other
            if board[i] == board[j]:
                num_collisions += 1
            # Check if queens on diagonals are attacking each other
            elif abs(board[i] - board[j]) == abs(i - j):
                num_collisions += 1

    # Calculate the maximum possible number of non-attacking queen pairs
    max_pairs = num_queens * (num_queens - 1) // 2

    # Calculate the fitness score by subtracting the number of collisions from the maximum possible pairs
    fitness_score = max_pairs - num_collisions

    return fitness_score


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
            mutate=random_position_mutation,
            crossover=single_point_co,
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
