from fastapi import FastAPI
from pydantic import BaseModel
from app.analyze import test

app = FastAPI()


class Analyzer(BaseModel):
    expression: str
    mode: str

@app.get("/")
def home():
    return {'success': 'is running'}

@app.post('/analyze')
def analyzer_expr(request: Analyzer):   #type of 'Analyzer' basemodel
    return test(request.expression, request.mode)
