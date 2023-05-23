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


class NQueensBacktracking:

    def solveNQueens(self, n: int) -> list[list[str]]:
        """
        Entry point for the backtracking algorithm, which returns a list of valid solutions.

        :type n: int
        :param n:
        :return:
        """
        solutions = []
        state = []
        self.search(state, solutions, n)
        return solutions

    def is_valid_state(self, state, n):
        """
        Check if the state is a valid solution. A valid solution is a state where all queens are placed on the board.
        :param state: boolean
        :param n:
        :return:
        """
        # check if it is a valid solution
        return len(state) == n

    def get_candidates(self, state, n):
        """
        Get the next set of candidates to construct the next state. A candidate is a column index to place a queen.

        :param state: boolean
        :param n:
        :return:
        """
        # if the state is empty, return all columns as candidates
        if not state:
            return range(n)

        # find the next position in the state to populate
        position = len(state)
        candidates = set(range(n))

        # prune down candidates that place the queen into attacks
        for row, col in enumerate(state):
            # discard the column index if it's occupied by a queen
            candidates.discard(col)
            dist = position - row

            # discard diagonals
            candidates.discard(col + dist)
            candidates.discard(col - dist)
        return candidates

    def search(self, state, solutions, n):
        """
        Recursively search for valid solutions.
        :param state:
        :param solutions:
        :param n:
        :return:
        """

        # base case
        if self.is_valid_state(state, n):
            state_string = self.state_to_string(state, n)
            solutions.append(state_string)
            return

        # get candidates
        for candidate in self.get_candidates(state, n):
            # recurse
            state.append(candidate)
            self.search(state, solutions, n)
            state.pop()

    def state_to_string(self, state, n):
        # ex. [1, 3, 0, 2]
        # output: [".Q..","...Q","Q...","..Q."]
        ret = []
        for i in state:
            string = '.' * i + 'Q' + '.' * (n - i - 1)
            ret.append(string)
        return ret

if __name__ == '__main__':
    n = int(sys.argv[1])
    solution = NQueensBacktracking()
    solutions = solution.solveNQueens(n)
    print(solutions)
    print("Number of solutions: {}".format(len(solutions)))
