#We import our main libraries which we need
import sys, ConfigParser, datetime
#We import the libraries needed by pygame
import pygame, pygame.locals


# The height and width of every tile we have
TILE_HEIGHT = 32
TILE_WIDTH = 32

#Just an extension we can put on the pygame sprite class where we can do whatever the frick we want with
class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.x = 0
        self.y = 0
    def update(self, x, y):
        self.x = x
        self.y = y
        #We need to create the rectange of the sprite. I can't divide this up or else it'll take a performance hit, so I'll put the statements in a seprate document
        self.rect = pygame.Rect((self.x * TILE_WIDTH), (self.y * TILE_HEIGHT), self.width, self.height)
    def move(self, xofs, yofs):
        self.x += xofs
        self.y += yofs
        self.rect = pygame.Rect((self.x * TILE_WIDTH), (self.y * TILE_HEIGHT), self.width, self.height)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Tileset:
    def __init__(self, file, tile_width, tile_height):
        #The convert is an optimization step. It sets the pixel type, which makes it faster.
        image = pygame.image.load(file)
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
        Sprite.__init__(self, image)
        self.name = properties["name"]
        self.properties = properties
        self.tilex = 0
        self.tiley = 0
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
        parser.read("../assets/maps/" + mapname + ".map")
        self.tileset = Tileset(("../assets/tilesets/" + parser.get("level", "tileset")), TILE_WIDTH, TILE_HEIGHT)
        self.playerx = int(parser.get("player", "startx"))
        self.playery = int(parser.get("player", "starty"))
        tmpMap = parser.get("level", "map").split('\n')
        self.dimensions = (len(tmpMap[0]) * TILE_WIDTH, len(tmpMap) * TILE_HEIGHT)
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
            for mapx in list(mapy):
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
                self.map[mapy][mapx].update(self.curx + mapx, self.cury + mapy)

    def draw(self, surface):
        for mapy in self.map:
            for mapx in mapy:
                mapx.draw(surface)
    def getTile(self, x, y):
        return self.map[y][x]
    def collision(self, sprite):
        for mapy in self.map:
            for mapx in mapy:
                if pygame.sprite.collide_rect(sprite, mapx):
                    return mapx


#Check to make sure the game isn't being used as a module
if __name__=='__main__':
    #Initalize the pygame library
    pygame.init()
    pygame.display.init()
    if len(sys.argv) != 2:
        print "Pygame map baker"
        print "Syntax: python mapbaker.py <mapname>"
        sys.exit()
    mapfile = sys.argv[1]
    print "Baking " + mapfile + ".map"
    map = Map(mapfile)
    surface = pygame.Surface(map.dimensions)
    map.draw(surface)
    pygame.image.save(surface, "../assets/maps/" + mapfile + ".png")
