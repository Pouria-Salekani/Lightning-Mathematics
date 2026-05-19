import pygame
import math

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
        

    pygame.draw.lines(window, (0,255,255), False, points, 2)







#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
pygame.quit()

