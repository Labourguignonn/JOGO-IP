import pygame

RED = (255,0,0)
GREEN = (0,255,0)

largura = 1500
altura = 640
tela = pygame.display.set_mode((largura, altura))


class HealthBar():

    def __init__(self, x, y, health, max_health):
        self.x = x  #Coordinates of the health bar
        self.y = y  #Coordinates of the health bar
        self.health = health
        self.max_health = max_health


    def draw(self, health):
        #update with new health
        self.health = health
        #draws a RED rectangle with max_health
        #Health bar size (bar_width, bar_height)
        #Use (150, 20) for player and smaller for enemies
        ratio = self.health / self.max_health
        pygame.draw.rect(tela, RED, (self.x, self.y, 150, 20)) 
        pygame.draw.rect(tela, GREEN, (self.x, self.y, 150 * ratio, 20)) 

#Desenhar a health bar do jogador no loop principal do jogo
#Desenhar a health bar de cada inimigo 