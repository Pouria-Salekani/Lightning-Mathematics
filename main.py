import pygame
import colors
import modes
import config
import rendering_math as render
import encyclopedia

pygame.init()
window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('Lightning Mathematics!')

center = (config.WIDTH, config.HEIGHT)


run = True
time = 0
state = 'user'

text_box = ''
user_input = None
error_text = ''

save_image = False

counter = 1
color_counter = 0
thickness = 0

points = None

jagged_pts = None
lightning_frame = 0
branches = []


while run:
    window.fill((0,0,0))
    keys = pygame.key.get_pressed()

    #this listens for key inputs, nothing else should be here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if state == 'user' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: #delete by 1
                text_box = text_box[:-1]
            elif event.key == pygame.K_RETURN:
                print(text_box)
                points, error, INFO = modes.user_input(text_box)
                
                if error is None:
                    user_input = text_box
                    #encyclopedia.func_info(exprs_info) from modes--->enclcy
                    text_box = ''
                    error_text = ''
                    state = 'draw'

                    jagged_pts = None
                    branches = []
                    lightning_frame = 0

                else:
                    text_box = ''
                    error_text = error
            elif event.key == pygame.K_SLASH and (event.mod & pygame.KMOD_SHIFT):
                text_box = ''
                state = 'instructions'
            elif event.key == pygame.K_COMMA and (event.mod & pygame.KMOD_SHIFT):
                text_box += 'exp(sin(theta)) - 2*cos(4*theta) + sin((2*theta-pi)/24)**5'
            else:   #writing
                text_box += event.unicode

        elif state == 'draw' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                color_counter = 0
                state = 'user'
            elif event.key == pygame.K_s and (event.mod & pygame.KMOD_SHIFT):
                save_image = True
            elif event.key == pygame.K_z:
                color_counter = (color_counter+1) % len(colors.COLORS)  #loops back
            elif event.key == pygame.K_4 and (event.mod & pygame.KMOD_SHIFT):
                state = 'encyclopedia'
                #go to encyclopedia page
            


    
    if state == 'user':
            font = pygame.font.SysFont(None, 50)
            introduction_text = font.render('Enter equation:', True, (255,255,255))
            window.blit(introduction_text, (50,50))

            text_surface = font.render(text_box, True, (255,255,255))
            window.blit(text_surface, (50,100))

            text = ['To view instructions, press "?"',
                    'To change the colors, press "Z"',
                    'To make lines thicker, press UP ARROW. To make them thinner, DOWN ARROW', 
                    'To take a screenshot, press "SHIFT + S" when the graph appears',
                    'Press "<" then ENTER for a cool graph!']
            screenshot_font = pygame.font.SysFont(None, 33)
            y = 550
            for i in text:
                surface = screenshot_font.render(i, True, colors.WHITE)
                window.blit(surface, (50, y))
                y += 40
           

            if error_text != '':
                font = pygame.font.SysFont(None, 30)
                instruction = font.render(error_text, True, (255,250,250))
                window.blit(instruction, (((config.WIDTH - instruction.get_width()) // 2), 250)) #center below textbox


    elif state == 'encyclopedia':
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            state = 'draw'
        font = pygame.font.SysFont(None, 35)
       
        y = 300
        for key, value in INFO.items():
            if key == 'Input' and len(value) == 2:
                value = ', '.join(value)
            surface = font.render(f'{key}: {value}', True, colors.WHITE)
            window.blit(surface, (((config.WIDTH - surface.get_width()) // 2), y))
            y += 60


    elif state == 'instructions':
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            error_text = ''
            state = 'user'
        font = pygame.font.SysFont(None, 40)
        text = ['Example functions below are supported (these are just examples, more are supported): ',
                'Single: sin(x), cos(x), x**2, x**3, exp(x), x**2 + sin(2x), etc...',
                'Polar: sin(3*theta) + cos(2*theta), cos(-theta), 0.2*theta, etc...',
                'Parametric (two expressions WITH comma included): cos(t), sin(t); t+2, t**2; etc...',
                '\n',
                '\n',
                '\n',
                'The parametric REQUIRES a comma to separate two expressions.',
                'Press ESC to go back.'
                ]

        y = 50
        for i in text:
            surface = font.render(i, True, colors.WHITE)
            window.blit(surface, (30, y))
            y += 40


    elif state == 'draw':
        time += 0.09
        lightning_frame += 1
        
        if keys[pygame.K_UP]: 
            thickness = min(config.MAX_THRESHOLD, thickness + 1)
        if keys[pygame.K_DOWN]:
            thickness = max(config.MIN_THRESHOLD, thickness - 1)
        
        layer1, layer2, layer3 = colors.COLORS[color_counter]
        
        pygame.draw.line(window, (255,255,255), (0, config.center[1]), (config.WIDTH, config.center[1])) #x-axis
        pygame.draw.line(window, (255,255,255), (config.center[0], 0), (config.center[0], config.HEIGHT))  #y-axis
    
        #encyclopedia page
        e_font = pygame.font.SysFont(None, 33)
        instruction = e_font.render('Press "$" for information about the expression', 
                                  True, (255,250,250))
        window.blit(instruction, (20,10))

        
        if not jagged_pts or lightning_frame >= config.L_REFRESH_RATE:
            jagged_pts, b1 = render.simplex_midpoint_disp(points, time)
            jagged_pts, b2 = render.simplex_midpoint_disp(jagged_pts, time)
            jagged_pts, b3 = render.simplex_midpoint_disp(jagged_pts, time)
            branches = b1 + b2 + b3     #adding them all up because **DON'T** OVERIDE, unlike jagged_pts
            

            multi_jagged_branches = []
            for x, y in branches: 
                pts = [x,y]     #branches is a 3D, so doing this, makes it 2D, like so: [(......), (......)]
                jagged_branch = render.branch_displacement(pts, -8, 8)
                jagged_branch = render.branch_displacement(jagged_branch, -3, 3)
                multi_jagged_branches.append(jagged_branch)

            lightning_frame = 0 # this is crucial, otherwise, the frames will be laggy


        #thicker/fuller colors first
        pygame.draw.lines(window, layer1, False, jagged_pts, 12 + thickness)
        pygame.draw.lines(window, layer2, False, jagged_pts, 6 + thickness)
        pygame.draw.lines(window, layer3, False, jagged_pts, 3 + thickness)


        #a loop for branches because they're all diff
        # for x, y in branches: 
        #     pts = [x,y]     #branches is a 3D, so doing this, makes it 2D, like so: [(......), (......)]
        #     jagged_branch = render.branch_displacement(pts, -8, 8)
        #     jagged_branch = render.branch_displacement(jagged_branch, -3, 3)
        
        for j in multi_jagged_branches:
            pygame.draw.lines(window, layer1, False, j, 4)
            pygame.draw.lines(window, layer2, False, j, 2)
            pygame.draw.lines(window, layer3, False, j, 1)


    pygame.display.update()

    if save_image:
        pygame.image.save(window, f'cool_lightning{counter}.png')
        counter += 1
        save_image = False

    
    
pygame.quit()

