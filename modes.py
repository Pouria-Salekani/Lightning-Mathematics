from sympy import lambdify, sympify, symbols
from config import center, SCALE
import math
from math import sin, cos

x = symbols('x')
theta_ = symbols('theta')
t = symbols('t') # parametric

user_expr = sympify('cos(theta)')

m_variable = user_expr.free_symbols
print(m_variable)

mode = None #user generated


def graph_to_screen(x, y):
    X = center[0] + x*SCALE #right
    Y = center[1] - y*SCALE #up
    return X,Y


x = symbols('x')
y = symbols('y')
equation_x = 'sin(x)' #will be user inputted
equation_y = 'cos(y)'
expression_x = sympify(equation_x)
expression_y = sympify(equation_y)
f_x = lambdify(x, expression_x, 'math')
f_y = lambdify(y, expression_y, 'math')


#TODO: bunch everything up in a function and eventually call the renderer below for the respective mode
def user_input(m_variable): 
    if ',' in m_variable:    #parametric
        expressions = m_variable.split(',')
        expr1 = expressions[0].strip() 
        expr2 = expressions[1].strip()
        f_x = lambdify(t, sympify(expr1), 'math')
        f_y = lambdify(t, sympify(expr2), 'math')
        return generate_parametric(f_x, f_y)
    
    user_expr = sympify(m_variable)
    inpt = user_expr.free_symbols

    if inpt == {x}:
        equation = user_expr #so, sin(x), cos(x), x^2, etc...
        f = lambdify(x, equation, 'math')
        return generate_single(f)

    elif inpt == {theta_}:
        #print('CHECK and --> ', user_expr, lambdify(theta, user_expr, 'math'), type(user_expr))
        equation = user_expr #like sin(5*theta)
        f = lambdify(theta_, equation, 'math')
        return generate_polar(f)

    raise ValueError('This expression is not supported, please see the instructions.')

    #TODO: parametric
    #if [0] == ( and [-1] == )
        #then mode = parametric



#user_input(m_variable)


def generate_single(f):
    points = []
    for i in range(-600,601, 5):
        x = i / SCALE
        try:
            y = f(x)
        except:
            continue

        points.append((graph_to_screen(x,y)))

    return points

def generate_polar(f):
    points = []
    for i in range(0, 2000, 10):
        theta = i / 100 #TODO: change scaling later
        r = f(theta)
        x = 5 * r * cos(theta)
        y = 5 * r * sin(theta)

        points.append((graph_to_screen(x,y)))

    return points

def generate_parametric(f_x, f_y):
    points = []
    for i in range(0, 1500, 5):
        t = i / 100 #TODO: change scaling later
        x = 3 * f_x(t)
        y = 3 * f_y(t)

        points.append((graph_to_screen(x,y)))

    return points

# if m_variable == {x}:
#     mode = 'single'

# elif m_variable == {theta}:
#     mode = 'polar'

# elif m_variable == {t}:
#     mode = 'error'






#if single i.e. explicit, parametric, or polar then set mode ====> operate

