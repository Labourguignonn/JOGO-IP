import pygame
from pygame.locals import *
from sys import exit

pygame.init()
pygame.display.set_caption("Jogo esgoto")
largura = 1500
altura = 700

tela = pygame.display.set_mode((largura,altura))

background = pygame.image.load("sewer.png").convert_alpha()
background = pygame.transform.scale(background, (largura,altura))


rodando = True
while rodando == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False 
            exit
    tela.blit(background, (0,0))
    
    rel_largura = largura % background.get_rect().width
    tela.blit(background, (rel_largura - background.get_rect().width,0))
    if rel_largura < 1500:
        tela.blit(background, (rel_largura, 0))


    #movimento
    largura += 0.75


    pygame.display.update()