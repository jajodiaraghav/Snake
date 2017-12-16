import pygame


class Snake(object):
    """
        A Snake object.
        Members:
        x, y: store the position of the head.
        head_img: stores the pygame.img reference.
        length: size of the snake, 1 initially.
        body: stores the x, y coordinate of the previous frame.
    """

    def __init__(self, x, y, img):
        """ Initialize the snake! """

        self.x = x
        self.y = y
        self.length = 1
        self.size = 10
        self.body = [(x, y)]
        self.head_img = img

    def get_head(self):
        """ Returns a tuple containing the coordinate of the head """

        return (self.x, self.y)

    def get_length(self):
        """ Returns the length of the snake """

        return self.length

    def move(self, x, y, speed):
        """
            Moves the snake in x or y direction by some speed.
            x, y can be +1 or -1, depending on the direction.
            boost is boolean type, to apply boost.
        """

        dx = x * speed
        dy = y * speed

        self.x += dx
        self.y += dy

        self.body.append((self.x, self.y))

        # remove the first instance from the body of the snake.
        if len(self.body) > self.length:
            del self.body[0]

    def check_boundary(self, width, height):
        """ Head wraps around to 0 """

        self.x = self.x % (width-210)
        self.y = self.y % height

    def ate_itself(self):
        """ Returns true if the snake itself """

        head = (self.x, self.y)

        # for every part check if the head collides with the body.
        for part in self.body[:-1]:
            if head == part:
                return True

        return False

    def draw(self, game_display, direction, color):
        """ Draws the snake body onto the game_display """

        head = self.head_img

        if direction == "right":
            head = pygame.transform.rotate(self.head_img, 270)
        if direction == "left":
            head = pygame.transform.rotate(self.head_img, 90)
        if direction == "down":
            head = pygame.transform.rotate(self.head_img, 180)

        game_display.blit(head, (self.body[-1][0], self.body[-1][1]))

        for part in self.body[:-1]:
            pygame.draw.rect(game_display, color, (part[0], part[1], self.size, self.size))

    def increment_length(self):
        """ Increment length """

        self.length += 1

    def get_rect(self):
        """ Return rectangle object of the snake head for collision detection """

        return pygame.Rect(self.x, self.y, self.size, self.size)
