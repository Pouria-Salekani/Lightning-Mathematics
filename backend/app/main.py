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
from app.text_formatter import remove_brackets

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



# API --- create
@app.post('/analyze')
def analyzer_expr(request: Analyzer, db: Session = Depends(ini_db)):   #type of 'Analyzer' basemodel
    user_expr = expression_parser(request.expression)
    print(user_expr, type(user_expr))
    if type(user_expr) == list:
        symbol = config.T
    else:
        symbol = find_symbol(user_expr.free_symbols)
    
    info = expression_analyzer(symbol, user_expr, request.expression, request.bundle)
    
    derivative = info.get('info', None) #incase if parametric
    if derivative is None:
        derivative = f"Left: {info.get('Left Derivative')}, Right: {info.get('Right Derivative')}"


    row = Expression(
        expression=str(remove_brackets(info.get('Input')) 
                       if '[' in info.get('Input') else info.get('Input')),
        expression_type=str(info.get('Type')),
        derivatives=derivative,
        roots=str(info.get('Roots', info.get('Roots (approximated)', ''))),
        domain=str(info.get('Domain')),
        range=str(info.get('Range', info.get('Range (approximated)', '')))
    )

    db.add(row)
    db.commit() #important after each op
    db.refresh(row)


    return info #front-end needs data


#read --- all
@app.get('/history')
def create(db: Session = Depends(ini_db)):
    rows = db.query(Expression).order_by(Expression.created_at.desc()).all()
    return rows

#read --- one
@app.get('/history/{expr_id}')
def create_one(expr_id, db: Session = Depends(ini_db)):
    row = db.query(Expression).filter(Expression.id == expr_id).first()
    
    if row is None:
        return {'error': 'Expression not found'}
    
    return row

#read --- query
@app.get('/history/search/{query}')
def search(query, db: Session = Depends(ini_db)):
    rows = (
        db.query(Expression)
        .filter(Expression.expression.contains(query))
        .order_by(Expression.created_at.desc())
        .all()
    )

    if not rows:
        return {'error': 'Expression does not exist, please try again'}

    return rows

#delete
@app.delete('/history/{expr_id}')
def delete(expr_id, db: Session = Depends(ini_db)):
    row = db.query(Expression).filter(Expression.id == expr_id).first()

    if row is None:
        return {'error': 'Expression not found'}
    
    db.delete(row)
    db.commit()

    return {'success':'Expression deleted'}