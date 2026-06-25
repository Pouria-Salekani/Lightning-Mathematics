from fastapi import FastAPI
from pydantic import BaseModel
from app.analyze import expression_analyzer
from typing import Any
from sympy import sympify
from app import config

app = FastAPI()

#we can do sympify stuff here


#IN THE WEBPAGE, when YOU enter the expression, it does stuff based off of that
#hence, probably only need: expression, and bundles or expr, symbol, bundle

#TODO: MAKE METHODS HERE TO SYMPIFY STUFF. CODE ALREADY IN MODES.PY



class Analyzer(BaseModel):
    expression: str
    #bundle: list[Any] | None = None

@app.get("/")
def home():
    return {'success': 'is running'}

@app.post('/analyze')
def analyzer_expr(request: Analyzer):   #type of 'Analyzer' basemodel
    user_expr = sympify(request.expression)
    return expression_analyzer(config.THETA, user_expr, request.expression, None)
