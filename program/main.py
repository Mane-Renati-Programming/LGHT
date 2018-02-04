#This is our main game file

#We import our main libraries which we need
import sys, ConfigParser
#We import the libraries needed by pygame
import pygame, pygame.locals

# We set our screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

class Tileset:
    def __init__(self, file, tile_width, tile_height):
        #The convert is an optimization step. It sets the pixel type, which makes it faster.
        image = pygame.image.load(file).convert()
        image_width, image_height = image.get_size()
        self.tile_table = []
        for tile_x in range(0, image_width/tile_width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/tile_height):
                rect = (tile_x * tile_width, tile_y * tile_height, tile_width, tile_height)
                line.append(image.subsurface(rect))


class Sprite:
    def __init__(self, file):
        #Placeholder for Now
        return None

#For the game we use a simple state machine
class Game:
    #Here is our constructor
    def __init__(self):
        # The default state can be the title menu
        self.state = 0


if __name__=='__main__':
    #Initalize the pygame library
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
