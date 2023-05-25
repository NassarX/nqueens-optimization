# N-Queens Puzzle - Optimization Techniques
>Course project of **`COMPUTATIONAL INTELLIGENCE FOR OPTIMIZATION`**  course - [MDSAA-DS](www.novaims.unl.pt/MDSAA-DS) - Spring 2023

## Overview
The `N Queens` puzzle is a classic puzzle in chess, going back to 1848. The goal is to try to place the queens on a chessboard so that none of them are attacking any of the other.
More information about the puzzle can be found on [Wikipedia](https://en.wikipedia.org/wiki/Eight_queens_puzzle). 
Or you can watch [this video](https://youtu.be/jPcBU0Z2Hj8) to get a better understanding of the problem.

In this project, we will explore different optimization techniques including backtracking, local search, and genetic algorithms to solve the n-queens puzzle.
While the examples in documentation focuses on the 8-queens version, you can apply these techniques to solve the puzzle for different board sizes.

## Table of Contents
- [Problem Statement](#problem-statement)
  - [Computational Complexity](#computational-complexity)
    - [Brute-Force](#brute-force)
    - [Possible Optimization](#possible-optimization)
- [Optimization Techniques](#optimization-techniques)
  - [Backtracking Technique (Baseline)](#backtracking-technique-baseline)
  - [Heuristic Methods](#heuristic-methods)
    - [Hill Climbing Algorithm](#hill-climbing-algorithm)
    - [Simulated Annealing Algorithm](#simulated-annealing-algorithm)
  - [Metaheuristic Methods](#metaheuristic-methods)
    - [Genetic Algorithms](#genetic-algorithms)
      - [Fitness Module](#fitness-module)
      - [Selection Module](#selection-module)
      - [Crossover Module](#crossover-module)
      - [Mutation Module](#mutation-module)
      - [Algorithm](#algorithm)
- [Setup Environment](#setup-environment)
  - [Docker](#docker)
  - [Local Environment](#local-environment)


## Problem Statement

The `eight queens` puzzle is a classic puzzle in chess, going back to 1848. The goal is to try to place eight queens on a chessboard so that none of them are attacking any of the other.

*Ps. The queen can move as far as she likes vertically, horizontally or diagonally. which mean we can't place two queens in the same row, column, or diagonal.* S*o on a normal chessboard (8 x 8) we can't put nine or more queens. Eight is the maximum.*

*A single queen threatening the squares on the board (marked in red)*
![A *single queen threatening*](assets/queen_threatens.svg)


Our task here is to find all such configurations of queens on the *(8 x 8)* board. There are 92 possible configurations.

### Computational Complexity

Let's first understand and represented the problem mathematically to get a better understanding of problem computational complexity.

There are 92 solutions to the *8 x 8* problem. Many of these are reflections and rotations of some of the others, and if we de-duplicate against this, purists state that there are only 12 distinct solutions (92 does not divide equally by 12 because many of the reflections and rotations of a pure solutions are not unique).

All fundamental solutions are presented below:
![All fundamental solutions (12 distinct solutions)](assets/solutions.png)

#### **Brute-Force**

[Brute-force computational techniques](https://en.wikipedia.org/wiki/Brute-force_search) could be the first possible mechanism we think of where blindly trying the eight queens in every possible location. This is a really dumb idea and computationally so expensive, but would calculate all possible combinations Using [Combinations Calculator nCr](https://www.calculatorsoup.com/calculators/discretemathematics/combinations.php) :

$$ C(n, r) = ({n \over r}) = {n! \over (r!(n-r)!)} $$

$$ C(64, 8) = {64! \over (8!(64 - 8)!)} = 4,426,165,368 $$

Imagine having to test 4,426,165,368 combinations. If we can process 50,000 combinations per second that's going to take our computer over 24 hours to complete the task. ouch!

#### Possible Optimization

- By applying a simple rule that to put each queen on a separate row, and this massively reduces the number of possibilities.

$$ P(n,n) = n^n $$

$$ P(8,8) = 8^8 = 16,777,216 $$

- Similarly, there can be only one queen per column, and this reduces the possibilities even further. The problem can be trimmed down to an analogous problem of generating [permutations](https://en.wikipedia.org/wiki/Permutation) of the 8 queens, which can then be checked for diagonal attacks.

$$ n! = 8! = 40,320 $$

This is a much more manageable number. However, checking each permutation is still computationally expensive. We can do better by using a heuristic approach.

## Optimization Techniques

### Backtracking Technique (Baseline) 

Backtracking is a systematic algorithmic technique for finding solutions to problems that involve finding
an arrangement of elements satisfying certain constraints. It explores the search space by incrementally
building candidates and backtracking when a dead-end or invalid solution is encountered.

Unlike heuristic methods, backtracking does not use heuristics or approximate techniques to guide the search process. Instead, it exhaustively explores the entire search space by considering all possible combinations, making it more computationally expensive for large problem instances.

**You can find the implementation of the backtracking algorithm here [backtracking.py](https://github.com/NassarX/NQueens-Optimization/blob/main/app/nqueens/backtracking.py)**

Usage:
```shell
python backtracking.py --n-queen 8
```

Output:

```
N-Queens Backtracking Algorithm
==========================
Dimension: 8
Number of solutions: 92
Execution time: 0:00:00.002758

╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗
║   ║   ║   ║   ║ ♛ ║   ║   ║   ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║   ║   ║   ║   ║   ║   ║ ♛ ║   ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║   ║ ♛ ║   ║   ║   ║   ║   ║   ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║   ║   ║   ║   ║   ║ ♛ ║   ║   ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║   ║   ║ ♛ ║   ║   ║   ║   ║   ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║ ♛ ║   ║   ║   ║   ║   ║   ║   ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║   ║   ║   ║   ║   ║   ║   ║ ♛ ║
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣
║   ║   ║   ║ ♛ ║   ║   ║   ║   ║
╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝
```

Here, we are using backtracking as a baseline algorithm for solving the N-Queens problem before applying
other techniques like hill climbing and genetic algorithms. By starting with backtracking as a baseline, we can compare and evaluate the effectiveness and efficiency
of other techniques like hill climbing and genetic algorithms for solving the N-Queens problem.

### Heuristic Methods
Heuristic algorithms use practical and approximate techniques to guide the search for optimal solutions. They do not guarantee finding the global optimum but aim to find good-quality solutions efficiently.

#### Hill Climbing Algorithm


#### Simulated Annealing Algorithm

### Metaheuristic Methods
Metaheuristic algorithms are high-level strategies that guide the search process by combining and adapting different heuristics. They are designed to handle complex optimization problems with large search spaces and provide robust and efficient solutions.

#### Genetic Algorithms
Genetic algorithms are a powerful technique for optimization problems that mimic natural selection. 

In this project, we're going to use genetic algorithms to solve the classic 8 Queen Puzzle. The goal is to find a placement of 8 queens on a chessboard such that no two queens are attacking each other. We start with an initial state where some queens may be attacking each other, and use the genetic algorithm to evolve towards the optimal solution. The project includes a Python implementation of the genetic algorithm, as well as visualization tools to help understand the evolution process. Our results show that the genetic algorithm can efficiently solve the 8 Queen Puzzle and find solutions that are optimal or close to optimal.

##### Fitness Module

##### Selection Module

##### Crossover Module

##### Mutation Module

##### Algorithm

### Setup Environment

Feel free to use any of the following methods to run the application locally.

#### Docker

This application is shipped with the Docker Compose environment and requires Docker to be installed locally and running.
If you're not familiar with Docker or don't have it locally, please reach out to 
[the official website](https://www.docker.com) to get the latest version and installation instructions.

Once you have Docker up and running please perform the following command to start the application:

```shell
docker-compose up
```
Or
```shell
make up
```

The container will be listening on port `80` on your `localhost`, you can access the application main page using the 
following URL: [http://localhost](http://localhost:80).

As soon as you are done with the test assignment you can stop the application:

```shell
docker-compose down --rmi all
```
Or
```shell
make down
```
This will stop the application and remove containers & network.

#### Local environment

If you don't want to use Docker, you can run the application locally. Please make sure you have the following
requirements installed:
- python >= 3.8
- pip >= 20.2.4

Once you have the requirements installed, please perform the following commands to start the application:

```shell
cd app
pip install -r requirements.txt
```