from colorama import Fore, Back, Style

MUTATION_PROBABILITY_CONST = 0.1
CROSSOVER_PROBABILITY_CONST = 0.1
INITIAL_POPULATION_CONST = 100
GENERATIONS_CONST = 100
N_QUEEN_CONST = 8
CELL = '   '
QUEEN = '♛'


def state_to_string(state, n):
    # ex. [1, 3, 0, 2]
    # output: [".Q..","...Q","Q...","..Q."]
    ret = []
    print("state: {}".format(state))

    for i in state:
        string = '.' * i + 'Q' + '.' * (n - i - 1)
        ret.append(string)
    return ret


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
