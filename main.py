import pygame
import random
import os
from Snake import Snake
from Food import Food
from Block import Block
from World import worlds

from tkinter import *
import tkinter.simpledialog


width, height = None, None
game_display = None
sound = None
clock = None
buttons = list()
highscore = None
name_high_scorer = None
FPS = 25


def init():
    """ Initialize pygame and other global variables """

    global width, height, game_display, sound, clock, highscore

    # pygame boiler plate initialization
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    point_path = os.path.join('Assets', 'Sounds', 'Point.wav')
    sound = pygame.mixer.Sound(point_path)

    width, height = 1000, 600

    # set game icon and caption
    head_path = os.path.join('Assets', 'Images', 'head.png')  
    img = pygame.image.load(head_path)      
    pygame.display.set_icon(img)

    game_display = pygame.display.set_mode((width, height))
    game_display.fill((170, 150, 255))
    pygame.display.set_caption('SNAKES')

    clock = pygame.time.Clock()

    # sync high score
    get_high_score()


def get_high_score():
    """ Get high score from file """
    global highscore, name_high_scorer

    with open('highscore.txt', 'rt') as highscore_file:
        highscore = highscore_file.readline()

        # if no highscore is present, then its the first game.
        try:
            highscore = int(highscore)
        except ValueError:
            highscore = 0
            return

        name_high_scorer = highscore_file.readline()


def update_high_score(score, name):
    """ Update high score """

    global highscore, name_high_scorer
    highscore = score
    name_high_scorer = name

    with open('highscore.txt', 'wt') as highscore_file:
        highscore_file.write(str(score) + '\n')
        highscore_file.write(name + '\n')


def total(score, i):
    """ function for total score """
    return score + i * 10


def get_button_event():
    """ Returns the character corresponding to the button clicked """
    global buttons

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    for bttn in buttons:
        if bttn[0] + bttn[2] > mouse[0] > bttn[0] and bttn[1] + bttn[3] > mouse[1] > bttn[1]:
            if click[0] == 1:
                return bttn[4]
    return None


def pause(scorestr):
    """ Pause the screen. Show high score, name """

    paused = True
    while paused:
        show_buttons()
        
        # Check for 'quit' and 'continue' type events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keyp = get_button_event()
            # For keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            
            # For mouse
            if keyp != None:
                if keyp == 'c':
                    paused = False

                if keyp == 'q':
                    pygame.quit()
                    quit()

        # Render screen
        message("Paused", (0, 0, 0))
        message("C to continue, Q to Quit", (200, 0, 0), 40)
        message(scorestr, (255, 0, 0), 80)
        
        pygame.display.update()
        clock.tick(FPS)


def draw_button(string, x, y, w, h):
    """ 
        Draw a button at (x, y) position, with some width and height
    """

    mouse = pygame.mouse.get_pos()

    # Render button on screen.
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, (0, 0, 250), (x, y, w, h))
    else:
        pygame.draw.rect(game_display, (0, 0, 100), (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    text = smallText.render(string, True, (0, 200, 0))
    t = text.get_rect()
    t.center = ((x + (w / 2)), (y + (h / 2)))

    game_display.blit(text, t)


def intro():
    """ Display the welcome screen """

    while True:
        # Check for 'quit' or 'continue' type events.
        for event in pygame.event.get():
            keyp = get_button_event()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # For key board presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

            # For button presses
            if keyp != None:
                if keyp == 'c':
                    return
                    
                if keyp == 'q':
                    pygame.quit()
                    quit()

        # Render screen
        show_buttons()
        index3_path = os.path.join('Assets', 'Images', 'index3.jpg')
        image = pygame.image.load(index3_path)
        game_display.blit(image, (0, 0))

        message('\tWelcome to Snakes!!', (200, 0, 0), -59)
        message('Press C to continue', (100, 0, 100), 260)

        pygame.display.update()
        clock.tick(15)


def show_buttons():
    global buttons
    pygame.draw.rect(game_display, (170, 150, 255), (800, 0, 200, 600))
    
    draw_button("Continue", 800, 200, 130, 30)
    buttons.append((800, 200, 130, 30, 'c'))
    
    draw_button("Exit", 935, 200, 65, 30)
    buttons.append((935, 200, 65, 30, 'q'))
    
    draw_button("Up", 870, 235, 50, 30)
    buttons.append((870, 235, 50, 30, 'up'))
    
    draw_button("Down", 865, 305, 60, 30)
    buttons.append((865, 305, 60, 30, 'dn'))
    
    draw_button("Right", 895, 270, 60, 30)
    buttons.append((895, 270, 60, 30, 'rt'))
    
    draw_button("Left", 830, 270, 60, 30)
    buttons.append((830, 270, 60, 30, 'lt'))
    
    draw_button("Pause", 830, 340, 125, 30)
    buttons.append((830, 340, 125, 30, 'p'))

    draw_button("Shift", 830, 375, 125, 30)
    buttons.append((830, 375, 125, 30, 'st'))
    pygame.draw.line(game_display, (0, 200, 100), (800, 0), (800, 600), 5)


def message(string, color, dispy=0):
    """ Displays a message at the center of the screen """

    font = pygame.font.SysFont('comicsansms', 35)
    text = font.render(string, True, color)
    t = text.get_rect()
    t.center = (400, 300 + dispy)

    game_display.blit(text, t)


def food_collides_block(food_rect, blocks):
    """ Returns True if any of the blocks collide with the food """

    for block in blocks:
        if food_rect.colliderect(block.get_rect()):
            return True

    return False


def get_blocks(food_rect, n):
    """ Generates `n` blocks at random x, y """

    blocks = list()
    for i in range(n):
        block_x = round(random.randrange(0, (width)) / 10.0) * 10
        block_y = round(random.randrange(0, height) / 10.0) * 10

        block_width, block_height = 10, 10
        block = Block(block_x, block_y, block_width, block_height)

        # if the block collides with food, generate at other x, y.
        if food_rect.colliderect(block.get_rect()):
            i -= 1
            continue

        blocks.append(block)

    return blocks

def show_high_score_window(final_score):
    """ Shows the window to record the highscore """

    scorewindow = Tk()
    scorewindow.geometry('300x100')
    frame = Frame(scorewindow, width=100, height=100)
    frame.pack()
    
    scorewindow.title('Congratulations')
    Label(frame, text='You\'ve made a new highscore!').pack(side='top')
    v = StringVar()
    textbox = Entry(frame, textvariable=v)
    textbox.pack(side='top')

    def namewrite():
        update_high_score(final_score, v.get())            
        scorewindow.destroy()

    okbutton = Button(frame, 
                        text="ok", fg="black",
                        bg="white", command=namewrite)
    okbutton.pack(side='bottom')
    scorewindow.mainloop()


def game_over(loss_reason, final_score):
    """ Displays the game over screen, waiting for further action """

    global highscore, name_high_scorer

    python_path = os.path.join('Assets', 'Images', 'python.jpg')
    python_image = pygame.image.load(python_path)

    while True:
        game_display.blit(python_image, (0, 0))

        # Display all messages.
        message('Game Over! Press C to play Again, Q to Quit',
                (255, 0, 0), -20)
        message(loss_reason, (255, 0, 0), 30)
        scorestr = 'Your score {}'.format(final_score)
        message(scorestr, (255, 0, 0), 80)

        pygame.display.update()

        # if new score is higher then update the highscore.
        if final_score > highscore:
            show_high_score_window(final_score)
            final_score = 0
        else:
            message('Highscore by {} : {}'.format(name_high_scorer, highscore), (255, 0, 0), 120)

        for event in pygame.event.get():
            keyp = get_button_event()

            # For keyboard presses.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    gameLoop()

            # For button presses.
            if keyp != None:
                if keyp == 'q':
                    pygame.quit()
                    quit()

                if keyp == 'c':
                    gameLoop()



def gameLoop():
    """ Main loop """

    global dirn, k, highscore, name_high_scorer

    pyOver = False
    score = world_num = 0
    scorestr = 'Score : {}'

    # image of the head of the snake.
    head_path = os.path.join('Assets', 'Images', 'head.png')  
    img = pygame.image.load(head_path)      
    snake = Snake(200, 200, img)

    # generate food at the center of the screen
    food = Food(int(width / 2), int(height / 2))
    blocks = worlds(width - 200, height, world_num)

    # Keeps track of the direction of the snake.
    dx, dy = 0, 0
    dirn = "right"
    loss_reason = ''

    while True:
        if pyOver:
            game_over(loss_reason, score)
            pygame.quit()
            quit()
        
        # Check for movement keys / buttons being pressed, 'quit', 'pause'.
        for event in pygame.event.get():
            keyp = get_button_event()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dirn != "right":
                    dirn = "left"
                    dx = -1
                    dy = 0

                if  event.key == pygame.K_RIGHT and dirn != "left":
                    dirn = "right"
                    dx = 1
                    dy = 0

                if  event.key == pygame.K_UP and dirn != "down":
                    dirn = "up"
                    dy = -1
                    dx = 0

                if  event.key == pygame.K_DOWN and dirn != "up":
                    dirn = "down"
                    dy = 1
                    dx = 0

                if  event.key == pygame.K_p:
                    pause(scorestr.format(score))

                if  event.key == pygame.K_q:
                    pygame.quit()
                    quit(0)
            
            if keyp != None:
                if keyp == 'lt' and dirn != "right":
                    dirn = "left"
                    dx = -1
                    dy = 0

                if keyp == 'rt' and dirn != "left":
                    dirn = "right"
                    dx = 1
                    dy = 0

                if keyp == 'up' and dirn != "down":
                    dirn = "up"
                    dy = -1
                    dx = 0

                if keyp == 'dn' and dirn != "up":
                    dirn = "down"
                    dy = 1
                    dx = 0

                if keyp == 'p':
                    pause(scorestr.format(score))

                if keyp == 'q':
                    pygame.quit()
                    quit(0)

        # level changer value
        if score > 10 * (world_num + 1):
            world_num += 1
            blocks = worlds(width - 200, height, world_num)
            food.x, food.y = int(width / 2), int(height / 2)

        # Engage boost of pressing shift
        keyp = get_button_event()
        keyPresses = pygame.key.get_pressed()
        boost_speed = keyPresses[pygame.K_LSHIFT] or keyPresses[pygame.K_RSHIFT] or keyp == 'st'

        # if boost_speed is true it will move 2 blocks in one gameloop
        # else it will just move one block
        iterations = [1]
        if boost_speed:
            iterations.append(2)

        for i in iterations:
            # Update snake positon
            snake.move(dx, dy, 10)
            snake.check_boundary(width, height)

            snake_rect = snake.get_rect()
            food_rect = food.get_rect()

            # Detect Snake-Snake collision
            if snake.ate_itself():
                pyOver = True
                loss_reason = 'Oooops You Hit YOURSELF'
                sound.play()

            # Detect Snake-Block collision
            for block in blocks:
                block_rect = block.get_rect()
                if block_rect.colliderect(snake_rect):
                    pyOver = True
                    loss_reason = 'Ooops You Hit a BLOCKER'
                    sound.play()

           # Detect Snake-Food collision
            if food_rect.colliderect(snake_rect):
                score += 1
                snake.increment_length()
                sound.play()

                # generate food at random x, y.
                food.generate_food(width, height)

                # try generating the food at a position where blocks are not present.
                while food_collides_block(food.get_rect(), blocks):
                    food.generate_food(width - food.size, height - food.size)

            # Render screen
            game_display.fill((255, 255, 255))
            show_buttons()
            snake.draw(game_display, dirn, (0, 155, 0))
            food.draw(game_display, (0, 255, 0))

        # draw the blocks.
        for block in blocks:
            block.draw(game_display, (255, 0, 0))

        font = pygame.font.SysFont(None, 30)
        text = font.render(scorestr.format(score), True, (0, 0, 255))
        game_display.blit(text, (0, 0, 20, 20))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    init()
    intro()
    gameLoop()
