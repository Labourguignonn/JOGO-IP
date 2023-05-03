import pygame

class enemy(object):
    walkRight = [pygame.image.load('rato/walk/walk_01.png'), pygame.image.load('rato/walk/walk_02.png'), pygame.image.load('rato/walk/walk_03.png'), pygame.image.load('rato/walk/walk_04.png')]
    walkLeft = [pygame.image.load('rato/walk/walk_05.png'), pygame.image.load('rato/walk/walk_06.png'), pygame.image.load('rato/walk/walk_07.png'), pygame.image.load('rato/walk/walk_08.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(pygame.transform.scale(self.walkRight[self.walkCount//3], (64, 64)), (self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(pygame.transform.scale(self.walkLeft[self.walkCount//3], (64, 64)), (self.x,self.y))
            self.walkCount += 1
            
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
