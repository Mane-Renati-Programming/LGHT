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

#This will also affect overall game speed, as the game's internal timer is based on how many frames have passed
MAX_FPS = 30

### GRAPHICS CLASSES

## SPRITE CLASSES
#We will be using this as a base class for us to extend on for Player, Enemy, and NPCs
class SpriteSheet(pygame.sprite.Group):
    def __init__(self, file):
        pygame.sprite.Group.__init__(self)
        image = pygame.image.load("assets/sprites/"+file).convert_alpha()
        image_width, image_height = image.get_size()
        self.x = 0
        self.y = 0
        #Iterates through the image, pulling out tiles at the width and height passed
        for tile_x in range(0, image_width/TILE_WIDTH):
            #And now we go through each tile's line and put each tile we get into the list
            for tile_y in range(0, image_height/TILE_HEIGHT):
                #We make a rectangle containing the tile
                rect = (tile_x * TILE_WIDTH, tile_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                #And we store that part of the image in the list
                self.add(Sprite(image.subsurface(rect)))
    def draw(self, surface, spriteno):
        surface.blit(self.sprites()[spriteno].image, self.sprites()[spriteno].rect)
    def move(self, xofs, yofs):
        self.x += xofs
        self.y += yofs
        self.update(self.x, self.y)

    def getSprite(self, spriteno):
        return self.sprites()[spriteno]


#Just an extension we can put on the pygame sprite class where we can do whatever the frick we want with
class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.width, self.height = self.image.get_size()
        self.rect = (0, 0, self.width, self.height)
        self.x = 0
        self.y = 0
    def update(self, x, y):
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, self.width+self.x, self.height+self.y)
    def move(self, xofs, yofs):
        self.x += xofs
        self.y += yofs
        self.rect = (self.x, self.y, self.width+self.x, self.height+self.y)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(SpriteSheet):
    def __init__(self, file):
        SpriteSheet.__init__(self, file)


## BACKGROUND CLASSES
class Tileset:
    def __init__(self, file, tile_width, tile_height):
        #The convert is an optimization step. It sets the pixel type, which makes it faster.
        image = pygame.image.load(file).convert_alpha()
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
    def getTile(self, x, y):
        return self.tile_table[x][y]

#We use this as a base for our map
class Tile(Sprite):
    def __init__(self, image, properties):
        super(Sprite, self)
        self.name = properties["name"]
        self.image = image
        self.width, self.height = self.image.get_size()
        self.rect = (0, 0, self.width, self.height)
        self.x = 0
        self.y = 0
        self.properties = properties
    def getProperty(self, prop):
        return self.properties[prop]

class Map:
    def __init__(self, mapname):
        #Set up basic coordinates
        #This coordinate corresponds to the top left of the whole map
        self.curx = 0
        self.cury = 0
        self.mapname = mapname
        #This will store a matrix of tiles
        self.map = []
        #This stores the map given in the config file
        tmpMap = []
        tmpKey = {}
        parser = ConfigParser.ConfigParser()
        parser.read("assets/maps/" + mapname + ".map")
        self.tileset = Tileset(("assets/tilesets/" + parser.get("level", "tileset")), TILE_WIDTH, TILE_HEIGHT)
        tmpMap = parser.get("level", "map").split('\n')
        self.dimensions = (len(tmpMap[0]), len(tmpMap))
        for section in parser.sections():
            #We check if the section is a tile descriptor (It will only have one character)
            if len(section) == 1:
                #We get each property and make it into a dictionary
                desc = dict(parser.items(section))
                #And we add this onto the key with the tile given as the index we use to look for it
                tmpKey[section] = desc
        #And now we parse the map into a matrix of tiles
        for mapy in tmpMap:
            line = []
            for mapx in mapy:
                curTileProp = tmpKey[mapx]
                line.append(Tile(self.tileset.getTile(int(curTileProp["tilex"]), int(curTileProp["tiley"])), curTileProp))
            self.map.append(line)

        #And now we update the map itself
        self.update()

    def move(self, xofs, yofs):
        self.curx += xofs
        self.cury += yofs
        self.update()

    def update(self):
        for mapy in xrange(0, len(self.map)):
            for mapx in xrange(0, len(self.map[0])):
                self.map[mapy][mapx].update(self.curx + (mapx*TILE_WIDTH), self.cury + (mapy*TILE_HEIGHT))

    def draw(self, surface):
        for mapy in self.map:
            for mapx in mapy:
                mapx.draw(surface)


### FUNCTIONALITY CLASSES

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

    def tick(self):
        #Overworld
        if self.state == 10:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exitGame()
                    if event.key == pygame.K_LEFT:
                        game.currentLevel.move(-10, 0)
                        player.move(-5,0)
                    if event.key == pygame.K_RIGHT:
                        game.currentLevel.move(10, 0)
                        player.move(5,0)
                    if event.key == pygame.K_UP:
                        game.currentLevel.move(0, -10)
                        player.move(0,-5)
                    if event.key == pygame.K_DOWN:
                        game.currentLevel.move(0, 10)
                        player.move(0,5)
            #We fill the background with black just to make surface
            screen.fill((0,0,0))
            #And we draw the game
            game.currentLevel.draw(screen)
            player.draw(screen, 0)
            #Every second, print the current fps
            if (counter % 30) == 0:
                print gameClock.get_fps()
            #Flip the buffer into the display
            pygame.display.flip()
            #Wait one frame
            gameClock.tick(MAX_FPS)


def exitGame():
    pygame.display.quit()
    sys.exit()


#Check to make sure the game isn't being used as a module
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


    player = Player("32x32-ex-idle.png")
    counter = 0


    #We create an infinite loop
    while 1:
        counter += 1
        #We check for any events that may have occured
        game.tick()

else:
    print "This game should not be used as a module"
    sys.exit()
