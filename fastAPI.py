# fastAPI.py

from fastapi import FastAPI  # FastAPI import

app = FastAPI()


@app.get("/")
def printHello():
    return "Hello World!"

@app.get("/search/{keyword}")
def printHello(keyword:str):
    return {'keyword':keyword}
