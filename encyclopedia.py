from sympy import diff, S, solve
from sympy.calculus.util import function_range, continuous_domain


import text_formatter
import config

# x = symbols('x')
# theta = sympify('theta')
# t = sympify('t')
# print(ww)
# f = lambdify(x, ww, 'math')
# fix Union(Interval.open(-oo, -2), 
# Interval.open(-2, 2), Interval.open(2, oo)), 'range': Union(Interval(-oo, -1/4), Interval.open(0, oo)
#read from user input to determine type


#TODO: add ANOTHER info thats specific for PARAMETRIC onlly
#it needs domain for x and y as eell as range for x and y


def test(t):
    print(t)

def find_symbol(symbol):
    if symbol.free_symbols == {config.X}:
        return 'x'
    elif symbol.free_symbols == {config.THETA}:
        return 'theta'
    else:
        return 't'

def expression_analyzer(symbol, expr, user_input, bundle): #(symb, expr)
    # g = [j for i,j,q,o in roots] #range
    # gm = min(g)
    # gmax = max(g)
    # gs = []
    # gt = []
    # roots, range = None
    # print(bundle)

    if bundle:
        roots, range = bundle

    # q = continuous_domain(expr[0], symbol, S.Reals).intersect(continuous_domain(expr[1], symbol, S.Reals))
    # print(text_formatter.complement_andelse_pretty(q))
    # print('q', type(q), q.args)
    # e,r = q.args
    # print('e', type(e), e.args)
    # print('r', type(r), r.args)
    # print()
    
    # for j in r.args:
    #     print(j, '---->>>', j.lamda, j.lamda.args, j.lamda.args[1])
        #for solns for tan when the domain is messy
        #for parametric, domain is always an intersection
        #make a separate case on where something like complement or image set exists

    # print(symbol, expr, user_input)
    # flag = False
    # string_symbol = find_symbol(symbol) 
    # symb_counter = user_input.count(f'{string_symbol}') #if symbol in {config.}
    # print(symb_counter, string_symbol)
    
    # if symb_counter >= 2:
    #     flag = False

    #TODO: also add notimplementederror for here
    if type(expr) == tuple and len(expr) == 2:
        try:
            INFO = {
            'Input': user_input,
            'Type': 'Parametric',   
            'Left Derivative': diff(expr[0]),
            'Right Derivative': diff(expr[1]),
            #'roots_left': solve(expr[0]),
            #'roots_right': solve(expr[1]),
            #'roots' : gs,
            'Roots': roots if roots else 'None',
            # 'left_domain': continuous_domain(expr[0], symbol, S.Reals),
            # 'right_domain': continuous_domain(expr[1], symbol, S.Reals),
            'Domain': text_formatter.make_pretty_text(continuous_domain(expr[0], symbol, S.Reals)
                                    .intersect(continuous_domain(expr[1], 
                                    symbol, S.Reals))),
            # 'left_range': function_range(expr[0], symbol, S.Reals),
            # 'right_range': function_range(expr[0], symbol, S.Reals)
        # 'range': (gm, gmax)
            'Range': text_formatter.make_pretty_text(function_range(
                                    expr[1], symbol, S.Reals))    #just use it for y(t)
                                                                #so expr[1]

            }
        except NotImplementedError:
             print('NOT IMPLEMENTED ^^^PARAMETRIC')
             INFO = {
            'Input': user_input,
            'Type': 'Parametric',   
            'Left Derivative': diff(expr[0]),
            'Right Derivative': diff(expr[1]),
            'Roots (approximated)': roots if roots else 'None',
            'Domain': 'Cannot compute due to expression complexity',
            'Range (approximated)':range
             }

    else:
       # print(user_input.count('x') >= 2) then skip for trigs
        try:
            INFO = {
            'Input': user_input,
            'Type': 'Single' if symbol.free_symbols == {config.X} else 'Polar',
            'Derivative': diff(expr, symbol),
            'Roots': solve(user_input),
            'Domain':text_formatter.make_pretty_text(continuous_domain(expr, symbol, S.Reals)),
                               # if not flag else 'Cannot compute due to expression complexity', 
            'Range': text_formatter.make_pretty_text(function_range(expr, symbol, S.Reals))
                               #if not flag else 'Cannot compute due to expression complexity'
            }
        except NotImplementedError:
            print('NOT IMPLEMENT ERROR')
            INFO = {
            'Input': user_input,
            'Type': 'Single' if symbol.free_symbols == {config.X} else 'Polar',
            'Derivative': diff(expr, symbol),
            'Roots (approximated)': roots if roots else 'None',
            'Domain':'Cannot compute due to expression complexity', 
            'Range (approximated)': range
            }

    print(INFO)
    return INFO


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



