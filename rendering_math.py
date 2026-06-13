import math
from math import sin, cos
import random
from opensimplex import OpenSimplex
import config

noise = OpenSimplex(seed=55)


def polar_roots(ls):
    roots = []
    for i in range(len(ls)-1):
        x1, y1, r1, theta1 = ls[i]
        x2, y2, r2, theta2 = ls[i+1]        
        if r1*r2 < 0:
            roots.append(round((theta1+theta2)/2, 2))

    # print(ls)
    # print(sorted(list(set(ls))[:10]))
    return sorted(list(set(roots)))[:10] #remove duplicates 

def parametric_roots(ls):  #not really 'roots' more like x-axis crossings
    roots = []  
    for i in range(len(ls)-1):
            x1, y1, t1 = ls[i]
            x2 ,y2, t2 = ls[i+1]
            if y1*y2 < 0:
                roots.append(round((x1+x2)/2,2))

    return sorted(list(set(roots)))[:10]

def graph_to_screen(x, y):
    X = config.center[0] + x*config.SCALE #right
    Y = config.center[1] - y*config.SCALE #up
    return X,Y


def generate_single(f):
    points = []
    for i in range(-600,601, 5):
        x = i / config.SCALE
        try:
            y = f(x)
        except:
            continue

        points.append((graph_to_screen(x,y)))

    return points, None


def generate_polar(f):
    points = []
    ls = []
    for i in range(1, 2000, 10):
        theta = i / 100 #TODO: change scaling later
        r = f(theta)
        x = 3 * r * cos(theta)
        y = 3 * r * sin(theta)

        #TODO: add auto-scaling for all of the graphs
        x_,y_ = graph_to_screen(x,y)
        if -100 < x_ < 100 + config.WIDTH and -100 < y_ < 100 + config.HEIGHT:
            points.append((x_,y_))
            ls.append((x_ / 3, y_ / 3, r, theta))
    
    root_ls = polar_roots(ls)
    return points, root_ls

def generate_parametric(f_x, f_y):
    points = []
    ls = []
    for i in range(1, 1100, 5):
        t = i / 100 #TODO: change scaling later
        x = 3 * f_x(t)
        y = 3 * f_y(t)

        points.append((graph_to_screen(x,y)))
        ls.append((x / 3, y / 3, t))  #ADD THE RAW VALUES NOT SCALED

    root_ls = parametric_roots(ls)
    return points, root_ls

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
