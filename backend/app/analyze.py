from sympy import diff, S, solve
from sympy.calculus.util import function_range, continuous_domain
from app import text_formatter as text_formatter
from app import config


def find_symbol(symbol):
    if symbol.free_symbols == {config.X}:
        return 'x'
    elif symbol.free_symbols == {config.THETA}:
        return 'theta'
    else:
        return 't'


#TODO: for the database, it only like str values or ints, floats, etc...
#sympy wont work
def expression_analyzer(symbol, expr, user_input, bundle): 
    if bundle:
        roots, range = bundle

    print(expr, type(expr))

    if type(expr) == list and len(expr) == 2:
        try:
            
            
            INFO = {
            'Input': user_input,
            'Type': 'Parametric',   
            'Left Derivative': diff(expr[0]),
            'Right Derivative': diff(expr[1]),
            'Roots': roots if roots else 'None',
            'Domain': text_formatter.make_pretty_text(continuous_domain(expr[0], symbol, S.Reals)
                                    .intersect(continuous_domain(expr[1], 
                                    symbol, S.Reals))),
            'Range': range                          #just use it for y(t)
                                                            #so expr[1]

            }
        except NotImplementedError:
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
        try:
            roots = solve(user_input)
            if len(roots) >= 5:
                temp = roots[:3]
                
            INFO = {
            'Input': user_input,
            'Type': 'Single' if symbol.free_symbols == {config.X} else 'Polar',
            'Derivative': diff(expr, symbol),
            'Roots': roots if len(roots) < 5 else '[' + ', '.join(map(str,temp)) + ', ...' + ']',
            'Domain':text_formatter.make_pretty_text(continuous_domain(expr, symbol, S.Reals)),
                               # if not flag else 'Cannot compute due to expression complexity', 
            'Range': text_formatter.make_pretty_text(function_range(expr, symbol, S.Reals))
                               #if not flag else 'Cannot compute due to expression complexity'
            }
        except NotImplementedError:
            INFO = {
            'Input': user_input,
            'Type': 'Single' if symbol.free_symbols == {config.X} else 'Polar',
            'Derivative': diff(expr, symbol),
            'Roots (approximated)': roots if roots else 'None',
            'Domain':'Cannot compute due to expression complexity', 
            'Range (approximated)': range
            }
    INFO = {k: str(v) for k, v in INFO.items()}
    if '[' in INFO['Input']:
        INFO['Input'] = text_formatter.remove_brackets(INFO['Input']) 
    return INFO

