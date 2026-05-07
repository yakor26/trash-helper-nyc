from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return "Placeholder for root"