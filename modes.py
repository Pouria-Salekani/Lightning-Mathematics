from sympy import lambdify, sympify, symbols

x = symbols('x')
theta = symbols('theta')
t = symbols('t') # parametric

user_expr = sympify('cos(theta)')

m_variable = user_expr.free_symbols
print(m_variable)

mode = None #user generated

#TODO: bunch everything up in a function and eventually call the renderer below for the respective mode
if m_variable == {x}:
    mode = 'single'

elif m_variable == {theta}:
    mode = 'polar'

elif m_variable == {t}:
    mode = 'error'

#TODO: parametric
#if [0] == ( and [-1] == )
    #then mode = parametric





#if single i.e. explicit, parametric, or polar then set mode ====> operate

