from random import choice, uniform
from math import exp


def hill_climb(search_space, max_iter=1000):
    """Hill climbs a given search space.

    Args:
        search_space (Population): A Population of solutions
        max_iter (int): Maximum number of iterations to run the algorithm.

    Returns:
        Individual: Local optimal Individual found in the search.
    """

    # initialize a feasible solution from search space
    start = choice(search_space)

    # current solution is i-start
    position = start
    consecutive_no_improvement = 0  # Counter for consecutive iterations without improvement

    print(f"Initial position: {position.representation}, fitness: {position.fitness}")

    # Repeat until termination condition is met
    while consecutive_no_improvement < max_iter:
        # Generate neighbors
        neighbors = position.get_neighbours()

        # Find the best neighbor with the highest fitness
        best_neighbor = max(neighbors, key=lambda x: x.fitness)

        # If the best neighbor is better than the current position, update the position
        if best_neighbor.fitness > position.fitness:
            print(f"Found better solution: {best_neighbor.representation}, Fitness: {best_neighbor.fitness}")
            position = best_neighbor
            consecutive_no_improvement = 0  # Reset the counter
        else:
            consecutive_no_improvement += 1  # Increment the counter

    print(f"Hill Climbing returned: {position.representation}, Fitness: {position.fitness}")
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
