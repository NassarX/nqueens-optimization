from fastapi import FastAPI
import debugpy

app = FastAPI()

#debugpy.listen(("0.0.0.0", 5678))
#print("Waiting for client to attach...")
#debugpy.wait_for_client()

@app.get("/")
def check():
    return {"Ok! All set guys!"}
