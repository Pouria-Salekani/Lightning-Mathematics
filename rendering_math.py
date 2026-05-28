import math
import random
from opensimplex import OpenSimplex

noise = OpenSimplex(seed=55)


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
#TODO: change name and clear variables
def perpen_displacement(pts, per_x, per_y, time):
    new_p = []
    branch = []
    is_called = False
    #L = 15
    for i in range(len(pts) - 1):
        s = i / len(pts)    #normalization
        pertrub = noise.noise2(s * 15, time) * 10
        L = random.uniform(5,20) #need to fix this
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
        if r <= 0.4:
            branch_endpoint = (new_midpt_total[0] + L*norm_vector[0], new_midpt_total[1] + L*norm_vector[1])
            branch.append((new_midpt_total, branch_endpoint)) #the start is at the midpoint, thats where the branch starts
        

    return new_p, branch 
