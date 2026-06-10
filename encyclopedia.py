from sympy import lambdify, sympify, symbols, diff, S, Interval, Union, sstr
from sympy.calculus.util import function_range, continuous_domain


import math

x = symbols('x')
ww = sympify('1/x**2')
print(ww)
f = lambdify(x, ww, 'math')
# fix Union(Interval.open(-oo, -2), 
# Interval.open(-2, 2), Interval.open(2, oo)), 'range': Union(Interval(-oo, -1/4), Interval.open(0, oo)
#read from user input to determine type


#TODO: add ANOTHER info thats specific for PARAMETRIC onlly
#it needs domain for x and y as eell as range for x and y


def test(t):
    print(t)


def expression_analyzer(text): #(symb, expr)
    symbol, expr = text
    #INFO = {}

    if type(expr) == tuple and len(expr) == 2:
        INFO = {
        'input': None,
        'type': None,
        'left_deriv': None,
        'right_deriv': None,
        'roots': None,
        'left_domain': None,
        'right_domain': None,
        'left_range': None,
        'right_range': None

        }
    else: 
        INFO = {
        'input': None,
        'type': None,
        'derivative': None,
        'roots': None,
        'domain': None,
        'range': None
        }

    print(INFO)
    return


INFO = {
    'input': None,
    'type': None,
    'derivative': None,
    'roots': None,
    'domain': None,
    'range': None

}

INFO_parametric = {
    'input': None,
    'type': None,
    'derivative for (left of comma user input)': None,
    'derivate for (right of comma user input)': None,
    'roots': None,
    'domain for (left of comma user input)': None,
    'domain for (right of comma user input)': None,
    'range for (left of comma user input)': None,
    'range for (right of comma user input)': None
}




INFO['input'] = ww
INFO['derivative'] = diff(ww, x)
INFO['domain'] = continuous_domain(ww, x, S.Reals)
g = function_range(ww, x, S.Reals)
ff = continuous_domain(ww, x, S.Reals)




def make_som(g):
    if isinstance(g, Interval):
        left = '(' if g.left_open else '['
        right = ')' if g.right_open else ']'
        pretty_text = f'{left}'+f'{g.start}, {g.end}'+f'{right}'

        return pretty_text

def what(ff):
    print(ff)
    print(type(ff))
    if isinstance(ff, Union):
        res = ''
        for i in ff.args:
            res += make_som(i) + ' U '

        print(res[-1], res[-2])
        return res if res[-1] != ' ' else res[:-2]
    

def func_info(f):   #(symbol, (sympfy1, sympfy2)) for parametric, check if len == 2
    print('SUCCESS')
    expression, func = f
    if type(func) == tuple and len(func) == 2:  #works, for parametric, do a loop in an if statement
        print('PARAMETRIC ', func, func[0], func[1])
        print(expression,'---', func)
        return
    else:
        return
    try:
        range = function_range(func, expression, S.Reals)  #sympfy, symbol
        domain = continuous_domain(func, expression, S.Reals)

        if range:
            if isinstance(range, Union):
                return #TODO: call union func
            elif isinstance(range, Interval):
                return #TODO: call interval func
            
        if domain:
            if isinstance(domain, Union):
                return #TODO: call union func
            elif isinstance(domain, Interval):
                return #TODO: call interval func

    
    except NotImplementedError: #important
        INFO['range'] = 'Impossible'
        print(INFO)
    #print(what(ff), 'HHHHHH')
        
#EITGER DOMAIN OR RANGE COUDL HAVE A UNION OR INTERVAL, SO U NEED 4 CASES TOTAL
    #actually u just need 2. if its union, its gonna cal interval, if its interval
        #then, thats it but make sure to check for all 4, i guess 4 if statements

# print(what())

#only for intervals, unions will be different

#cleaning the interval stuff type

INFO['range'] = None



# print(sstr(function_range(ww, x, S.Reals)))
# print(INFO)

