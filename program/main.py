#This is our main game file

#We import our main libraries which we need
import sys, const
#We import the libraries needed by pygame
import pygame, pygame.locals




#Now we start our game class

class Tileset:
    def __init__(self, file):
        #Placeholder for now
        return None

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
