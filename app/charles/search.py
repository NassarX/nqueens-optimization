from random import choice, uniform
from math import exp


def hill_climb(search_space):
    """Hill climbs a given search space.

    Args:
        search_space (Population): A Population of solutions

    Returns:
        Individual: Local optima Individual found in the search.
    """
    # initialize a feasible solution from search space
    start = choice(search_space)
    # current solution is i-start
    position = start

    print(f"Initial position: {start}")
    # repeat
    while True:
        # generate solution from neighbours
        n = position.get_neighbours()

        # fitness of the neighbours
        n_fit = [i.fitness for i in n]
        best_n = n[n_fit.index(max(n_fit))]

        # if neighbour is better than current solution
        if best_n.fitness > position.fitness:
            print(f"Found better solution: {best_n.representation}")
            position = best_n # neighbour is the new solution
        elif best_n.fitness == position.fitness:
            position = best_n
        else:
            print(f"Hill Climbing returned: {position.representation}")
            return position


def sim_annealing(search_space, L=20, c=10, alpha=0.95, threshold=0.05):
    """Simulated annealing implementation.

    Args:
        search_space (Population): a Population object to search through.
        L (int, optional): Internal loop parameter. Defaults to 20.
        c (int, optional): Temperature parameter. Defaults to 10.
        alpha (float, optional): Alpha to decrease the temperature. Defaults to 0.95.

    Returns:
        Individual: an Individual object - the best found by SA.
    """
    # 1. initialize solution randomly
    position = choice(search_space)
    elite = position
    # 3. repeat until termination condition
    while c > threshold:
        # 3.1 repeat L times
        for _ in range(L):
            # 3.1.1 choose neighbour randomly
            neighbour = choice(position.get_neighbours())
            # 3.1.2. if better, accept
            if neighbour.fitness >= position.fitness:
                position = neighbour
                print(f"Found better solution: {position}")
                if position.fitness > elite.fitness:
                    elite = position
            # else, accept with probability
            else:
                p = uniform(0, 1)
                pc = exp(-abs(neighbour.fitness - position.fitness) / c)
                if p < pc:
                    position = neighbour
                    print(f"Accepted a worse solution: {position}")

        # 3.2 decrement c
        c = c * alpha
    # 4. return solution
    print(f"Elite is {elite}")
    print(f"Simulated Annealing found {position}")
    return elite
