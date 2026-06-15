from sympy import lambdify, sympify, symbols, pi
from math import sin, cos
import rendering_math as render
import numpy as np
import encyclopedia

x = symbols('x')
theta_ = symbols('theta')
t = symbols('t') # parametric
user_expr = sympify('pi')

def user_input(m_variable): 
    res = None
    error = None
    info = None
    
    if m_variable.strip() == '':    
        return None, 'Invalid syntax.', None
    
    elif ',' in m_variable:    #parametric
        expressions = m_variable.split(',')
        expr1 = expressions[0].strip() 
        expr2 = expressions[1].strip()

        try:
            s_expr1 = sympify(expr1)
            s_expr2 = sympify(expr2)

        except:
            return None, 'Invalid syntax for parametric expression', info
        
        if s_expr1.free_symbols != {t} or s_expr2.free_symbols != {t}:
            return None, 'For parametric, symbols MUST match "t". Please see instructions for examples.', None
        
        f_x = lambdify(t, s_expr1, 'math')
        f_y = lambdify(t, s_expr2, 'math')
        

        res, bundle = render.generate_parametric(f_x, f_y)
        info = encyclopedia.expression_analyzer(t, (s_expr1, s_expr2), expressions, bundle)
        
        #res, ls = render.generate_parametric(f_x, f_y)
        if len(res) <= 2:
            error = 'Graph is outside the screen, please try a smaller constant.'

        return res, error, info
        #return render.generate_parametric(f_x, f_y), None
    
    try:
        user_expr = sympify(m_variable, locals={'pi':pi})
    except:
        return None, 'Invalid, please press "?" for instructions.', None
    
    inpt = user_expr.free_symbols 

    if not inpt.issubset({x,theta_,t}):
        error = 'Unrecognized variable. Please use x, theta, or t.'

    elif inpt == {t}:
        error = 'Parametric expressions require a comma. Example: sin(-3*t), cos(t).'

    elif len(inpt) > 1:
        error = 'Hybrid variables are not supported at this time. Please see the instructions.'
        
    elif inpt == {x} or inpt == set():
        equation = user_expr #so, sin(x), cos(x), x^2, etc...
        f = lambdify(x, equation, 'math')
        
        #encyclopedia.test(m_variable)
       
        res, bundle = render.generate_single(f)
        info = encyclopedia.expression_analyzer(x, equation, m_variable, bundle)
        
        if len(res) <= 2:
            error = 'Graph is outside the screen, please try a smaller constant.'
    
    elif inpt == {theta_}:
        equation = user_expr #like sin(5*theta)
        f = lambdify(theta_, equation, 'math')

        res, bundle = render.generate_polar(f)
        info = encyclopedia.expression_analyzer(theta_, equation, m_variable, bundle)
        
        #res, ls = render.generate_polar(f)
        if len(res) <= 2:
            error = 'Graph is outside the screen, please try a smaller constant.'

    return res, error, info

