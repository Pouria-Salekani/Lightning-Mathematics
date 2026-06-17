import math
from math import sin, cos
import random
from opensimplex import OpenSimplex
import config
from sympy import solve

noise = OpenSimplex(seed=55)


def check_on_screen(x,y):
    return -100 < x < 100 + config.WIDTH and -100 < y < 100 + config.HEIGHT

def range_func(ls):
    if len(ls[0]) == 4: #polar
        num = [r for _,_,r,_ in ls]
        return (min(num), max(num))
    else:
        num = [y for _,y,_ in ls]
        return (min(num), max(num))

def polar_roots(ls):
    roots = []
    for i in range(len(ls)-1):
        x1, y1, r1, theta1 = ls[i]
        x2, y2, r2, theta2 = ls[i+1]        
        if r1*r2 < 0:
            roots.append(round((theta1+theta2)/2, 2))

   
    return sorted(list(set(roots)))[:10] #remove duplicates 

def roots(ls):  #not really 'roots' more like x-axis crossings
    roots = []  
    for i in range(len(ls)-1):
            x1, y1, t1 = ls[i]
            x2 ,y2, t2 = ls[i+1]
            if y1*y2 < 0: #y(t) = 0 --- x-intercepts
                roots.append(round((x1+x2)/2,2))
    
    return sorted(list(set(roots)))[:10]

def graph_to_screen(x, y):
    X = config.center[0] + x*config.SCALE #right
    Y = config.center[1] - y*config.SCALE #up
    return X,Y


def generate_single(f):
    points = []
    ls = []
    for i in range(-700,701, 5):
        x = i / config.SCALE
        try:
            y = f(x)
            if isinstance(y, complex):
                continue
            elif not math.isfinite(y):
                continue
        except:
            continue

        x_,y_ = graph_to_screen(x,y)
        if check_on_screen(x_,y_):
            points.append((x_,y_))
            ls.append((x, y, i))

    if ls:
        root_ls = roots(ls)
        range_ls = range_func(ls)
        return points, (root_ls, range_ls)
    else:
        return points, (0,0)


def generate_polar(f):
    points = []
    ls = []
    for i in range(1, 2000, 10):
        theta = i / 100 
        r = f(theta)
        if isinstance(r, complex):
            continue
        x = 3 * r * cos(theta)
        y = 3 * r * sin(theta)



        #TODO: add auto-scaling for all of the graphs
        x_,y_ = graph_to_screen(x,y)
        if check_on_screen(x_,y_):
            points.append((x_,y_))
            ls.append((x / 3, y / 3, r, theta))   #??? why is this x_ / 3...
    if ls:
        root_ls = polar_roots(ls)
        range_ls = range_func(ls)
        return points, (root_ls, range_ls)
    else:
        return points, (0,0)

def generate_parametric(f_x, f_y):
    points = []
    ls = []
    for i in range(1, 1100, 5):
        t = i / 100 
        x = 3 * f_x(t)
        y = 3 * f_y(t)
        if isinstance(x,complex) or isinstance(y, complex):
            continue

        x_,y_ = graph_to_screen(x,y)
        if check_on_screen(x_,y_):
            points.append((x_,y_))
            ls.append((x / 3, y / 3, t)) 

    
    if ls:
        root_ls = roots(ls)
        range_ls = range_func(ls)
        return points, (root_ls, range_ls)
    else:
        return points, (0,0)

# follows a random procedure, no simplex noise
def branch_displacement(pts, per_x, per_y):
    new_p = []
    for i in range(len(pts) - 1):
        pertrub = random.uniform(per_x,per_y)
       
        x1,y1 = pts[i]
        x2,y2 = pts[i+1]

        perpen_vector = (-(y2-y1), x2-x1)

        #computing normalization for pepn_vector
        magnitude = math.sqrt((perpen_vector[0]**2 + perpen_vector[1]**2))  #avoiding pts very close to each other
        if magnitude == 0:
            continue
        norm_vector = (perpen_vector[0] / (magnitude), perpen_vector[1] / (magnitude))

        new_midpt_x = (x1+x2)/2 + pertrub*norm_vector[0]
        new_midpt_y = (y1+y2)/2 + pertrub*norm_vector[1]
        new_midpt_total = (new_midpt_x, new_midpt_y)

        new_p.append(pts[i])
        new_p.append(new_midpt_total)
        new_p.append(pts[i+1])

    return new_p


# simplex noise displacement, the smoothing function
def simplex_midpoint_disp(pts, time):
    new_p = []
    branch = []
   
    for i in range(len(pts) - 1):
        s = i / len(pts)    #normalization
        pertrub = noise.noise2(s * 15, time) * 10
        L = random.uniform(5,20) 
        x1,y1 = pts[i]
        x2,y2 = pts[i+1]

        perpen_vector = (-(y2-y1), x2-x1)

        #computing normalization for pepn_vector
        magnitude = math.sqrt((perpen_vector[0]**2 + perpen_vector[1]**2)) 
        if magnitude == 0:
            continue
        norm_vector = (perpen_vector[0] / (magnitude), perpen_vector[1] / (magnitude))

        r = random.uniform(0,1)

        new_midpt_x = (x1+x2)/2 + pertrub*norm_vector[0]
        new_midpt_y = (y1+y2)/2 + pertrub*norm_vector[1]
        new_midpt_total = (new_midpt_x, new_midpt_y)

        new_p.append(pts[i])
        new_p.append(new_midpt_total)
        new_p.append(pts[i+1])

        #branching lightning at new_midpot_total
        if r <= config.BRANCHING_PROBABILITY:
            branch_endpoint = (new_midpt_total[0] + L*norm_vector[0], new_midpt_total[1] + L*norm_vector[1])
            branch.append((new_midpt_total, branch_endpoint)) #the start is at the midpoint, thats where the branch starts
        

    return new_p, branch 
