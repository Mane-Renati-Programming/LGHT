#This is our main game file

#We import our main libraries which we need
import sys, ConfigParser
#We import the libraries needed by pygame
import pygame, pygame.locals

# We set our screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN_DEFAULT_COLOR = (255,255,255)

class Tileset:
    def __init__(self, file, tile_width, tile_height):
        #The convert is an optimization step. It sets the pixel type, which makes it faster.
        image = pygame.image.load(file).convert()
        image_width, image_height = image.get_size()
        self.tile_table = []
        #Iterates through the image, pulling out tiles at the width and height passed
        for tile_x in range(0, image_width/tile_width):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height/tile_height):
                rect = (tile_x * tile_width, tile_y * tile_height, tile_width, tile_height)
                line.append(image.subsurface(rect))

#We will be using this as a base class for us to extend on for Player, Enemy, and NPCs
class Sprite(pygame.sprite.Sprite):
    def __init__(self, file):
        #Placeholder for Now
        super(Sprites)
        return None


class Player(Sprite):
    def __init__(self, file):
        super(Sprite, self).__init__(file)


class Map:

    #We can load our map here
    def __init__(self, mapname):
        self.mapname = mapname
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read("assets/maps/" + mapname + ".map")
        self.tileset = Tileset(("assets/tilesets/" + parser.get("level", "tileset")), int(parser.get("level", "tilewidth")), int(parser.get("level", "tileheight")))
        self.map = parser.get("level", "map").split('\n')
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def getTile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

#For the game we use a simple state machine
class Game:
    #Here is our constructor
    def __init__(self):
        # The default state can be the title menu
        self.state = 0
        self.currentLevel = None

    def loadOverworldMap(self, mapname):
        #We set the state to overworld
        self.state = 10
        self.currentLevel = Map(mapname)




if __name__=='__main__':
    #Initalize the pygame library
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #Set the current state to the overworld
    game = Game()
    game.loadOverworldMap("testmap")

    #We create an infinite loop
    while 1:
        #We check for any events that may have occured
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                SCREEN_DEFAULT_COLOR = (255,0,0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    SCREEN_DEFAULT_COLOR = (255,255,255)
        screen.fill(SCREEN_DEFAULT_COLOR)
        pygame.display.flip()
        pygame.time.wait(1)
