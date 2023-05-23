from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time
from nqueens.backtracking import NQueensBacktracking

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def check():
    return "Welcome to NQueens Puzzle Optimizations!"

@app.get("/backtracking/{n}")
def nqueens(n: int):
    solution = NQueensBacktracking()
    start_time = time.time()
    solutions = solution.solveNQueens(n)
    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        "solutions": solutions,
        "elapsed_time": elapsed_time,
        "number_of_solutions": len(solutions)
    }


@app.get("/puzzle/genetic/{n}")
def nqueens(request: Request, n: int):
    solution = NQueensBacktracking()
    start_time = time.time()
    solutions = solution.solveNQueens(n)
    end_time = time.time()
    elapsed_time = end_time - start_time

    return templates.TemplateResponse("index.html", {
        "request": request,
        "solutions": solutions,
        "elapsed_time": elapsed_time,
        "n":n,
        "number_of_solutions": len(solutions)
    })
