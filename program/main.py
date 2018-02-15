#This is our main game file

#We import our main libraries which we need
import sys, ConfigParser
#We import the libraries needed by pygame
import pygame, pygame.locals



# We set our screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
# The height and width of every tile we have
TILE_HEIGHT = 32
TILE_WIDTH = 32

class Tileset:
    def __init__(self, file, tile_width, tile_height):
        #The convert is an optimization step. It sets the pixel type, which makes it faster.
        image = pygame.image.load(file).convert()
        image_width, image_height = image.get_size()
        #We make a list where we will store all the graphics for each tile
        self.tile_table = []
        self.tile_width = tile_width
        self.tile_height = tile_height
        #Iterates through the image, pulling out tiles at the width and height passed
        for tile_x in range(0, image_width/tile_width):
            #We set a line so we can have the table as a grid
            line = []
            #We push that line to the list, adding one more row
            self.tile_table.append(line)
            #And now we go through each tile's line and put each tile we get into the list
            for tile_y in range(0, image_height/tile_height):
                #We make a rectangle containing the tile
                rect = (tile_x * tile_width, tile_y * tile_height, tile_width, tile_height)
                #And we store that part of the image in the list
                line.append(image.subsurface(rect))

#We will be using this as a base class for us to extend on for Player, Enemy, and NPCs
class Sprite(pygame.sprite.Sprite):
    def __init__(self, file):
        #Placeholder for Now
        super(Sprite, self).__init__()
        image = pygame.image.load("assets/sprites/"+file).convert()
        self.sprite_table = []
        image_width, image_height = image.get_size()
        #Iterates through the image, pulling out tiles at the width and height passed
        for tile_x in range(0, image_width/TILE_WIDTH):
            #We set a line so we can have the table as a grid
            line = []
            #We push that line to the list, adding one more row
            self.sprite_table.append(line)
            #And now we go through each tile's line and put each tile we get into the list
            for tile_y in range(0, image_height/TILE_HEIGHT):
                #We make a rectangle containing the tile
                rect = (tile_x * TILE_WIDTH, tile_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                #And we store that part of the image in the list
                line.append(image.subsurface(rect))


class Player(Sprite):
    def __init__(self, file):
        super(Sprite, self).__init__(file)

class Map:

    #We can load our map here
    def __init__(self, mapname):
        self.curx = 0
        self.cury = 0
        self.mapname = mapname
        #Will contain the map itself
        self.map = []
        #This is a dictionary (Accessable per characters instead of numbers) storing each tile type and its properties
        self.key = {}
        #We set up our parser to make sense of our config file
        parser = ConfigParser.ConfigParser()
        parser.read("assets/maps/" + mapname + ".map")
        #We set up our current tileset for this map as the tileset given in the config file
        self.tileset = Tileset(("assets/tilesets/" + parser.get("level", "tileset")), TILE_WIDTH, TILE_HEIGHT)
        #And we get the full map and split it by each line
        self.map = parser.get("level", "map").split('\n')
        #We set the width and height of the map
        self.width = len(self.map[0])
        self.height = len(self.map)
        #We go through each section which is a tile in our config file
        for section in parser.sections():
            #We check if the section is a tile descriptor (It will only have one character)
            if len(section) == 1:
                #We get each property and make it into a dictionary
                desc = dict(parser.items(section))
                #And we add this onto the key with the tile given as the index we use to look for it
                self.key[section] = desc


    def getTile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def drawTile(self, tilex, tiley, x, y, xofs, yofs):
        #TODO: Fix this
        screen.blit(self.tileset.tile_table[tilex][tiley], (self.tileset.tile_width*x+xofs, self.tileset.tile_width*y+yofs))

    def draw(self):
        screen.fill((0,0,0))
        for tile_y in xrange(0, len(self.map)):
            for tile_x in xrange(0, len(self.map[tile_y])):
                curTile = self.getTile(tile_x, tile_y)
                self.drawTile(int(curTile["tilex"]), int(curTile["tiley"]), tile_x, tile_y, self.curx, self.cury)


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




def exitGame():
    pygame.display.quit()
    sys.exit()


#I don't remember why we need this if statement, but I remember it was necessay. Just ignore it.
if __name__=='__main__':
    #Initalize the pygame library
    pygame.init()
    pygame.font.init()
    gameClock = pygame.time.Clock()
    #We initialize the screen with our resolution
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #Set the current state to the overworld
    game = Game()
    game.loadOverworldMap("testmap")
    #We set up a font to draw our FPS stuff in
    myFont = pygame.font.SysFont("Arial", 30)

    player = Sprite("32x32-ex-idle.png")


    #We create an infinite loop
    while 1:
        #We check for any events that may have occured
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.currentLevel.curx -= 10
                if event.key == pygame.K_RIGHT:
                    game.currentLevel.curx += 10
                if event.key == pygame.K_UP:
                    game.currentLevel.cury -= 10
                if event.key == pygame.K_DOWN:
                    game.currentLevel.cury += 10

        # And we draw the game
        game.currentLevel.draw()
        #blit sets an image on the screen with the texture given, in this case, our font
        screen.blit(myFont.render(str(gameClock.get_fps()), False, (255, 255, 255)), (0,0))
        # Flip the buffer into the display
        pygame.display.flip()
        # Wait one frame
        gameClock.tick(30)
