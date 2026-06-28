from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.analyze import expression_analyzer
from typing import Any
from sympy import sympify, pi
from app.database import Base, engine, SessionLocal
from app.models import Expression
from sqlalchemy.orm import Session
from app import config
from app import models #automatically loads the class

app = FastAPI()
Base.metadata.create_all(bind=engine)

def ini_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Analyzer(BaseModel):
    expression: Any
    bundle: list[Any] | None = None

def find_symbol(symbol):
    if symbol == {config.X}:
        return config.X
    elif symbol == {config.THETA}:
        return config.THETA
    else:
        return config.T
    
def expression_parser(expr):
    if ',' in expr:    #parametric
        expressions = expr.split(',')
        expr1 = expressions[0].strip() 
        expr2 = expressions[1].strip()
        
        s_expr1 = sympify(expr1)
        s_expr2 = sympify(expr2)

        return (s_expr1, s_expr2)

    else:
        user_expr = sympify(expr, locals={'pi':pi})
        return user_expr



@app.get('/')
def home():
    return {'success': 'is running'}

# API
@app.post('/analyze')
def analyzer_expr(request: Analyzer, db: Session = Depends(ini_db)):   #type of 'Analyzer' basemodel
    user_expr = expression_parser(request.expression)
    print(user_expr)
    if type(user_expr) == list:
        symbol = config.T
    else:
        symbol = find_symbol(user_expr.free_symbols)
    
    info = expression_analyzer(symbol, user_expr, request.expression, request.bundle)
    
    derivative = info.get('info', None) #incase if parametric
    if derivative is None:
        derivative = f"Left: {info.get('Left Derivative')}, Right: {info.get('Right Derivative')}"


    row = Expression(
        expression=str(info.get('Input')),
        expression_type=str(info.get('Type')),
        derivatives=derivative,
        roots=str(info.get('Roots', info.get('Roots (approximated)', ''))),
        domain=str(info.get('Domain')),
        range=str(info.get('Range', info.get('Range (approximated)', '')))
    )

    db.add(row)
    db.commit()
    db.refresh(row)


    return info #front-end needs data
