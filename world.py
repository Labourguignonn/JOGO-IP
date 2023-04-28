import pygame
import button
import csv
from os import listdir
from os.path import isfile,join
from funçoes import *

pygame.init()
############### FABY #############################
#GAME WINDOW
largura = 1500
altura = 640
#lower
margem = 100
#side
margem_lado = 300


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Após a enchente')

#######

################### LUCAS ###############################
FPS = 30
PLAYER_VEL = 1
SCROLL_THRESH = 0

############### FABY ####################
#variaveis scrool
esquerda = False
direita = False
scroll = 0
bg_scroll = 0
scroll = 0
#variaveis matriz
rows = 16
colunas_max = 150
#######TILE SIZE###############
tamanho = altura // rows
level = 1
#variaveis grafico
#QUANTAS IMAGENS TEM ---  tem que mudar sempre que add alguma imagem
tipo = 9
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

def reset_level():
    water_group.empty()
    data = []
    for row in range(rows):
        r = [-1]*colunas_max
        data.append(r)

    return data


class World():
    def __init__(self):
        self.lista_obstaculos = []
    def process_data(self, data):
        self.level_length = len(data[0])
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
                        water = Water(img, x * tamanho, y * tamanho)
                        water_group.add(water)
                    if tile == 7 or tile == 8:
                        pass #inimigos
                    if tile == 6:
                        player = Jogador('player', x * tamanho, y *tamanho)#tamanhos do personagem(Lucas)

        return player
    def draw(self):
        for tile in self.lista_obstaculos:
            tile[1][0] += scroll
            tela.blit(tile[0], tile[1])

class Jogador(pygame.sprite.Sprite):
    PLAYER_VEL = 1
    GRAVITY = 0.1
    SPRITES = baixar_sprite("personagem",48,50, True)
    ANIMATION_DELAY = 50
    #INICIO DAS VARIAVEIS PRINCIPAIS
    def __init__(self, char_type, x, y):
        self.rect = pygame.Rect(x,y,55,120)
        ########
        self.char_type = char_type
        self.y_vel = 0
        ##self speed
        self.x_vel = 0
        self.mask = None
        #mudanca 
        self.virar = 'esquerda'
        #####
        self.attack_animation_count = 0
        self.animation_count = 0
        self.fall_count = True
        self.jump_count = False
        self.ataque = False
        self.width = 55
        self.height = 120
        
    #FUNCAO SOMA A VEL NA POSICAO PRA ANDAR
    def move(self, dx, dy):
        #check for collision
        scroll = 0
        for tile in world.lista_obstaculos:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.left + dx, self.rect.y, self.width, self.height):
                dx = 0
            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground, i.e. jumping
                if self.y_vel< 0:
                    self.y_vel = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.y_vel >= 0:
                    self.y_vel = 0
                    self.jump_count = False
                    dy = tile[1].top - self.rect.bottom
        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        if self.char_type == 'player':
            if self.rect.left + dx < -50 or self.rect.right + dx > largura + 50:
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        #update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > largura - SCROLL_THRESH and bg_scroll < (world.level_length * tamanho) - largura) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                scroll = -dx
        return scroll


    def mover_esquerda(self, vel):
        self.x_vel = -vel
        if self.virar != 'esquerda':
            self.virar = 'esquerda'
            self.animation_count = 0
    
    def mover_direita(self,vel):
        self.x_vel = vel
        if self.virar != 'direita':
               self.virar = 'direita'
               self.animation_count = 0
    def jump(self):
        if self.jump_count == False:
          self.y_vel = -4
          self.jump_count = True

        #FUNCAO QUE VAI VERIFICAR O QUE O PERSONAGEM FAZ A CADA FRAME
    def loop(self, fps):
        self.y_vel += min(0.05, (self.fall_count/6*fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.movimento()
        self.fall_count += 0.3
        self.update_sprite()

    def update_sprite(self):
        if self.ataque:
            sprite_sheet_name = "Attack" + "_" + self.virar
            sprites = self.SPRITES[sprite_sheet_name]
            sprite_index = (self.attack_animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.sprite = sprites[sprite_index]
            self.attack_animation_count += 1
            if self.attack_animation_count >= len(sprites) * self.ANIMATION_DELAY:
                self.ataque = False
                self.attack_animation_count = 0
        else:
            sprite_sheet = "Idle"
            if self.x_vel != 0:
                sprite_sheet = "Walk"
            sprite_sheet_name = sprite_sheet + "_" + self.virar
            sprites = self.SPRITES[sprite_sheet_name]
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.sprite = sprites[sprite_index]
            self.animation_count += 1

        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    def atacar(self):
      if self.ataque == False:
        self.ataque = True 
        
    def draw(self,tela):
        tela.blit(self.sprite, (self.rect.x,self.rect.y))
    
    
    def movimento(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.mover_esquerda(PLAYER_VEL)
           
        if keys[pygame.K_RIGHT]:
            self.mover_direita(PLAYER_VEL)

class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tamanho // 2, y + (tamanho - self.image.get_height()))

	def update(self):
		self.rect.x += scroll

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
                        
#CRIAR GROUPS

water_group = pygame.sprite.Group()
world = World()
player =  world.process_data(lista)

rodando = True
while rodando == True:
    imagens()
    world.draw()
    

    player.loop(FPS) 
    player.movimento()
    player.update()
    player.draw(tela) 

    water_group.update()
    water_group.draw(tela)
    
    scroll = player.move(0,0)
    #pode ser move(1,-1) ou (1, 0) 
    bg_scroll -= scroll

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

    pygame.display.update()


pygame.quit()
