import sys
import os
sys.path.append(os.path.abspath("."))
import argparse
from datetime import datetime
from app.charles import Individual, Population
from app.charles import hill_climb
from app.nqueens.utils import calculate_fitness_score, get_neighbours, N_QUEEN_CONST, _create_chessboard


class NQueensHillClimbing:
    """A class to represent the N-Queens Hill Climbing Algorithm.

    Attributes:
        dimension (int): The dimension of the board.

    It is initialized with a population of individuals. Each individual represents a configuration of queens on board.
    """

    dimension: int = N_QUEEN_CONST
    best_fitness: int = 0

    def __init__(self, dimension):
        self.best_indv = None
        self.dimension = dimension
        self.best_fitness = self.dimension * (self.dimension - 1) // 2

        # Override Individual class get_fitness, get_neighbours using Monkey Patching (Duck Typing) technique.
        Individual.get_fitness = calculate_fitness_score
        Individual.get_neighbours = get_neighbours

    def search(self):
        # Initialize the population
        population = Population(size=1, optim="max", sol_size=self.dimension,
                                valid_set=range(self.dimension), distinct=True)

        # Run the hill climbing algorithm
        self.best_indv = hill_climb(search_space=population, max_iter=100)

    def run(self):
        start_time = datetime.now()

        try:
            self.search()
        except KeyboardInterrupt:
            print("\nInterrupted", end="\n")

        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds() * 1000)
        best_fitness = self.report()["best_fitness"]
        best_fitness_percentage = self.report()["best_fitness_percentage"]
        best_representation = self.report()["best_representation"]

    def report(self):
        """ Returns a report of the best individual in the population. """
        if self.best_indv is None:
            return

        best_fitness_percentage = (self.best_indv.fitness * 100) / self.best_fitness
        best_representation = self.best_indv.representation

        return {
            "best_fitness": self.best_indv.fitness,
            "best_fitness_percentage": best_fitness_percentage,
            "best_representation": best_representation,
        }


def main():
    parser = argparse.ArgumentParser(description='Hill Climbing Algorithm')
    parser.add_argument('-n', '--n-queen', type=int, default=N_QUEEN_CONST,
                        help='Number of queens')
    args = parser.parse_args()

    nQueensHC = NQueensHillClimbing(dimension=args.n_queen)
    start_time = datetime.now()
    try:
        start_time = datetime.now()
        nQueensHC.search()
    except KeyboardInterrupt:
        print("\nInterrupted", end="\n")
    finally:
        end_time = datetime.now()
        representation = ""
        representation += "N-Queens Hill Climbing Algorithm\n"
        representation += "==========================\n"
        representation += "Dimension: {}\n".format(nQueensHC.dimension)
        representation += "Best Fitness: {}\n".format(nQueensHC.report()["best_fitness"])
        representation += "Best Fitness Percentage: {}\n".format(nQueensHC.report()["best_fitness_percentage"])
        representation += "Best Representation: {}\n".format(nQueensHC.report()["best_representation"])
        representation += "Execution time: {} ms\n".format(int((end_time - start_time).total_seconds() * 1000))
        representation += "\n"
        representation += _create_chessboard(args.n_queen, nQueensHC.report()["best_representation"])

        print(representation)


if __name__ == '__main__':
    main()
