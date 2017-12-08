import pygame
import random
import os
from Snake import *
from worlds import *
from tkinter import *
import tkinter.simpledialog

head_path = os.path.join('Assets', 'Images', 'head.png')
index3_path = os.path.join('Assets', 'Images', 'index3.jpg')
python_path = os.path.join('Assets', 'Images', 'python.jpg')
point_path = os.path.join('Assets', 'Sounds', 'Point.wav')
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
game_display = pygame.display.set_mode((800, 600))

pygame.display.set_caption('SNAKES')
img = pygame.image.load(head_path)
pygame.display.set_icon(img)
dirn = "right"
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)
k = 25

# function for total score
def total(score,i):
    total = score + i * 5
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


def snake(snakeList):
    if dirn == "right":
        head = pygame.transform.rotate(img, 270)
    if dirn == "left":
        head = pygame.transform.rotate(img, 90)
    if dirn == "up":
        head = img
    if dirn == "down":
        head = pygame.transform.rotate(img, 180)
    game_display.blit(head, [snakeList[-1][0], snakeList[-1][1]])
    for val in snakeList[:-1]:
        pygame.draw.rect(game_display, (0, 155, 0), [val[0], val[1], 10, 10])





def gameLoop():
    global dirn
    global k
    global highscore
    global namehighscore
    
    pyExit = False
    pyOver = False

    snake = Snake(300, 300, img)
    dx, dy = 0, 0
    i = 0 #world number
    score = 0
    scorestr = "Score:0"
    foodX = round(random.randrange(0, 790) / 10.0) * 10.0
    foodY = round(random.randrange(20, 590) / 10.0) * 10.0
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
                
                butok=Button(frame,text="ok",fg="black",bg="white", command = namewrite)
                butok.pack(side='bottom') 

                
                
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
        if score == 10: # level changer value
            score = 0
            i += 1
            
        game_display.fill((255, 255, 255))
        pygame.draw.rect(game_display, (0, 255, 0), [foodX, foodY, 10, 10])
        keyPresses = pygame.key.get_pressed()
        boost_speed = keyPresses[pygame.K_LSHIFT] or keyPresses[pygame.K_RSHIFT]
        #if boost_speed is true it will move 2 blocks in one gameloop or else it will just move one block
        if boost_speed == 1:
            for loop in [1,2]:
                snake.move(dx, dy, 10)
                snake.check_boundary(800, 600)

                if snake.ate_itself():
                    pyOver = True
                    lossreason = 'Oooops You Hit YOURSELF'
                    sound = pygame.mixer.Sound(point_path)
                    sound.play()

                snake.draw(game_display, dirn, (0, 155, 0))
                blocks = worlds(i)
                for block in blocks:
                    pygame.draw.rect(game_display, (255, 0, 0), [block[0], block[1], 10, 10])

                    if block == snake.get_head():
                        pyOver = True
                        lossreason = 'Ooops You Hit a BLOCKER'
                        sound = pygame.mixer.Sound(point_path)
                        sound.play()

                if (foodX, foodY) == snake.get_head():
                    foodX = round(random.randrange(0, 790) / 10.0) * 10.0
                    foodY = round(random.randrange(20, 590) / 10.0) * 10.0
                    for block in blocks:
                        if block == (foodX, foodY):
                            foodX += 20
                            foodY += 20
                    snake.increment_length()
                    score += 1
                        

                    sound = pygame.mixer.Sound(point_path)
                    sound.play()
        else:
            snake.move(dx, dy, 10)
            snake.check_boundary(800, 600)

            if snake.ate_itself():
                pyOver = True
                lossreason = 'Oooops You Hit YOURSELF'
                sound = pygame.mixer.Sound(point_path)
                sound.play()

            snake.draw(game_display, dirn, (0, 155, 0))
            blocks = worlds(i)
            for block in blocks:
                pygame.draw.rect(game_display, (255, 0, 0), [block[0], block[1], 10, 10])

                if block == snake.get_head():
                    pyOver = True
                    lossreason = 'Ooops You Hit a BLOCKER'
                    sound = pygame.mixer.Sound(point_path)
                    sound.play()

            if (foodX, foodY) == snake.get_head():
                foodX = round(random.randrange(0, 790) / 10.0) * 10.0
                foodY = round(random.randrange(20, 590) / 10.0) * 10.0
                for block in blocks:
                    if block == (foodX, foodY):
                        foodX += 20
                        foodY += 20
                snake.increment_length()
                score += 1
                    

                sound = pygame.mixer.Sound(point_path)
                sound.play()

        #count and display score on screen
        tot = total(score,i)
        scorestr = 'Score:' + str(tot)
        font = pygame.font.SysFont(None,30)
        text = font.render(scorestr, True,(0,0,255))
        game_display.blit(text,(0,0,20,20))        




        
        

        pygame.display.update()
        clock.tick(k)

    pygame.quit()
    quit()



intro()
gameLoop()
