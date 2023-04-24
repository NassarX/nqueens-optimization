# Genetic Algorithm - Eight Queens Puzzle
>Course project of **`COMPUTATIONAL INTELLIGENCE FOR OPTIMIZATION`**  course - [MDSAA-DS](www.novaims.unl.pt/MDSAA-DS) - Spring 2023

## Abstract
Genetic algorithms are a powerful technique for optimization problems that mimic natural selection. In this project, we use a genetic algorithm to solve the classic 8 Queen Puzzle. The goal is to find a placement of 8 queens on a chessboard such that no two queens are attacking each other. We start with an initial state where some queens may be attacking each other, and use the genetic algorithm to evolve towards the optimal solution. The project includes a Python implementation of the genetic algorithm, as well as visualization tools to help understand the evolution process. Our results show that the genetic algorithm can efficiently solve the 8 Queen Puzzle and find solutions that are optimal or close to optimal.

## Eight Queens Puzzle
>The "eight queens" puzzle is a well-known puzzle, going back to 1848. The problem is to try to place eight queens on a chessboard so that none of them are attacking any of the other - remember that the queen can move as far as she likes vertically, horizontally or diagonally. You can't place two queens in the same row, for example, so on a normal chessboard (8 by 8) you can't put nine or more queens. Eight is the maximum.
> 
> More information about the puzzle can be found on [Wikipedia](https://en.wikipedia.org/wiki/Eight_queens_puzzle).
> 
> Or you can watch [this video](https://youtu.be/jPcBU0Z2Hj8) to get a better understanding of the problem.

## Table of Contents
- [Up And Running](#up-and-running)
  - [Docker](#docker) 
  - [Run application](#run-application)
  - [Remove application](#remove-application)
- [SetUp](#setup)
  - [Project GUI](#project-gui)
  - @TODO
- [Modules](#modules)
  - [Fitness Module](#fitness-module)
  - [Crossover Module](#crossover-module)
  - [Mutation Module](#mutation-module)
  - [Algorithm](#algorithm)
- [Usage](#usage)
  - [Run the Algorithm](#run-the-algorithm)


## Up And Running

### Docker

This application is shipped with the Docker Compose environment and requires Docker to be installed locally and running.
If you're not familiar with Docker or don't have it locally, please reach out to 
[the official website](https://www.docker.com)
 to learn more and follow the Docker installation instructions to install it on your platform:   

[Docker for Mac](https://docs.docker.com/desktop/install/mac-install/)  
[Docker for Linux](https://docs.docker.com/desktop/get-started/)  
[Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)

The Project is containerized within one container currently on `Python-3.11-slim` image. 
You don't need to build anything locally, the related images will be automatically pulled from the remote registry 
as soon as you run the application for the first time.

Dependencies:
* `fastapi` - for building APIs with Python.
* `requests` - for making HTTP requests and handling responses.
* `uvicorn` - for running Python APIs.
* `debugpy` - for debugging of Python code running in a container.

### Run application

Once you have Docker up and running please perform the following command to start the application:

    docker-compose up

Alternatively you can start the application containers in detached mode to suppress containers messages:

    docker-compose up --detach

Please see the `Logs` for more details about log messages:

    docker-compose logs -f

If you run the application for the first time, this will pull images from the remote repository, 
create `ga-8queens-puzzle` container run the `pip install` command.

The container will be listening on port `80` on your `localhost`, you can access the application main page using the 
following URL: [http://localhost](http://localhost:80).

### Remove application

As soon as you are done with the test assignment you can stop the application:

    docker-compose down

This will stop the application and remove containers & network.

## SetUp

### Project GUI
@TODO

## Modules

### Fitness Module
@TODO

### Crossover Module
@TODO

### Mutation Module
@TODO

### Algorithm
@TODO

## Usage

### Run the Algorithm
@TODO
