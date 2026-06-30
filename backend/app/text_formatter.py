from sympy import Interval, Union

def complement_andelse_pretty(f):
    _, text = f.args
    ls = []
    flag = True
    
    for t in text.args:
        if hasattr(t, 'lamda'):
            flag = False

    if flag:
        return str(f)

    for i in text.args:
        temp = str(i.lamda.args[1])
        new_text = temp.replace('_n', 'n').replace('pi', 'π')
        ls.append(new_text)
    return '[' + ', '.join(ls) + ']'


def interval_pretty(f):
    if isinstance(f, Interval):
        left = '(' if f.left_open else '['
        right = ')' if f.right_open else ']'
        pretty_text = f'{left}'+f'{f.start}, {f.end}'+f'{right}'

        return pretty_text
    return 'Cannot compute due to expression complexity'

def union_pretty(f):
    text = ''
    for i in f.args:
        text += interval_pretty(i) + ' U '
        if text[:6] == 'Cannot':
            return 'Cannot compute due to expression complexity'

    return text if text[-1] != ' ' else text[:-2]
    

def make_pretty_text(f):   #(symbol, (sympfy1, sympfy2)) for parametric, check if len == 2
    try:
        if isinstance(f, Union):
            return union_pretty(f)
        elif isinstance(f, Interval):
            return interval_pretty(f)
        else:
            return complement_andelse_pretty(f)
    
    except NotImplementedError:
        return 'Undefined'


def remove_brackets(s):
    return s[1:-1].replace("'",'')
