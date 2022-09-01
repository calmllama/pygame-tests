import pygame
import os
import random

pygame.init()

class Object:
    def __init__(self, x, y, height, width, color):
        self.pos = pygame.math.Vector2(x, y)
        self.color = color
        self.rect = pygame.Rect(x, y, height, width)
        self.speed = pygame.math.Vector2(40.0, 10.0)
        self.gravity = 5
        self.friction = 0.99
    
    def draw(self):
        self.rect.center = (self.pos.x, self.pos.y)
        pygame.draw.circle(window, self.color, (self.pos.x, self.pos.y), self.rect.width//2)
    
    def update(self, targets):
        dir_vec = pygame.math.Vector2()
        for target in targets:
            dir_vec += (pygame.math.Vector2(target[0].rect.center) - self.rect.center) * (0.1 * target[1])
        v_len_sq = dir_vec.length_squared()
        if v_len_sq > 0:
            dir_vec.scale_to_length(self.gravity)
            self.speed = (self.speed + dir_vec) * self.friction
            self.pos += self.speed
    
    def explode(self):
        EXPLOSION = pygame.image.load(os.path.join('Assets', 'explosion.png'))
        explosionSize = 10
        EXPLOSION = pygame.transform.scale(EXPLOSION, (explosionSize,  + explosionSize))
        for i in range(100):
            expXPos = self.pos.x - (explosionSize/2)
            expYPos = self.pos.y - (explosionSize/2)
            window.blit(EXPLOSION, (expXPos, expYPos))
            EXPLOSION = pygame.transform.rotate(pygame.transform.scale(EXPLOSION, (explosionSize, explosionSize)), 90)
            pygame.display.update()
            explosionSize += i

def targetMaker():        
    targetCount = random.randrange(1, 6)
    targets = []
    for target in range(targetCount):
        xCoord = random.randrange(int(displayInfo.current_w))
        yCoord = random.randrange(displayInfo.current_h)
        rVal = random.randrange(255)
        gVal = random.randrange(255)
        bVal = random.randrange(255)
        size = random.randrange(30, 100)
        targets.append((Object(xCoord, yCoord, size, size, (rVal, gVal, bVal)), size))
    return targets

hasExploded = False
displayInfo = pygame.display.Info()
BG_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("check it")
clock = pygame.time.Clock()
meteor = Object(0, 0, 20, 20, (255, 0, 255))
targetCount = random.randrange(1, 6)
targets = targetMaker()
move = True
run = True

while run:
    window.blit(BG_IMAGE, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                move = False
                meteor = Object(250, 400, 20, 20, (255, 255, 255))
            else:
                hasExploded = False
                move = True
                targets = targetMaker()
                xCoord = random.randrange(int(displayInfo.current_w))
                yCoord = random.randrange(displayInfo.current_h)
                meteor.pos = (xCoord, yCoord)
                xSpeed = random.randrange(5, 60)
                ySpeed = random.randrange(5, 60)
                meteor.speed = pygame.math.Vector2(xSpeed, ySpeed)

    for target in targets:
        if (meteor.pos - target[0].pos).length() < ((meteor.rect.width/2)+(target[0].rect.width/2)):
            move = False

    if move:
        meteor.update(targets)
    elif not hasExploded:
        hasExploded = True
        meteor.explode()

    meteor.draw()
    for target in targets:
        target[0].draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()