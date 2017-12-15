import pygame


class Block(object):
    """
        A Block object.
        Members:
        x, y: store the position of the block.
        width and height of the block.
    """

    def __init__(self, x, y, width, height):
        """ Initialize block with position and size """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, game_display, color):
        """ Draw the block on game_display with some color at x, y position """

        pygame.draw.rect(game_display, color, (self.x, self.y, self.width, self.height))

    def get_pos(self):
        """ Returns the position of the block as a tuple """

        return (self.x, self.y)

    def get_rect(self):
        """ Return rectangle object of the block for collision detection """

        return pygame.Rect(self.x, self.y, self.width, self.height)
