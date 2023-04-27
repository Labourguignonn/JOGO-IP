""" import pygame

pygame.init()

largura = 1500
altura = 640
margem = 100
margem_lado = 300

tela = pygame.display.set_mode((largura, altura + margem))
class Inimigos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lista_sprites = []
        self.lista_sprites.append(pygame.image.load("rato\walk\walk_01.png"))
        self.lista_sprites.append(pygame.image.load("rato\walk\walk_02.png"))
        self.lista_sprites.append(pygame.image.load("rato\walk\walk_03.png"))
        self.lista_sprites.append(pygame.image.load("rato\walk\walk_04.png"))
        self.imagem_atual = 0
        self.image = self.lista_sprites[self.imagem_atual]
        
        #definir a posição da sprite 
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100
        
rato = Inimigos() """