import random
import pygame

class Food(object):
    """
        A Food object.
        Members:
        x, y: store the position of the food.
        size: size of the food.
    """

    def __init__(self, x, y, size=10):
        """ Initialize block at given x, y position """

        self.x = x
        self.y = y
        self.size = size

    def generate_food(self, width, height):
        """ Generate food at random location within the width and height """

        self.x = round(random.randrange(0, width-210) / 10.0) * 10
        self.y = round(random.randrange(0, height) / 10.0) * 10

        return (self.x, self.y)

    def draw(self, game_display, color):
        """ Draws the food at x y position """

        pygame.draw.rect(game_display, color, (self.x, self.y, self.size, self.size))

    def get_pos(self):
        """ Returns the position of food as a tuple """

        return (self.x, self.y)

    def get_rect(self):
        """ Return rectangle object of the food for collision detection """

        return pygame.Rect(self.x, self.y, self.size, self.size)
