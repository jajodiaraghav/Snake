
import pygame
import random

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('SNAKES')
img=pygame.image.load('head.png')
pygame.display.set_icon(img)
dirn="right"

clock = pygame.time.Clock()
font= pygame.font.SysFont("comicsansms", 35)

def score(score):
	t=font.render("Score: "+str(score), True, (0,0,0))
	gameDisplay.blit(t,[0,0])

def pause():
        paused=True
        while paused:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_c:
                                paused=False
                        if event.key==pygame.K_q:
                                pygame.quit()
                                quit()
                message("Paused",(0,0,0))
                message("C to continue, Q to Quit",(200,0,0),40)
                pygame.display.update()
                clock.tick(5)

def intro():
    i=True
    while i:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    i=False
        image = pygame.image.load('index3.jpg')        
        gameDisplay.blit(image,(0,0))
        message("   Welcome to Snakes!!",(200,0,0),-59)
        message("Press C to continue",(100,0,100),260)
        pygame.display.update()
        clock.tick(15)

def message(m,color,dispy=0):
    text= font.render(m, True, color)
    t=text.get_rect()
    t.center=(400),(300)+dispy
    gameDisplay.blit(text, t)
    
def snake(snakeList):
    if dirn=="right":
        head=pygame.transform.rotate(img,270)
    if dirn=="left":
        head=pygame.transform.rotate(img,90)
    if dirn=="up":
        head=img
    if dirn=="down":
        head=pygame.transform.rotate(img,180)
    gameDisplay.blit(head, [snakeList[-1][0],snakeList[-1][1]])
    for val in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, (0,155,0), [val[0],val[1],10,10])
def gameLoop():
    global dirn
    pyExit=False
    pyOver=False
    x=400
    y=300
    x_change=0
    y_change=0
    snakeList=[]
    snakeLen=1
    foodX=round(random.randrange(0,790)/10.0)*10.0
    foodY=round(random.randrange(0,590)/10.0)*10.0
    while not pyExit:
        while pyOver:
            image = pygame.image.load('python.jpg')        
            gameDisplay.blit(image,(0,0))
            message("Game Over! Press C to play Again, Q to Quit",(255,0,0),30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        pyExit=True
                        pyOver=False
                    if event.key==pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pyExit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    dirn="left"
                    x_change=-10
                    y_change=0
                if event.key==pygame.K_RIGHT:
                    dirn="right"
                    x_change=10
                    y_change=0
                if event.key==pygame.K_UP:
                    dirn="up"
                    y_change=-10
                    x_change=0
                if event.key==pygame.K_DOWN:
                    dirn="down"
                    y_change=10
                    x_change=0
                if event.key==pygame.K_p:
                    pause()

        if x>=800:
            x=10
        if y>=600:
            y=10
        if x<=0:
            x=800
        if y<=0:
            y=600

        x+=x_change
        y+=y_change
        gameDisplay.fill((255,255,255))
        pygame.draw.rect(gameDisplay, (0,255,0), [foodX,foodY,10,10])
        
        snakeHead=[]
        snakeHead.append(x)
        snakeHead.append(y)
        snakeList.append(snakeHead)
        if len(snakeList)>snakeLen:
            del snakeList[0]
        for body in snakeList[:-1]:
            if body==snakeHead:
                pyOver=True

        snake(snakeList)
        score(snakeLen-1)
        pygame.display.update()
        clock.tick(25)

        if foodX==x and foodY==y:
                foodX=round(random.randrange(0,790)/10.0)*10.0
                foodY=round(random.randrange(0,590)/10.0)*10.0
                snakeLen+=1

    pygame.quit()
    quit()

intro()
gameLoop()
