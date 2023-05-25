from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import time
from app.nqueens.backtracking import NQueensBacktracking
from app.nqueens.utils import state_to_string

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def check():
    return "Welcome to NQueens Puzzle Optimizations!"


@app.get("/backtracking/{n}")
def backtracking(request: Request, n: int):
    solution = NQueensBacktracking()
    start_time = time.time()
    solutions = solution.solveNQueens(n)
    end_time = time.time()
    elapsed_time = end_time - start_time

    board = []
    for solution in solutions:
        board.append(state_to_string(solution, n))

    return templates.TemplateResponse("index.html", {
        "request": request,
        "solutions": board,
        "elapsed_time": elapsed_time,
        "n": n,
        "number_of_solutions": len(solutions)
    })


@app.get("/hill_climbing/{n}")
def backtracking(request: Request, n: int):
    return 'Not yet'
