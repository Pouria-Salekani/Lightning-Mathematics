import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 900, 900
SCALE = 55
window = pygame.display.set_mode((WIDTH, HEIGHT))
center = (WIDTH//2, HEIGHT//2)
# DOMAIN = 

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
def perpen_displacement(pts, per_x, per_y):
    new_p = []
    branch = []
    is_called = False
    #L = 15
    for i in range(len(pts)-1):
        pertrub = random.uniform(per_x,per_y)
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

        #midpt = (((x1+x2)/2) + pertrub, ((y1+y2)/2) + pertrub)
        new_midpt_x = (x1+x2)/2 + pertrub*norm_vector[0]
        new_midpt_y = (y1+y2)/2 + pertrub*norm_vector[1]
        new_midpt_total = (new_midpt_x, new_midpt_y)

        new_p.append(pts[i])
        new_p.append(new_midpt_total)
        new_p.append(pts[i+1])

        #branching lightning at new_midpot_total
        if r <= 0.2:
            branch_endpoint = (new_midpt_total[0] + L*norm_vector[0], new_midpt_total[1] + L*norm_vector[1])
            branch.append((new_midpt_total, branch_endpoint)) #the start is at the midpoint, thats where the branch starts
            #super_branch = branch_displacement(branch, per_x, per_y)
            #is_called = True

    return new_p, branch #if is_called else branch


run = True
while run:
    window.fill((0,0,0)) #so everything shows up
    
    pygame.draw.line(window, (255,255,255), (0, center[0]), (WIDTH, center[0])) #x-axis
    pygame.draw.line(window, (255,255,255), (center[0], 0), (center[0], HEIGHT))  #y-axis
    points = []
    branches = []

    #domain for sin
    for i in range(-600,601):
        x = i / SCALE #this is the domain, we want many domains, domain is [-i / SCALE, i / SCALE]
        y = math.sin(x)

        points.append((graph_to_screen(x,y)))
    
    
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
    jagged_pts, b1 = perpen_displacement(points, -12, 12)
    jagged_pts, b2 = perpen_displacement(jagged_pts, -6, 6)
    jagged_pts, b3 = perpen_displacement(jagged_pts, -3, 3)
    branches = b1 + b2 + b3     #adding them all up because **DON'T** OVERIDE, unlike jagged_pts



    # j = 0
    # new_p = []
    # #print(len(mid), len(points))
    # for i in range(len(points)-1):
    #     new_p.append(points[i])
    #     new_p.append(mid[i])
    #     new_p.append(points[i+1])
        
    WHITE = (255,255,255)

    CYAN = (0,255,255)

    BLUE = (0,100,255)

    DARK_BLUE = (0,30,120)

    PURPLE = (180,0,255)

    BLACK = (0,0,0)

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

