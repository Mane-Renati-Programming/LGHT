import pygame
pygame.init()

class Canvas(pygame.sprite.Sprite):
    def __init__(self, dimensions, spritesheet, tilesize=32):
        pygame.sprite.Sprite.__init__(self)
        self.set_spritesheet(spritesheet, tilesize)
        self.set_dimensions(dimensions)
        self.set_brush('.') # Set to 0

    def set_dimensions(self, dimensions):
        # Some basic sanity checking
        if dimensions[0] > 5:
            self.length = dimensions[0]
        else:
            self.length = 5

        if dimensions[1] > 5:
            self.height = dimensions[1]
        else:
            self.height = 5

        self.image = pygame.Surface((self.height*self.tilesize, self.length*self.tilesize))
        self.image.fill((150,150,150))
        self.rect = self.image.get_rect()

        self.canvas = [[' ' for _ in xrange(self.length)] for __ in xrange(self.height)]

    def set_spritesheet(self, spritesheet, tilesize):
        # Chops up a spritesheet and returns it for use
        image = pygame.image.load(spritesheet)
        rect  = image.get_rect()
        self.spritesheet = []
        self.tilesize = tilesize

        for i in xrange(rect.width/tilesize):
            for j in xrange(rect.height/tilesize):
                temp = pygame.Rect(i*tilesize, j*tilesize, tilesize, tilesize)
                self.spritesheet.append(image.subsurface(temp))

    def set_brush(self, tile):
        self.brush = tile

    def get_brush(self):
        return self.brush

    def get_index(self):
        return self.to_index(self.brush)

    def get_tile(self):
        return self.spritesheet[self.get_index()]

    def draw(self, pos):
        # Update map and draw the character onto it

        pos = [pos[0]/self.tilesize,pos[1]/self.tilesize]

        self.canvas[pos[0]][pos[1]] = self.brush
        self.image.blit(self.spritesheet[self.to_index(self.brush)], [pos[0]*self.tilesize, pos[1]*self.tilesize])

    def to_index(self, brush):
        chars = '.#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return chars.index(brush)

    def to_brush(self, index):
        chars = '.#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return chars[index%len(self.spritesheet)]

    def update(self):
        pass

DISPLAY_DIMENSIONS = [500,500]
CANVAS_SIZE = [8,8]
TILESET_NAME = '../assets/tilesets/PathAndObjects.png'

clock = pygame.time.Clock()
canvas = Canvas(CANVAS_SIZE, TILESET_NAME)
screen = pygame.display.set_mode(DISPLAY_DIMENSIONS)
exited = False

allSprites = pygame.sprite.Group(canvas)
offset = [0,0]

while not(exited):
    delta_time = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                canvas.set_brush(canvas.to_brush(canvas.get_index()+1))
            elif event.button == 5:
                canvas.set_brush(canvas.to_brush(canvas.get_index()-1))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save = open('map.txt', 'wb')
                save.writelines('\n'.join([''.join(i) for i in canvas.canvas]))
                save.close()
        elif event.type == pygame.QUIT:
            exited = True

    pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        canvas.draw([pos[0]-offset[0],pos[1]-offset[1]])

    rel = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[1]:
        offset[0] += rel[0]
        offset[1] += rel[1]

    canvas.update()

    allSprites.update()
    screen.fill((0,0,0))
    screen.blit(canvas.image, offset)
    pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, 0, 52, 52))
    screen.blit(canvas.get_tile(), [10,10])
    pygame.display.flip()

pygame.quit()
