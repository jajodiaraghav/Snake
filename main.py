import pygame
import random
import os
from Snake import *
from Food import *
from Block import *
from World import *

from tkinter import *
import tkinter.simpledialog

head_path = os.path.join('Assets', 'Images', 'head.png')
index3_path = os.path.join('Assets', 'Images', 'index3.jpg')
python_path = os.path.join('Assets', 'Images', 'python.jpg')
point_path = os.path.join('Assets', 'Sounds', 'Point.wav')
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

width, height = 800, 600
game_display = pygame.display.set_mode((width, height))

pygame.display.set_caption('SNAKES')
img = pygame.image.load(head_path)
pygame.display.set_icon(img)
dirn = "right"
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)
FPS = 25


def total(score, i):
    # function for total score
    total = score + i * 10
    return total
#for highscore
highscorefile = open('highscore.txt','rt')
highscore = highscorefile.readline()
highscore = int(highscore)
namehighscore = highscorefile.readline()
highscorefile.close()

def pause(scorestr):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        message("Paused", (0, 0, 0))
        message("C to continue, Q to Quit", (200, 0, 0), 40)
        #display score on pause
        message(scorestr,(255,0,0),80)
        pygame.display.update()
        clock.tick(5)


def intro():
    i = True
    while i:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    i = False
        image = pygame.image.load(index3_path)
        game_display.blit(image, (0, 0))
        message("   Welcome to Snakes!!", (200, 0, 0), -59)
        message("Press C to continue", (100, 0, 100), 260)
        pygame.display.update()
        clock.tick(15)


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
        block_x = round(random.randrange(0, width) / 10.0) * 10
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
    global dirn
    global k
    global highscore
    global namehighscore
    pyExit = False
    pyOver = False

    score = 0
    world_num = 0
    scorestr = "Score:0"
    # Initialize the game
    snake = Snake(200, 200, img)
    food = Food(int(width / 2), int(height / 2))
    blocks = worlds(width, height, world_num)

    # Keeps track of the direction of the snake.
    dx, dy = 0, 0
    lossreason = ''

    while not pyExit:
        while pyOver:
            image = pygame.image.load(python_path)
            game_display.blit(image, (0, 0))
            
            message("Game Over! Press C to play Again, Q to Quit", (255, 0, 0), -20)
            message(lossreason, (255, 0, 0), 30)
            #display score on game over
            message("Your"+scorestr,(255,0,0),80)
            if tot > highscore:
                #message("Highscore!!!",(255,0,0),120)
                #write new highscore
                highscorefile = open('highscore.txt','wt')      
                highscorefile.write(str(tot)+"\n")
                
                #name window
                def namewrite():
                    highscorefile.write(v.get())
                    scorewindow.destroy()
                
                scorewindow = Tk()
                scorewindow.geometry('300x100')
                frame=Frame(scorewindow,width=100,height=100)
                frame.pack()
                scorewindow.title("congratulations")
                
                
                Label(frame, text='you\'ve made highscore!!!!').pack(side='top')
                v = StringVar()
                v.set("type your name")
                textbox = Entry(frame, textvariable = v)
                textbox.pack(side='top')
                
                okbutton=Button(frame,text="ok",fg="black",bg="white", command = namewrite)
                okbutton.pack(side='bottom') 

                
                
                scorewindow.mainloop()
                highscorefile.close()
                
                #incase useer wants to countinue after creating highscore
                #to read his new score
                highscorefile = open('highscore.txt','rt')
                highscore = highscorefile.readline()
                highscore = int(highscore)
                namehighscore = highscorefile.readline()
                highscorefile.close()

            else:
                message("Highscore by "+namehighscore+":"+str(highscore),(255,0,0),120)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pyExit = True
                        pyOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        """ Events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pyExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dirn != "right":
                    dirn = "left"
                    dx = -1
                    dy = 0
                if event.key == pygame.K_RIGHT and dirn != "left":
                    dirn = "right"
                    dx = 1
                    dy = 0
                if event.key == pygame.K_UP and dirn != "down":
                    dirn = "up"
                    dy = -1
                    dx = 0
                if event.key == pygame.K_DOWN != dirn != "up":
                    dirn = "down"
                    dy = 1
                    dx = 0
                if event.key == pygame.K_p:
                    pause(scorestr)

        # level changer value
        if score > 10:
            score = 0
            world_num += 1
            blocks = worlds(width, height, world_num)
            food.x, food.y = int(width / 2), int(height / 2)

        # Engage boost of pressing shift
        keyPresses = pygame.key.get_pressed()
        boost_speed = keyPresses[pygame.K_LSHIFT] or keyPresses[pygame.K_RSHIFT]

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
                pyOver = True
                lossreason = 'Oooops You Hit YOURSELF'
                sound = pygame.mixer.Sound(point_path)
                sound.play()

            """ Snake-Block collision """
            for block in blocks:
                block_rect = block.get_rect()
                if block_rect.colliderect(snake_rect):
                    pyOver = True
                    lossreason = 'Ooops You Hit a BLOCKER'
                    sound = pygame.mixer.Sound(point_path)
                    sound.play()

            """ Snake-Food collision """
            # if snake collides with food, increase its length.
            if food_rect.colliderect(snake_rect):
                score += 1
                snake.increment_length()

                sound = pygame.mixer.Sound(point_path)
                sound.play()

                # generate food at random x, y.
                food.generate_food(width, height)

                # try generating the food at a position where blocks are not present.
                while food_collides_block(food.get_rect(), blocks):
                    food.generate_food(width, height)

                

            """ Draw """
            game_display.fill((255, 255, 255))

            # draw the food and snake.
            snake.draw(game_display, dirn, (0, 155, 0))
            food.draw(game_display, (0, 255, 0))

        # draw the blocks.
        for block in blocks:
            block.draw(game_display, (255, 0, 0))
        #count and display score on screen
        totalscore = total(score,world_num)
        scorestr = 'Score: ' + str(totalscore)
        font = pygame.font.SysFont(None,30)
        text = font.render(scorestr, True,(0,0,255))
        game_display.blit(text,(0,0,20,20))      

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


intro()
gameLoop()
