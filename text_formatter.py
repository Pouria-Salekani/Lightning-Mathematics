from sympy import Interval, Union


def interval_pretty(f):
    if isinstance(f, Interval):
        left = '(' if f.left_open else '['
        right = ')' if f.right_open else ']'
        pretty_text = f'{left}'+f'{f.start}, {f.end}'+f'{right}'

        return pretty_text

def union_pretty(f):
    text = ''
    for i in f.args:
        text += interval_pretty(i) + ' U '

    return text if text[-1] != ' ' else text[:-2]
    

def make_pretty_text(f):   #(symbol, (sympfy1, sympfy2)) for parametric, check if len == 2
    try:
        if isinstance(f, Union):
            return union_pretty(f)
        elif isinstance(f, Interval):
            return interval_pretty(f)
    
    except NotImplementedError:
        return 'Undefined'
    