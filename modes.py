from sympy import lambdify, sympify, symbols
from config import center, SCALE
from math import sin, cos

x = symbols('x')
theta = symbols('theta')
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
    if ',' in user_expr:    #parametric
        expressions = user_expr.split(',')
        expr1 = expressions[0].strip() 
        expr2 = expressions[1].strip()
        f_x = lambdify(t, sympify(expr1), 'math')
        f_y = lambdify(t, sympify(expr2), 'math')
        generate_parametric(f_x, f_y)

    elif m_variable == {x}:
        mode = 'single'
        equation = m_variable #so, sin(x), cos(x), x^2, etc...
        f = lambdify(x, sympify(equation), 'math')
        generate_single(f)

    elif m_variable == {theta}:
        #print('CHECK and --> ', user_expr, lambdify(theta, user_expr, 'math'), type(user_expr))
        mode = 'polar'
        equation = None #like sin(5*theta)
        f = lambdify(theta, sympify(equation), 'math')
        generate_polar(f)

    elif m_variable == {t}:
        mode = 'error'


    return mode

    #TODO: parametric
    #if [0] == ( and [-1] == )
        #then mode = parametric



#user_input(m_variable)


def generate_single(f):
    points = []
    for i in range(-600,601, 5):
        x = i / SCALE
        y = f(x)

        points.append((graph_to_screen(x,y)))

    return points

def generate_polar(f):
    points = []
    for i in range(0, 2000, 10):
        theta_ = i / 100 #TODO: change scaling later
        r = f(theta_)
        x = r * cos(theta_)
        y = r * sin(theta_)

        points.append((graph_to_screen(x,y)))

    return points

def generate_parametric(f_x, f_y):
    points = []
    for i in range(0, 1500, 5):
        t = i / 100 #TODO: change scaling later
        x = f_x(t)
        y = f_y(t)

        points.append((graph_to_screen(x,y)))

    return points

# if m_variable == {x}:
#     mode = 'single'

# elif m_variable == {theta}:
#     mode = 'polar'

# elif m_variable == {t}:
#     mode = 'error'






#if single i.e. explicit, parametric, or polar then set mode ====> operate

