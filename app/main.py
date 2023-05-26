from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def check():
    return "Welcome to NQueens Puzzle Optimizations!"
