import pygame
from button import Button
import csv

pygame.init()
# VALORES DA TELA
largura = 1500
altura = 640
tela = pygame.display.set_mode((largura, altura))

# CONSTANTES
FPS = 60
PLAYER_VEL = 4
SCROLL_THRESH = 300
GRAVITY = 0.1
# Cores
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (144, 201, 120)

# VARIÁVEIS
start_game = False
clock = pygame.time.Clock()
background = pygame.image.load('Esgoto/sewer.png').convert_alpha()
background = pygame.transform.scale(background, (largura,altura))
# Scroll
scroll = 0
bg_scroll = 0
# Matriz
rows = 16
colunas_max = 150
tamanho = altura // rows
level = 1
# Tiles
tipo = 10
current_tile = 0
mover_esquerda = False
mover_direita = False

# GRUPOS
water_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cure_potion_group = pygame.sprite.Group()

# BOTÕES DO MENU
# Carregar o botão de 'start'
start_img = pygame.image.load('menu_img/botaoStartCanva.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (200, 200))
# Carregar o botão de 'menu'
tips_img = pygame.image.load('menu_img/botaoMenuCanva.png').convert_alpha()
tips_img = pygame.transform.scale(tips_img, (200, 200))

# Criar o botao de restart
restart_img = pygame.image.load('menu_img/botaoRestartCanva.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img, (200, 200))

# Posicoes de botoes
start_button = Button(largura // 2 + 70, altura // 2 + 150 , start_img, 1)
tips_button = Button(largura // 2 + 310, altura // 2 + 150 , tips_img, 1)
restart_button = Button(largura // 2 - 100, altura // 2 , restart_img, 1)

# ADIÇÃO DAS IMAGENS NO INVENTARIO
img_lista = []
for x in range(tipo):
    img = pygame.image.load(f'img/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tamanho, tamanho))
    img_lista.append(img)

###MUSICA#####
pygame.mixer_music.set_volume(0.0)
musica_de_fundo = pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

#CONTADOR DE INIMIGOS TEXTO
font = pygame.font.Font('menu_img/Minecraftia-Regular.ttf', 18)
texto = font.render(f"INIMIGOS RESTANTES: {len(enemy_group)-2}", True, (255,255,255))
pos_texto = texto.get_rect()
pos_texto.center = (1300,25)

#WORLD DATA
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