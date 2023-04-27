import pygame
import button
import csv
from os import listdir
from os.path import isfile,join
from jogador import Jogador

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
scroll = 0
bg_scroll = 0
#variaveis matriz
rows = 16
colunas_max = 150
#######TILE SIZE###############
tamanho = altura // rows
level = 1
#variaveis grafico
#QUANTAS IMAGENS TEM ---  tem que mudar sempre que add alguma imagem
tipo = 7
current_tile = 0


#ADD AS IMAGES
background = pygame.image.load('Esgoto/sewer.png').convert_alpha()
background = pygame.transform.scale(background, (largura,altura))

img_lista = []
for x in range(tipo):
    #ADIÇÃO DAS IMAGENS NO INVENTARIO
    img = pygame.image.load(f'img/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tamanho, tamanho))
    img_lista.append(img)


#DEFINIR CORES 
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (144, 201, 120)


font = pygame.font.SysFont('Futura', 30)

def imagens():
    tela.fill(WHITE)
    width = tela.get_width()
    #quantas vezes a imagem repete 
    for x in range(4):
        tela.blit(background,((x*width) - bg_scroll*0.7, 0)) ##0.7 == velocidade que move a tela

class World():
    def __init__(self):
        self.lista_obstaculos = []
    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_lista[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tamanho
                    img_rect.y = y * tamanho
                    tile_data = (img, img_rect)
                    if tile == 0 or tile == 2 or tile == 4 or tile == 5 or tile == 1:
                        self.lista_obstaculos.append(tile_data)
                    if tile == 3: 
                        pass #agua 
                    else:
                        player = Jogador('player', x * tamanho, y * tamanho, 1.65, 5)#tamanhos do personagem(Lucas)

        return player
    def draw(self):
        for tile in self.lista_obstaculos:
            tile[1][0] -= scroll
            tela.blit(tile[0], tile[1])
#World data
lista = []
for row in range(rows):
    r = [-1]*colunas_max
    lista.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			lista[x][y] = int(tile)
world = World()
player =  world.process_data(lista)

rodando = True
while rodando == True:
    imagens()
    world.draw()
    

    #water_group.update()
    #water_group.draw(screen)
    

        #MOVER A TELA 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False 
        #pressionar teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                esquerda = True
            if event.key == pygame.K_RIGHT:
                direita = True
            if event.key == pygame.K_UP: #pulo do personagem
                player.jump()
            if event.key == pygame.K_SPACE:
                player.atacar()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                esquerda = False
            if event.key == pygame.K_RIGHT:
                direita = False

    # impede que a tela role para fora dos limites definidos
    if scroll < 0:
        scroll = 0
    if scroll > largura - margem_lado:
        scroll = largura - margem_lado

    # parte do personagem carreagndo na tela(Lucas)
    player.loop(FPS) 
    player.movimento()
    player.update()
    player.draw(tela) 
    pygame.display.update()



    
pygame.quit()
