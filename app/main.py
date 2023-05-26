from fastapi import FastAPI

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def check():
    return "Welcome to NQueens Puzzle Optimizations!"
