import pygame
import math
import random
from sympy import lambdify, sympify, symbols
from opensimplex import OpenSimplex
from colors import WHITE, CYAN, BLACK, DARK_BLUE, PURPLE, BLUE


pygame.init()
WIDTH, HEIGHT = 900, 900
SCALE = 40
window = pygame.display.set_mode((WIDTH, HEIGHT))
center = (WIDTH//2, HEIGHT//2)
# DOMAIN = 

noise = OpenSimplex(seed=55)
# Converting (x_i, y_i) to screen coordinates. Scaling is important to avoid microscopic moves
def graph_to_screen(x, y):
    X = center[0] + x*SCALE #right
    Y = center[1] - y*SCALE #up
    return X,Y


#regular displacement i.e. midpt dispplacement
def jagg(pts , per_x, per_y):
    new_p = []
    for i in range(len(pts)-1):
        pertrub_x = random.uniform(per_x,per_y)
        pertrub_y = random.uniform(per_x, per_y)
        x1,y1 = pts[i]
        x2,y2 = pts[i+1]

        midpt = (((x1+x2)/2) + pertrub_x, ((y1+y2)/2) + pertrub_y)

        new_p.append(pts[i])
        new_p.append(midpt)
        new_p.append(pts[i+1])
    return new_p

def midpoint():
    return

#this needs polishing
#TODO: polish branch displacement
def branch_displacement(pts, per_x, per_y):
    new_p = []
    for i in range(len(pts)-1):
        pertrub = random.uniform(per_x,per_y)
        s = i / len(pts)
        #pertrub = noise.noise2(s * 10, time) * 20
        L = random.uniform(5,20) #need to fix this
        x1,y1 = pts[i]
        x2,y2 = pts[i+1]

        perpen_vector = (-(y2-y1), x2-x1)

        #computing normalization for pepn_vector
        magnitude = math.sqrt((perpen_vector[0]**2 + perpen_vector[1]**2))  #avoiding pts very close to each other
        if magnitude == 0:
            continue
        norm_vector = (perpen_vector[0] / (magnitude), perpen_vector[1] / (magnitude))


        #midpt = (((x1+x2)/2) + pertrub, ((y1+y2)/2) + pertrub)
        new_midpt_x = (x1+x2)/2 + pertrub*norm_vector[0]
        new_midpt_y = (y1+y2)/2 + pertrub*norm_vector[1]
        new_midpt_total = (new_midpt_x, new_midpt_y)

        new_p.append(pts[i])
        new_p.append(new_midpt_total)
        new_p.append(pts[i+1])

    return new_p


#perpendicular displacement (more accurate for jaggedness)
def perpen_displacement(pts, per_x, per_y, time, noise_l):
    new_p = []
    branch = []
    is_called = False
    #L = 15
    for i in range(len(pts)-1):
        #pertrub = random.uniform(per_x,per_y)
        #pertrub = noise.noise2(i*0.005, time) * 20
        s = i / len(pts)    #normalization
        #pertrub = noise[i]
        pertrub = noise.noise2(s * 15, time) * 10
        L = random.uniform(5,20) #need to fix this
        x1,y1 = pts[i]
        x2,y2 = pts[i+1]

        vector = (x2-x1, y2-y1)
        perpen_vector = (-(y2-y1), x2-x1)

        #computing normalization for pepn_vector
        magnitude = math.sqrt((perpen_vector[0]**2 + perpen_vector[1]**2))  #avoiding pts very close to each other
        if magnitude == 0:
            continue
        norm_vector = (perpen_vector[0] / (magnitude), perpen_vector[1] / (magnitude))

        r = random.uniform(0,1)
        #pertrub *= 15

        #midpt = (((x1+x2)/2) + pertrub, ((y1+y2)/2) + pertrub)
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
            #super_branch = branch_displacement(branch, per_x, per_y)
            #is_called = True

    return new_p, branch #if is_called else branch

# def f(x):
#     #return math.sin(x)
#     x = symbols('x')
#     equation = 'sin(x)'
#     expression = sympify(equation)
#     f = lambdify(x, expression, 'math')
#     return lambdify(x, expression, 'math')


x = symbols('x')
y = symbols('y')
equation_x = 'sin(x)' #will be user inputted
equation_y = 'cos(y)'
expression_x = sympify(equation_x)
expression_y = sympify(equation_y)
f_x = lambdify(x, expression_x, 'math')
f_y = lambdify(y, expression_y, 'math')


run = True
time = 0
while run:
    window.fill((0,0,0)) #so everything shows up
    time += 0.09
    
    pygame.draw.line(window, (255,255,255), (0, center[0]), (WIDTH, center[0])) #x-axis
    pygame.draw.line(window, (255,255,255), (center[0], 0), (center[0], HEIGHT))  #y-axis
    points = []
    branches = []
    noise_ls = []

    #domain for sin
    for idx, i in enumerate(range(0,1500, 5)):
        # x = i / SCALE #this is the domain, we want many domains, domain is [-i / SCALE, i / SCALE]
        # y = f(x)
        t = i / 200
        x = 3*math.sin(5*t)#t*f_x(t)            #SPIRAL RANGE[0,900] and 55 as scale --- Polar is the same but [0,1500]
        y = 3*math.sin(4*t) #t*f_y(t)

        #THIS IS POLAR
        # t = i / 100
        # r = 0.1*t
        # x = 5*r * math.cos(t)
        # y = 5*r * math.sin(t)


        points.append((graph_to_screen(x,y)))
        #noise_ls.append(noise.noise2(idx * 0.005, time) * 20)
    
    
    # jagged_pts = []
    
    # #going thru the pts
    # for i in range(len(points)-1):
    #     pertrub_x = random.uniform(-5,5)
    #     pertrub_y = random.uniform(-5, 5)
    #     x1,y1 = points[i]
    #     x2,y2 = points[i+1]

    #     midpt = (((x1+x2)/2) + pertrub_x, ((y1+y2)/2) + pertrub_y)

    #     jagged_pts.append(points[i])
    #     jagged_pts.append(midpt)
    #     jagged_pts.append(points[i+1])

    #will get recursively cuz of the infinite while loop
    # jagged_pts, b1 = perpen_displacement(points, -10, 10)
    # jagged_pts, b2 = perpen_displacement(jagged_pts, -6, 6)
    # jagged_pts, b3 = perpen_displacement(jagged_pts, -3, 3)

    jagged_pts, b1 = perpen_displacement(points, -10, 10, time, noise_ls)
    jagged_pts, b2 = perpen_displacement(jagged_pts, -6, 6, time, noise_ls)
    jagged_pts, b3 = perpen_displacement(jagged_pts, -3, 3, time, noise_ls)
    branches = b1 + b2 + b3     #adding them all up because **DON'T** OVERIDE, unlike jagged_pts



    # j = 0
    # new_p = []
    # #print(len(mid), len(points))
    # for i in range(len(points)-1):
    #     new_p.append(points[i])
    #     new_p.append(mid[i])
    #     new_p.append(points[i+1])
        


    #thicker/fuller colors first
    pygame.draw.lines(window, BLACK, False, jagged_pts, 12)

    pygame.draw.lines(window, DARK_BLUE, False, jagged_pts, 6)

    pygame.draw.lines(window, CYAN, False, jagged_pts, 2)


    #a loop for branches cuz theyre all diff
    for x, y in branches:   #need to come up with a better color scheme
        pts = [x,y]     #branches is a 3D, so doing this, makes it 2D, like so: [(......), (......)]
        jagged_branch = branch_displacement(pts, -8, 8)
        jagged_branch = branch_displacement(jagged_branch, -3, 3)
        # pygame.draw.line(window, DARK_BLUE, x, y, 3)
        # pygame.draw.line(window, CYAN, x, y, 2) #maybe add sliders to the colors' thickness value?
        pygame.draw.lines(window, DARK_BLUE, False, jagged_branch, 4)
        pygame.draw.lines(window, CYAN, False, jagged_branch, 2)




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
pygame.quit()

