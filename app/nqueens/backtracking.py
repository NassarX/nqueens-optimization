# Backtracking Algorithm for N-Queens Problem

"""
Backtracking is a systematic algorithmic technique for finding solutions to problems that involve finding
an arrangement of elements satisfying certain constraints. It explores the search space by incrementally
building candidates and backtracking when a dead-end or invalid solution is encountered.

Here, we are using backtracking as a baseline algorithm for solving the N-Queens problem before applying
other techniques like hill climbing and genetic algorithms. The goal is to place N queens on an NxN chessboard
in such a way that no two queens are attacking each other. The constraints are that no two queens should be
in the same row, column, or diagonal.

The backtracking algorithm for the N-Queens problem follows these steps:
1. Start with an empty board.
2. Try placing a queen in the first column of the first row.
3. If a queen can be placed without conflicts, move to the next column and repeat step 2.
4. If all queens are placed successfully, a valid solution is found.
5. If a conflict is encountered, backtrack to the previous column and try a different position for the
   queen in that column.
6. Repeat steps 3-5 until all valid solutions are found or all possibilities have been explored.

The algorithm ensures that only valid and non-attacking queen placements are considered, leading to a
solution where no two queens attack each other.

By starting with backtracking as a baseline, we can compare and evaluate the effectiveness and efficiency
of other techniques like hill climbing and genetic algorithms for solving the N-Queens problem.

Let's proceed with the implementation.
"""
import sys
import os

sys.path.append(os.path.abspath("."))
import argparse
from datetime import datetime
from app.nqueens.utils import N_QUEEN_CONST, _create_chessboard


def get_candidates(state, size):
    """
    Get the next set of candidates to construct the next state. A candidate is a column index to place a queen.

    :param state: list - a list of column indices where queens are placed
    :param size: int - the size of the board
    :return: set
    """
    # if the state is empty, return all columns as candidates
    if not state:
        return range(size)

    # find the next position in the state to populate
    position = len(state)
    candidates = set(range(size))

    # prune down candidates that place the queen into attacks
    for row, col in enumerate(state):
        # discard the column index if it's occupied by a queen
        candidates.discard(col)
        dist = position - row

        # discard diagonals
        candidates.discard(col + dist)
        candidates.discard(col - dist)
    return candidates


def is_valid_state(state, size) -> bool:
    """
    Check if the state is a valid solution. A valid solution is a state where all queens are placed on the board.
    :param state: list - a list of column indices where queens are placed
    :param size: int - the size of the board
    :return: boolean
    """
    # check if it is a valid solution
    return len(state) == size


class NQueensBacktracking:

    def solveNQueens(self, size: int) -> list[list[str]]:
        """
        Entry point for the backtracking algorithm, which returns a list of valid solutions.

        :param size: int - the size of the board
        :return: list[list[str]]
        """
        solutions = []
        state = []
        self.search(state, solutions, size)
        return solutions

    def search(self, state, solutions, size):
        """
        Recursively search for valid solutions.
        :param state: list - a list of column indices where queens are placed
        :param solutions: list[list[str]]
        :param size: int - the size of the board
        :return: None
        """

        # base case
        if is_valid_state(state, size):
            solutions.append(state[:])
            return

        # get candidates
        for candidate in get_candidates(state, size):
            # recurse
            state.append(candidate)
            self.search(state, solutions, size)
            state.pop()


def main():
    """
    Entry point for the backtracking algorithm, which returns a list of valid solutions.

    USAGE: python backtracking.py -n 8
    """
    parser = argparse.ArgumentParser(description='NQueens Backtracking')
    parser.add_argument('-n', '--n-queen', type=int, default=N_QUEEN_CONST,
                        help='Number of queens')
    args = parser.parse_args()

    results = []
    start_time = datetime.now()
    try:
        start_time = datetime.now()
        backtracking = NQueensBacktracking()
        results = backtracking.solveNQueens(args.n_queen)
    except KeyboardInterrupt:
        print("\nInterrupted", end="\n")
    finally:
        end_time = datetime.now()
        representation = ""
        representation += "N-Queens Backtracking Algorithm\n"
        representation += "==========================\n"
        representation += "Dimension: {}\n".format(args.n_queen)
        representation += "Number of solutions: {}\n".format(len(results))
        representation += "Execution time: {} ms\n".format(int((end_time - start_time).total_seconds() * 1000))
        representation += "\n"
        representation += _create_chessboard(args.n_queen, results[0])

        print(representation)


if __name__ == '__main__':
    main()
