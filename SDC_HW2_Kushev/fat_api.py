from fastapi import FastAPI
from pydantic import BaseModel

def do_it(x, y):
    return str(round((x/y)*100)) + "%"
    
class User_Input(BaseModel):
    x : float
    y : float

app = FastAPI()

@app.post("/do_it")
def calc(input:User_Input):
    res = do_it(input.x, input.y)
    return res