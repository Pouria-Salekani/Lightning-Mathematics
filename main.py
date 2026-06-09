import pygame
import colors
import modes
import config
import rendering_math as render

pygame.init()
window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('Lightning Mathematics!')

center = (config.WIDTH//2, config.HEIGHT//2)


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
                points, error = modes.user_input(text_box)

                if error is None:
                    user_input = text_box
                    text_box = ''
                    error_text = ''
                    state = 'draw'

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
        
        if keys[pygame.K_UP]: 
                thickness = min(config.MAX_THRESHOLD, thickness + 1)
        if keys[pygame.K_DOWN]:
            thickness = max(config.MIN_THRESHOLD, thickness - 1)
        
        layer1, layer2, layer3 = colors.COLORS[color_counter]
        
        pygame.draw.line(window, (255,255,255), (0, center[0]), (config.WIDTH, center[0])) #x-axis
        pygame.draw.line(window, (255,255,255), (center[0], 0), (center[0], config.HEIGHT))  #y-axis
        
        branches = []
        noise_ls = []

        
        jagged_pts, b1 = render.simplex_midpoint_disp(points, time,)
        jagged_pts, b2 = render.simplex_midpoint_disp(jagged_pts, time,)
        jagged_pts, b3 = render.simplex_midpoint_disp(jagged_pts, time)
        branches = b1 + b2 + b3     #adding them all up because **DON'T** OVERIDE, unlike jagged_pts


        #thicker/fuller colors first
        pygame.draw.lines(window, layer1, False, jagged_pts, 12 + thickness)
        pygame.draw.lines(window, layer2, False, jagged_pts, 6  + thickness)
        pygame.draw.lines(window, layer3, False, jagged_pts, 3 + thickness)


        #a loop for branches because they're all diff
        for x, y in branches: 
            pts = [x,y]     #branches is a 3D, so doing this, makes it 2D, like so: [(......), (......)]
            jagged_branch = render.branch_displacement(pts, -8, 8)
            jagged_branch = render.branch_displacement(jagged_branch, -3, 3)
         
            pygame.draw.lines(window, layer1, False, jagged_branch, 4)
            pygame.draw.lines(window, layer2, False, jagged_branch, 2)
            pygame.draw.lines(window, layer3, False, jagged_branch, 1)


    pygame.display.update()

    if save_image:
        pygame.image.save(window, f'cool_lightning{counter}.png')
        counter += 1
        save_image = False

    
    
pygame.quit()

