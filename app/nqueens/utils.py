import sys
import os
sys.path.append(os.path.abspath(".."))
from colorama import Fore, Back, Style
from app.charles import Individual, tournament_selection, swap_mutation, pmx


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

    for row in range(num_queens):
        for col in range(row + 1, num_queens):
            # Check if queens on the same column are attacking each other
            if board[row] == board[col]:
                num_collisions += 1
            # Check if queens on diagonals are attacking each other
            elif abs(board[row] - board[col]) == abs(row - col):
                num_collisions += 1

    # Calculate the maximum possible number of non-attacking queen pairs
    max_pairs = num_queens * (num_queens - 1) // 2

    # Calculate the fitness score by subtracting the number of collisions from the maximum possible pairs
    fitness_score = max_pairs - num_collisions

    return fitness_score


def get_neighbours(self):
    """Return a list of neighbours for the N-Queens problem."""
    neighbours = []

    dimension = len(self.representation)
    for row in range(dimension):
        for col in range(dimension):
            if col != self.representation[row]:
                neighbour_representation = self.representation[:]
                neighbour_representation[row] = col
                neighbour = Individual(representation=neighbour_representation)
                neighbours.append(neighbour)

    return neighbours


def state_to_string(state, n):
    # ex. [1, 3, 0, 2]
    # output: [".Q..","...Q","Q...","..Q."]
    ret = []
    print("state: {}".format(state))

    for i in state:
        string = '.' * i + 'Q' + '.' * (n - i - 1)
        ret.append(string)
    return ret


MUTATION_PROBABILITY_CONST = 0.1
CROSSOVER_PROBABILITY_CONST = 0.1
INITIAL_POPULATION_CONST = 100
GENERATIONS_CONST = 100
N_QUEEN_CONST = 8

# CHANGE
SELECT_CONST = tournament_selection
MUTATE_CONST = swap_mutation
CROSSOVER_CONST = pmx

CELL = '   '
QUEEN = '♛'


class CONST:
    WHITE_CELL = f'{Back.WHITE}{CELL}{Style.RESET_ALL}'
    BLACK_CELL = f'{Back.BLACK}{CELL}{Style.RESET_ALL}'
    WHITE_QUEEN = f'{Back.WHITE} {Fore.RED}{QUEEN} {Style.RESET_ALL}'
    BLACK_QUEEN = f'{Back.BLACK} {Fore.LIGHTRED_EX}{QUEEN} {Style.RESET_ALL}'


def _create_chessboard(n_queen, board) -> str:
    """
    Create a chessboard with the queens in their positions and return it as a string.

    :param n_queen:
    :param board:
    :return:
    """

    PUT_QUEEN = 1
    NOT_PUT_QUEEN = 0
    line = '╠═══' + '╬═══' * (n_queen - 1) + '╣'
    first_line = ('╔' + line[1:-1] + '╗').replace('╬', '╦')
    last_line = ('╚' + line[1:-1] + '╝').replace('╬', '╩')
    board = [[PUT_QUEEN if queen_pos == _ else NOT_PUT_QUEEN for _ in range(n_queen)]
             for queen_pos in board]
    chessboard = ''
    chessboard += f'{first_line}\n'

    cell_color = lambda i, j: f'{CONST.BLACK_CELL}' if (i + j) % 2 else f'{CONST.WHITE_CELL}'
    queen_color = lambda i, j: f'{CONST.BLACK_QUEEN}' if (i + j) % 2 else f'{CONST.WHITE_QUEEN}'

    for i, row in enumerate(board):
        chessboard += '║' + '║'.join('{}'.format(
            queen_color(i, j) if col == PUT_QUEEN else cell_color(i, j)
        ) for j, col in enumerate(row)
                                     ) + '║\n'
        chessboard += f'{line}\n' if i != n_queen - 1 else f'{last_line}'

    return chessboard
