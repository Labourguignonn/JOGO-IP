import pygame
import button
import csv
import os
from os.path import isfile,join
from life import HealthBar
from enemies import Enemy
from potion import Potion


largura = 1500
altura = 640
margem = 100
margem_lado = 300
pygame.init()
############### FABY #############################
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Após a enchente')

################### LUCAS ###############################
FPS = 60
clock = pygame.time.Clock()
PLAYER_VEL = 4
SCROLL_THRESH = 300
GRAVITY = 0.1

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
tipo = 10
current_tile = 0
mover_esquerda = False
mover_direita = False

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
    enemy_group.empty()
    cure_potion_group.empty()
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
                        enemy = Enemy('enemy',img,tamanho, 1000, 496, 32, 32, 1300)
                        enemy_group.add(enemy)
                    if tile == 6:
                        player = Jogador('player', x * tamanho, y *tamanho,PLAYER_VEL,2.50)#tamanhos do personagem(Lucas)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    if tile == 9:
                        cure_potion = Potion(img, x * tamanho, y * tamanho,tamanho)
                        cure_potion_group.add(cure_potion)


        return player, health_bar
    def draw(self):
        for tile in self.lista_obstaculos:
            tile[1][0] += scroll
            tela.blit(tile[0], tile[1])

class Jogador(pygame.sprite.Sprite):
    PLAYER_VEL = 1
    #INICIO DAS VARIAVEIS PRINCIPAIS
    def __init__(self, char_type, x, y,vel, scale):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        ##self speed
        self.x_vel = vel
        self.y_vel = 0
        self.mask = None
        #####
        self.animation_list = []
        #mudanca 
        self.flip = False
        #####
        self.fall = False
        self.jump_count = False
        self.ataque = False
        self.width = 55
        self.height = 120
        ####
        self.health = 100
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.walkCount = 0

###CARREGAR IMAGENS DO PERSONAGEM#######
        animações_personagem = ['Idle', 'Walk', 'Attack', 'Death', 'Hurt']
        for animation in animações_personagem:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            numero_frames = len(os.listdir(f'personagem/{animation}'))
            for i in range(numero_frames):
                img = pygame.image.load(f'personagem/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    
    def update(self):
        self.update_animation()

    def update_animation(self):
        #update animation
        ANIMATION_DELAY = 130
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1       
            else:
                self.frame_index = 0
                
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    #FUNCAO SOMA A VEL NA POSICAO PRA ANDAR
    def move(self, mover_esquerda,mover_direita):
        dx = 0
        dy = self.y_vel
        if mover_esquerda:
          dx = -self.x_vel
          self.flip = True 

        if mover_direita:
          dx = self.x_vel
          self.flip = False

        if self.jump_count == True and self.fall == False:
          self.y_vel = -4
          self.jump_count = False
          self.fall = True
        
        
        self.y_vel += GRAVITY
        if self.y_vel > 10:
            self.y_vel
        dy += self.y_vel
    

        #check for collision
        scroll = 0
        for tile in world.lista_obstaculos:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0      
            
                if self.char_type == 'enemy':
                        print("inimigo")
                        self.flip = False
                        self.walkCount = 0
            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground, i.e. jumping
                if self.y_vel < 0:
                    self.y_vel = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.y_vel >= 0:
                    self.y_vel = 0
                    self.fall = False
                    self.jump_count = False
                    dy = tile[1].top - self.rect.bottom
        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        if self.rect.bottom > altura:
            self.health -= 10
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > largura + 0:
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        #check collision with health potion
        if pygame.sprite.spritecollide(self, cure_potion_group, False):
            self.health += 25
        
        #update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > largura - SCROLL_THRESH and bg_scroll < (world.level_length * tamanho) - largura) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                scroll = -dx
        return scroll
    
    def draw(self):
	    tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    
class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tamanho // 2, y + (tamanho - self.image.get_height()))

	def update(self):
		self.rect.x += scroll

#CRIAR GROUPS
water_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cure_potion_group = pygame.sprite.Group()

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
player, health_bar =  world.process_data(lista)

rodando = True
while rodando == True:
    imagens()
    world.draw()
    clock.tick(FPS)
    health_bar.draw(player.health)
    player.update()
    player.draw() 

    water_group.update()
    water_group.draw(tela)
    
    cure_potion_group.update(scroll)
    cure_potion_group.draw(tela)
    
    if (mover_direita or mover_esquerda) and player.fall == False and player.ataque == False:
        player.update_action(1) #walk
    elif player.ataque:
        player.update_action(2) #attack
    else:
        player.update_action(0)#0: idle


    scroll = player.move(mover_esquerda,mover_direita) 
    bg_scroll -= scroll

    for enemy in enemy_group:
        enemy.update(scroll)
        enemy.draw(tela)


        #MOVER A TELA 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False 
        #pressionar teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mover_esquerda = True
            if event.key == pygame.K_RIGHT:
                mover_direita = True
            if event.key == pygame.K_UP: #pulo do personagem
                player.jump_count = True
            if event.key == pygame.K_SPACE:
                player.ataque = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                mover_esquerda = False
            if event.key == pygame.K_RIGHT:
                mover_direita = False
            if event.key == pygame.K_SPACE:
                player.ataque = False

    pygame.display.update()


pygame.quit()
