import pygame
import random
import os
from Snake import Snake
from Food import Food
from Block import Block
from World import worlds

from tkinter import *
import tkinter.simpledialog

head_path = os.path.join('Assets','Images','head.png')
index3_path = os.path.join('Assets','Images','index3.jpg')
python_path = os.path.join( 'Assets','Images','python.jpg')
point_path = os.path.join('Assets','Sounds','Point.wav')
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
#intiating sounds
intro_sound = pygame.mixer.Sound(os.path.join('Assets','Sounds','intro.wav'))
game_sound = pygame.mixer.Sound(os.path.join('Assets','Sounds','gamesound.wav'))
pause_sound = pygame.mixer.Sound(os.path.join('Assets','Sounds','pausesound.wav'))
endgame_sound = pygame.mixer.Sound(os.path.join('Assets','Sounds','endsound.wav'))
#the volume are set such that sounds are pleasant
intro_sound.set_volume(0.1)
game_sound.set_volume(0.6)
pause_sound.set_volume(0.1)
endgame_sound.set_volume(0.12)

width, height = 1000, 600
game_display = pygame.display.set_mode((width, height))
game_display.fill((170,150,255))
blist=[]

pygame.display.set_caption('SNAKES')
img = pygame.image.load(head_path)
pygame.display.set_icon(img)
dirn = "right"
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)
FPS = 25


def total(score, i):
    """ function for total score """
    return score + i * 10


# for highscore
highscorefile = open('highscore.txt', 'rt')
highscore = highscorefile.readline()
try:
    highscore = int(highscore)
except ValueError:
    highscore = 0
namehighscore = highscorefile.readline()
highscorefile.close()


def pause(scorestr):
    #stop in game music and play pause music
    game_sound.stop()
    pause_sound.play(-1) 
    paused = True
    while paused:    
        showButton()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keyp = action()
            if event.type == pygame.KEYDOWN or keyp != None:
                try:
                    if keyp == 'c' or event.key == pygame.K_c:
                        paused = False
                except:
                    pass
                try:
                    if keyp == 'q' or event.key == pygame.K_q:
                        print('quit')
                        pygame.quit()
                        quit()
                except:
                    pass
                    
        message("Paused", (0, 0, 0))
        message("C to continue, Q to Quit", (200, 0, 0), 40)
        # display score on pause
        message(scorestr, (255, 0, 0), 80)
        pygame.display.update()
        clock.tick(5)
    #stop pause music and play in game music if game continues
    if paused == False:
        pause_sound.stop()
        game_sound.play(-1)

def button(msg,x,y,w,h):
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, (0,0,250),(x,y,w,h))
    else:
        pygame.draw.rect(game_display, (0,0,100),(x,y,w,h))
    smallText = pygame.font.Font("freesansbold.ttf",20)
    text= smallText.render(msg, True, (0,200,0))
    t=text.get_rect()
    t.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(text, t)

def intro():
    #play intro music infinite loop
    intro_sound.play(-1)
    i=True
    while i:
        for event in pygame.event.get():
            keyp=action()
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if keyp!=None or event.type==pygame.KEYDOWN :
                try:
                    if keyp=='c' or event.key==pygame.K_c :
                        i=False
                except:
                    continue
        showButton()
        image = pygame.image.load(index3_path)
        game_display.blit(image,(0,0))
        message("   Welcome to Snakes!!",(200,0,0),-59)
        message("Press C to continue",(100,0,100),260)
        pygame.display.update()
        clock.tick(15)

def showButton():
    global blist
    pygame.draw.rect(game_display, (170, 150, 255), (800, 0, 200, 600))
    button("Continue", 800, 200, 130, 30)
    blist.append((800, 200, 130, 30,'c'))
    button("Exit", 935, 200, 65, 30)
    blist.append((935, 200, 65, 30,'q'))
    button("Up", 870, 235, 50, 30)
    blist.append((870, 235, 50, 30,'up'))
    button("Down", 865, 305, 60, 30)
    blist.append((865, 305, 60, 30,'dn'))
    button("Right", 895, 270, 60, 30)
    blist.append((895, 270, 60, 30,'rt'))
    button("Left", 830, 270, 60, 30)
    blist.append((830, 270, 60, 30,'lt'))
    button("Pause",830,340,125,30)
    blist.append((830,340,125,30,'p'))
    button("Shift", 830, 375, 125, 30)
    blist.append((830, 375, 125, 30,'st'))
    pygame.draw.line(game_display,(0,200,100),(800,0),(800,600),5)

def action():
    global blist
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for tup in blist:
        if tup[0] + tup[2] > mouse[0] > tup[0] and tup[1] + tup[3] > mouse[1] > tup[1]:
            if click[0] == 1:
                return tup[4]
    return None

def message(m, color, dispy=0):
    text = font.render(m, True, color)
    t = text.get_rect()
    t.center = (400), (300) + dispy
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


def gameLoop():
    global dirn, k, highscore, namehighscore
    pyExit = False
    pyOver = False
    #stop intro music and play in game music infinite loop
    intro_sound.stop()
    game_sound.play(-1)
    score = 0
    world_num = 0
    scorestr = "Score:0"
    # Initialize the game
    snake = Snake(200, 200, img)
    food = Food(int(width / 2), int(height / 2))
    blocks = worlds(width - 200, height, world_num)

    # Keeps track of the direction of the snake.
    dx, dy = 0, 0
    lossreason = ''

    while not pyExit:
        if pyOver == True:
            #play end music
            endgame_sound.play(-1)
        while pyOver:
            image = pygame.image.load(python_path)
            game_display.blit(image, (0, 0))

            message("Game Over! Press C to play Again, Q to Quit",
                    (255, 0, 0), -20)
            message(lossreason, (255, 0, 0), 30)
            # display score on game over
            message("Your" + scorestr, (255, 0, 0), 80)
            if totalscore > highscore:
                # message("Highscore!!!",(255,0,0),120)
                # write new highscore
                highscorefile = open('highscore.txt', 'wt')
                highscorefile.write(str(totalscore) + "\n")

                # name window
                def namewrite():
                    highscorefile.write(v.get())
                    scorewindow.destroy()

                scorewindow = Tk()
                scorewindow.geometry('300x100')
                frame = Frame(scorewindow, width=100, height=100)
                frame.pack()
                scorewindow.title("congratulations")

                Label(frame, text='you\'ve made highscore!!!!').pack(side='top')
                v = StringVar()
                v.set("type your name")
                textbox = Entry(frame, textvariable=v)
                textbox.pack(side='top')

                okbutton = Button(frame, text="ok", fg="black",
                                  bg="white", command=namewrite)
                okbutton.pack(side='bottom')

                scorewindow.mainloop()
                highscorefile.close()

                # incase user wants to countinue after creating highscore
                # to read his new score
                highscorefile = open('highscore.txt', 'rt')
                highscore = highscorefile.readline()
                highscore = int(highscore)
                namehighscore = highscorefile.readline()
                highscorefile.close()

            else:
                message("Highscore by " + namehighscore +
                        ":" + str(highscore), (255, 0, 0), 120)
            pygame.display.update()

            for event in pygame.event.get():
                keyp = action()
                if keyp != None or event.type == pygame.KEYDOWN:
                    try:
                        if keyp == 'q' or event.key == pygame.K_q:
                            pyExit = True
                            pyOver = False
                    except:
                        blank = []  # bypass the exception
                    try:
                        if keyp == 'c' or event.key == pygame.K_c:
                            #stop endgame music
                            endgame_sound.stop()
                            gameLoop()
                    except:
                        blank = []  # bypass the exception
                        
        """ Events """
        #the conditions are modified to work with the buttons
        for event in pygame.event.get():
            keyp = action()
            # blank is not used anywhere
            # it is just used to jump the exception
            if event.type == pygame.QUIT:
                pyExit = True
            if event.type == pygame.KEYDOWN or keyp != None:
                try:
                    if keyp == 'lt' or event.key == pygame.K_LEFT and dirn != "right":
                        dirn = "left"
                        dx = -1
                        dy = 0
                except:
                    blank = []
                try:
                    if keyp == 'rt' or event.key == pygame.K_RIGHT and dirn != "left":
                        dirn = "right"
                        dx = 1
                        dy = 0
                except:
                    blank = []
                try:
                    if keyp == 'up' or event.key == pygame.K_UP and dirn != "down":
                        dirn = "up"
                        dy = -1
                        dx = 0
                except:
                    blank = []
                try:
                    if keyp == 'dn' or event.key == pygame.K_DOWN and dirn != "up":
                        dirn = "down"
                        dy = 1
                        dx = 0
                except:
                    blank = []
                try:
                    if keyp == 'p' or event.key == pygame.K_p:
                        pause(scorestr)
                except:
                    blank = []
                try:
                    if keyp == 'q' or event.key == pygame.K_q:
                        pygame.quit()
                        quit(0)
                except:
                    blank = []

        # level changer value
        if score > 10:
            score = 0
            world_num += 1
            blocks = worlds(width - 200, height, world_num)
            food.x, food.y = int(width / 2), int(height / 2)

        # Engage boost of pressing shift
        keyp=action()
        keyPresses = pygame.key.get_pressed()
        boost_speed = keyPresses[pygame.K_LSHIFT] or keyPresses[pygame.K_RSHIFT] or keyp=='st'

        # if boost_speed is true it will move 2 blocks in one gameloop
        # else it will just move one block
        iterations = [1]
        if boost_speed == 1:
            iterations.append(2)

        for i in iterations:
            """ Update snake """
            snake.move(dx, dy, 10)
            snake.check_boundary(width, height)

            snake_rect = snake.get_rect()
            food_rect = food.get_rect()

            """ Snake-Snake collision """
            if snake.ate_itself():
                #stop game sound
                game_sound.stop()
                pyOver = True
                lossreason = 'Oooops You Hit YOURSELF'
                

            """ Snake-Block collision """
            for block in blocks:
                block_rect = block.get_rect()
                if block_rect.colliderect(snake_rect):
                    #stop game sound
                    game_sound.stop()
                    pyOver = True
                    lossreason = 'Ooops You Hit a BLOCKER'
                    
            """ Snake-Food collision """
            # if snake collides with food, increase its length.
            if food_rect.colliderect(snake_rect):
                score += 1
                snake.increment_length()

                sound = pygame.mixer.Sound(point_path)
                sound.set_volume(0.3)
                sound.play()

                # generate food at random x, y.
                food.generate_food(width, height)

                # try generating the food at a position where blocks are not present.
                while food_collides_block(food.get_rect(), blocks):
                    food.generate_food(width - food.size, height - food.size)

            """ Draw """
            game_display.fill((255, 255, 255))
            showButton()

            # draw the food and snake.
            snake.draw(game_display, dirn, (0, 155, 0))
            food.draw(game_display, (0, 255, 0))

        # draw the blocks.
        for block in blocks:
            block.draw(game_display, (255, 0, 0))
        # count and display score on screen
        totalscore = total(score, world_num)
        scorestr = 'Score: ' + str(totalscore)
        font = pygame.font.SysFont(None, 30)
        text = font.render(scorestr, True, (0, 0, 255))
        game_display.blit(text, (0, 0, 20, 20))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


intro()
gameLoop()
