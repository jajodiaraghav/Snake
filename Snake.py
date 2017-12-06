import pygame


class Snake:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.length = 1
        self.body = []
        self.head_img = img

    def get_head(self):
        return (self.x, self.y)

    def get_length(self):
        return self.length

    def move(self, x, y, speed, boost):
        boost_speed = 0
        if boost:
            boost_speed = 5

        dx = x * (speed + boost_speed)
        dy = y * (speed + boost_speed)

        self.x += dx
        self.y += dy

        self.body.append((self.x, self.y))

        if len(self.body) > self.length:
            del self.body[0]

    def check_boundary(self, width, height):
        self.x = self.x % width
        self.y = self.y % height

    def ate_itself(self):
        head = (self.x, self.y)

        for part in self.body[:-1]:
            if head == part:
                return True

        return False

    def draw(self, game_display, direction, color):
        head = self.head_img

        if direction == "right":
            head = pygame.transform.rotate(self.head_img, 270)
        if direction == "left":
            head = pygame.transform.rotate(self.head_img, 90)
        if direction == "down":
            head = pygame.transform.rotate(self.head_img, 180)

        game_display.blit(head, (self.body[-1][0], self.body[-1][1]))

        for part in self.body[:-1]:
            pygame.draw.rect(game_display, color, (part[0], part[1], 10, 10))

    def increment_length(self):
        self.length += 1
