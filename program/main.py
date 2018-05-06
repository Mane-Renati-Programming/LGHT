#This is our main game file


#We import our main libraries which we need
import sys, ConfigParser, datetime, ast, threading

#We import the libraries needed by pygame
import pygame, pygame.locals

GAME_NAME = "LGHT"

# We set our screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
# The height and width of every tile we have
TILE_HEIGHT = 32
TILE_WIDTH = 32

#This will also affect overall game speed, as the game's internal timer is based on how many frames have passed
MAX_FPS = 30

#Sets if debugging is enabled
DEBUG = 2
if DEBUG != False:
    LogFile = None

isRunning = True

ScreenLocation = [0 , 0] #This is the offset of the screen of itself.

counter = 0

### GRAPHICS CLASSES

## SPRITE CLASSES
#We will be using this as a base class for us to extend on for Player, Enemy, and NPCs

#All coordinates given that have to do with sprites will be done in coordinaes of where they are on the map.
class SpriteSheet(pygame.sprite.Group):
    def __init__(self, file, needsUpdate):
        pygame.sprite.Group.__init__(self)
        image = pygame.image.load("assets/sprites/"+file+".png").convert_alpha()
        image_width, image_height = image.get_size()
        self.x = 0
        self.y = 0
        aniFile = open("assets/sprites/animation/"+file+".ani")
        self.animation = ast.literal_eval(aniFile.read())
        self.currentAnimation = 0
        self.animationIndex = 0
        #Iterates through the image, pulling out tiles at the width and height passed
        for tile_x in range(0, image_width/TILE_WIDTH):
            #And now we go through each tile's line and put each tile we get into the list
            for tile_y in range(0, image_height/TILE_HEIGHT):
                #We make a rectangle containing the tile
                rect = pygame.Rect(tile_x * TILE_WIDTH, tile_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                #And we store that part of the image in the list
                self.add(Sprite(image.subsurface(rect), needsUpdate))
    def draw(self, surface, spriteno):
        surface.blit(self.sprites()[spriteno].image, self.sprites()[spriteno].rect)
    def setAnimation(self, animationNo):
        self.currentAnimation = animationNo
        self.animationIndex = 0
    def animationUpdate(self, surface):
        self.animationIndex += 1
        if self.animationIndex >= len(self.animation[self.currentAnimation]):
            self.animationIndex = 0
        self.draw(surface,self.animation[self.currentAnimation][self.animationIndex])
    def move(self, xofs, yofs):
        self.x += xofs
        self.y += yofs
        self.update(self.x, self.y)
    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.update(self.x, self.y)
    def getSprite(self, spriteno):
        return self.sprites()[spriteno]

#Just an extension we can put on the pygame sprite class where we can do whatever the frick we want with
class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image, needsUpdate):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.x = 0
        self.y = 0
        self.needsUpdate = needsUpdate
        if needsUpdate:
            self.screenUpdate = game.addHandler(4, self.draw)
    def update(self, x, y):
        self.x = x
        self.y = y
        #We need to create the rectange of the sprite. I can't divide this up or else it'll take a performance hit, so I'll put the statements in a seprate document
        self.rect = pygame.Rect((self.x * TILE_WIDTH) - ScreenLocation[0], (self.y * TILE_HEIGHT) - ScreenLocation[1], self.width, self.height)
    def move(self, xofs, yofs):
        self.x += xofs
        self.y += yofs
        self.rect = pygame.Rect((self.x * TILE_WIDTH) - ScreenLocation[0], (self.y * TILE_HEIGHT) - ScreenLocation[1], self.width, self.height)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(SpriteSheet):
    def __init__(self, file):
        #This sprite needs to be updated every time the map is redrawn
        SpriteSheet.__init__(self, file, True)
        self.update(self.x,self.y)
        #We can put all the stats in here
    def move(self, xofs, yofs):
        self.x += xofs
        self.y += yofs
        if (self.x * TILE_WIDTH - ScreenLocation[0] > SCREEN_WIDTH * 0.75):
            game.screenMove(TILE_WIDTH,0)
        if (self.y * TILE_HEIGHT - ScreenLocation[1] > SCREEN_HEIGHT * 0.75):
            game.screenMove(0,TILE_HEIGHT)
        if (self.x * TILE_WIDTH - ScreenLocation[0] < SCREEN_WIDTH * 0.25):
            game.screenMove(-TILE_WIDTH,0)
        if (self.y * TILE_HEIGHT - ScreenLocation[1] < SCREEN_HEIGHT * 0.25):
            game.screenMove(0,-TILE_HEIGHT)
        self.update(self.x, self.y)
    def update(self, x, y):
        self.x = x
        self.y = y
        SpriteSheet.update(self, x, y)
    #Returns true if the player will colide if it moves to that spot
    def willCollideMap(self,xofs,yofs,map):
        if not map.getTile(self.x + xofs, self.y + yofs).properties['passable']=="True":
            return True
        else:
            return False


## BACKGROUND CLASSES

#We use this as a base for our map
class Tile:
    def __init__(self, properties):
        self.name = properties["name"]
        self.properties = properties
        self.tilex = 0
        self.tiley = 0
    def getProperty(self, prop):
        return self.properties[prop]

#This will have a lot of commented out lines. This is due to the fact that we do not need to render each tile anymore.
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
        #We don't need to render every single tile now
        # self.tileset = Tileset(("assets/tilesets/" + parser.get("level", "tileset")), TILE_WIDTH, TILE_HEIGHT)
        #We need to load the image of the map for the use of the background
        self.image = pygame.image.load("assets/maps/" + mapname + ".png").convert_alpha()
        self.playerx = int(parser.get("player", "startx"))
        self.playery = int(parser.get("player", "starty"))
        tmpMap = parser.get("level", "map").split('\n')
        self.dimensions = (len(tmpMap[0]), len(tmpMap))
        self.screenHandler = game.addHandler(0, self.update)
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
                # line.append(Tile(self.tileset.getTile(int(curTileProp["tilex"]), int(curTileProp["tiley"])), curTileProp))
                line.append(Tile(curTileProp))
            self.map.append(line)
        self.rect = pygame.Rect((-ScreenLocation[0], -ScreenLocation[1]), (self.dimensions[0] * TILE_WIDTH, self.dimensions[1] * TILE_HEIGHT))
    def move(self, xofs, yofs):
        self.curx += xofs
        self.cury += yofs
        self.update()

    def update(self, surface):
        #We simply update the rectangle to reflect the map's position
        self.rect = pygame.Rect((-ScreenLocation[0], -ScreenLocation[1]), (self.dimensions[0] * TILE_WIDTH, self.dimensions[1] * TILE_HEIGHT))

    def draw(self, surface):
        #We fill the background with black
        surface.fill((0,0,0))
        #And then we draw our map
        surface.blit(self.image, self.rect)
    def getTile(self, x, y):
        return self.map[y][x]


### FUNCTIONALITY CLASSES

class Overworld:
    def __init__(self, mapname):
        self.currentMap = Map(mapname)
        self.frameHandler = game.addHandler(0,self.tickBG)
        self.finalHandler = game.addHandler(5,self.tickFinal)
        self.keyHandler = game.addHandler(2, self.keyPress)
        self.currentMap.draw(screen)
        player.setPos(self.currentMap.playerx, self.currentMap.playery)

    def keyPress(self,key):
        if key == pygame.K_ESCAPE:
            game.quit()
        if key == pygame.K_LEFT:
            if not player.willCollideMap(-1,0,self.currentMap):
                player.move(-1,0)
        if key == pygame.K_RIGHT:
            if not player.willCollideMap(1,0,self.currentMap):
                player.move(1,0)
        if key == pygame.K_UP:
            if not player.willCollideMap(0,-1,self.currentMap):
                player.move(0,-1)
        if key == pygame.K_DOWN:
            if not player.willCollideMap(0,1,self.currentMap):
                player.move(0,1)

    def tickBG(self, surface):
        self.currentMap.draw(surface)
    def tickFG(self,surface):
        pass
    def tickFinal(self,surface):
        player.animationUpdate(surface)

#For the game we use a simple state machine
class Game:
    #Here is our constructor
    def __init__(self):
        # The default state can be the title menu
        self.state = 0
        self.currentLevel = None
        #6 handlers
        self.handlers = [[],[],[],[],[],[]]
    def addHandler(self, handlertype, handler):
		#Handler list:
        # 0: Frame (BG)
        # 1: Quit
        # 2: Keydown
        # 3: Screen Move (Screen offset change)
        # 4: Frame (FG)
        # 5: Frame (Final)
        self.handlers[handlertype].append(handler)
        return len(self.handlers[handlertype])
    def removeHandler(self,handlertype,handlerID):
        del(self.handlers[handlertype][handlerID])
    def setState(self,stateno,data):
        if stateno == 10:
            self.currentLevel = Overworld(data)
    def quit(self):
        log(1, "Quitting game at: " + str(datetime.datetime.now()))
        for handler in self.handlers[1]:
            handler()
        exitGame()
    def screenMove(self, xofs, yofs):
        ScreenLocation[0] += xofs
        ScreenLocation[1] += yofs
        for handler in self.handlers[3]:
            handler()
    def tick(self):
        #global mainRenderingProcess
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                for handler in self.handlers[2]:
                    handler(event.key)
        log(3, "Tick")
        # if not mainRenderingProcess.is_alive():
        #      mainRenderingProcess.run()

class RenderingProcess(threading.Thread):
    def run(self):
        global isRunning
        while isRunning:
            log(3, "Process begin")
            global counter
            for handler in game.handlers[0]:
                handler(screen)
            for handler in game.handlers[4]:
                handler(screen)
            for handler in game.handlers[5]:
                handler(screen)
            #Every second, print the current fps
            if (counter % 30) == 0:
                log(2, "Current FPS: " + str(gameClock.get_fps()))
                log(2, "Time spent in frame: " + str(gameClock.get_time()))
                log(2, "Time spent doing calculations: " + str(gameClock.get_rawtime()))
            counter += 1
            #pygame.transform.scale(screen, (1920, 1080), realscreen)
            #Flip the buffer into the display
            pygame.display.flip()
            #Wait one frame
            gameClock.tick(MAX_FPS)
            log(3, "Process end")

#General purpose functions
def exitGame():
    global isRunning
    isRunning = False
    mainRenderingProcess.join()
    pygame.display.quit()
    log(1, "Game exited at: " + str(datetime.datetime.now()))
    sys.exit()

# def screenScroll(x,y):
#     global ScreenLocation
#     ScreenLocation = [x,y]

def log(loglevel, thing):
    if DEBUG != False:
        string = ""
        if loglevel == 0:
            string = "[ERR]" + str(thing)
        elif loglevel == 1:
            string = "[WARN]" + str(thing)
        elif loglevel == 2:
            string = "[VERBOSE]" + str(thing)
        elif loglevel == 3:
            string = "[DEBUG]" + str(thing)
        else:
            string = "[UNKNOWN]" + str(thing)
        LogFile.write(str(counter) + ": " + string + '\n')
        if loglevel <= DEBUG:
            print string
#Check to make sure the game isn't being used as a module
if __name__=='__main__':
    #Initalize the pygame library
    pygame.init()
    pygame.font.init()
    #Let's try to open the log file, if debugging is enabled
    if DEBUG:
        LogFile = open("log.txt","ab")
    log(1, "Starting game at: " + str(datetime.datetime.now()))
    pygame.key.set_repeat(100, 50)
    gameClock = pygame.time.Clock()
    #We initialize the screen with our resolution
    #The commented out lines are there in case we want to use scaling.
    #screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #realscreen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
    #Set the current state to the overworld
    game = Game()
    player = Player("player")
    game.setState(10,"testmap")
    #We set up a font to draw our FPS stuff in
    myFont = pygame.font.SysFont("Arial", 30)
    counter = 0

    pygame.display.set_caption(GAME_NAME)

    ScreenLocation = [0,0]
    mainRenderingProcess = RenderingProcess()
    mainRenderingProcess.start()

    #We create an infinite loop
    while 1:
        #We check for any events that may have occured
        pygame.time.wait(5)
        game.tick()

else:
    print "This game should not be used as a module"
    sys.exit()
