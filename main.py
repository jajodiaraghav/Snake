import pygame
import random
import os
from Snake import *

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


def score(score):
    s = "PRESS P TO PAUSE"
    t = font.render("Score: " + str(score) + s.rjust(len(s) + 10, ' '), True, (0, 0, 0))
    game_display.blit(t, [0, 0])


def pause():
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


def get_blocks(foodX, foodY, n=0):
    # showing blocks
    block = []
    for i in range(20 + n):
        blockX = round(random.randrange(0, 790) / 10.0) * 10.0
        blockY = round(random.randrange(20, 590) / 10.0) * 10.0
        if abs(blockX - foodX) <= 20 or abs(blockY - foodY) <= 20:
            i -= 1
            continue

        block.append((blockX, blockY))
    return block


def gameLoop():
    global dirn
    global k
    pyExit = False
    pyOver = False

    snake = Snake(400, 600, img)
    dx, dy = 0, 0

    foodX = round(random.randrange(0, 790) / 10.0) * 10.0
    foodY = round(random.randrange(20, 590) / 10.0) * 10.0
    lossreason = ''
    blocks = get_blocks(foodX, foodY)
    while not pyExit:
        while pyOver:
            image = pygame.image.load(python_path)
            game_display.blit(image, (0, 0))
            message("Game Over! Press C to play Again, Q to Quit", (255, 0, 0), 30)
            message(lossreason, (255, 0, 0), 55)
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
                if event.key == pygame.K_LEFT:
                    dirn = "left"
                    dx = -1
                    dy = 0
                if event.key == pygame.K_RIGHT:
                    dirn = "right"
                    dx = 1
                    dy = 0
                if event.key == pygame.K_UP:
                    dirn = "up"
                    dy = -1
                    dx = 0
                if event.key == pygame.K_DOWN:
                    dirn = "down"
                    dy = 1
                    dx = 0
                if event.key == pygame.K_p:
                    pause()

        game_display.fill((255, 255, 255))
        pygame.draw.rect(game_display, (0, 255, 0), [foodX, foodY, 10, 10])

        keyPresses = pygame.key.get_pressed()
        boost_speed = keyPresses[pygame.K_LSHIFT] or keyPresses[pygame.K_RSHIFT]

        snake.move(dx, dy, 10, boost_speed)
        snake.check_boundary(800, 600)

        if snake.ate_itself():
            pyOver = True
            lossreason = 'Oooops You Hit YOURSELF'
            sound = pygame.mixer.Sound(point_path)
            sound.play()

        snake.draw(game_display, dirn, (0, 155, 0))

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

            snake.increment_length()

            get_blocks(foodX, foodY, snake.get_length())

            sound = pygame.mixer.Sound(point_path)
            sound.play()

        pygame.display.update()
        clock.tick(k)

    pygame.quit()
    quit()


intro()
gameLoop()
