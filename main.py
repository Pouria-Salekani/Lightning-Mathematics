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

run = True
while run:
    window.fill((0,0,0)) #so everything shows up
    
    pygame.draw.line(window, (255,255,255), (0, center[0]), (WIDTH, center[0])) #x-axis
    pygame.draw.line(window, (255,255,255), (center[0], 0), (center[0], HEIGHT))  #y-axis
    points = []

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

    jagged_pts = jagg(points, -12, 12)
    jagged_pts = jagg(jagged_pts, -5, 5)
    jagged_pts = jagg(jagged_pts, -3, 3)


    # j = 0
    # new_p = []
    # #print(len(mid), len(points))
    # for i in range(len(points)-1):
    #     new_p.append(points[i])
    #     new_p.append(mid[i])
    #     new_p.append(points[i+1])
        


    pygame.draw.lines(window, (0,255,255), False, jagged_pts, 2)







#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
pygame.quit()

