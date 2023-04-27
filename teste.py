import pygame
from pygame.locals import *
from sys import exit

pygame.init()
largura = 1500
altura = 640
margem = 100
tela = pygame.display.set_mode((largura, altura + margem))

class Inimigos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("rato\Idle\idle_01.png"))
        self.sprites.append(pygame.image.load("rato\Idle\idle_02.png"))
        self.sprites.append(pygame.image.load("rato\Idle\idle_03.png"))
        self.sprites.append(pygame.image.load("rato\Idle\idle_04.png"))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (30*2, 32*2))

        self.rect = self.image.get_rect()
        self.rect.topleft = 250, 500

        self.animar = False

    def atacar(self):
        self.animar = True

    def update(self):
        if self.animar == True:
            self.atual += 0.5
            if self.atual >= len(self.sprites+1):
                self.atual = 0
                self.animar = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (30*2, 32*2))
            
#### BRUNA ####
inimigos = pygame.sprite.Group()
rato = Inimigos()
inimigos.add(rato)
""" relogio = pygame.time.Clock() """

rodando = True
while rodando == True:
    
    #####carregar inimigos#####
    inimigos.draw(tela)
    inimigos.update()
    pygame.display.flip()
    
pygame.quit()
