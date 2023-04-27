import pygame
import button
import csv
from os import listdir
from os.path import isfile,join
from jogador import Jogador
from water import Water


pygame.init()
############### FABY #############################
#GAME WINDOW
largura = 1500
altura = 640
#lower
margem = 100
#side
margem_lado = 300


tela = pygame.display.set_mode((largura, altura + margem))
pygame.display.set_caption('Após a enchente')

#######

################### LUCAS ###############################
FPS = 30

############### FABY ####################
#variaveis scrool
esquerda = False
direita = False
scroll = 4
scroll_speed = 1
#variaveis matriz
rows = 16
colunas_max = 150
#######TILE SIZE###############
tamanho = altura // rows
level = 1
#variaveis grafico
#QUANTAS IMAGENS TEM ---  tem que mudar sempre que add alguma imagem
tipo = 8
current_tile = 0


img_lista = []
for x in range(tipo):
    #ADIÇÃO DAS IMAGENS NO INVENTARIO
    img = pygame.image.load(f'img/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tamanho, tamanho))
    img_lista.append(img)

#CRIAR LISTA COM OS ESPAÇOS VAZIOS
#World data
lista = []
for row in range(rows):
    r = [-1]*colunas_max
    lista.append(r)

#CRIAR CHÃO
for tile in range(0, colunas_max):
    lista[rows - 2][tile] = 0 ##número da foto

for tile in range(0, colunas_max):
    lista[rows - 1][tile] = 1 ##número da foto

class World():
    def __init__(self):
        self.obstacle_list = []
    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(lista):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_lista[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tamanho
                    img_rect.y = y * tamanho
                    tile_data = (img, img_rect)
            if tile >= 0 and tile <= 3:
                self.obstacle_list.append(tile_data)
            if tile == 5:
                water = Water(img, x * tamanho, y * tamanho)
            if tile == 6:#create player
                player = Jogador('player',100,100,80,80)
        return player
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += scroll
            tela.blit(tile[0], tile[1])
