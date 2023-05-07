import pygame
import button
import csv
import os
import random
from os.path import isfile,join
from life import HealthBar

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
start_game = False

############### FABY ####################

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

###load botão start##
start_img = pygame.image.load('botaoStartCanva.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (200, 200))
###load botão start##
tips_img = pygame.image.load('botaoMenuCanva.png').convert_alpha()
tips_img = pygame.transform.scale(tips_img, (200, 200))
#bg = pygame.image.load('BG.jpg').convert_alpha()
#bg = pygame.transform.scale(bg, (1000, 580))
restart_img = pygame.image.load('botaoRestartCanva.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img, (200, 200))


#DEFINIR CORES 
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (144, 201, 120)



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
                    if tile == 0 or tile == 1 or tile == 2 or tile == 4 or tile == 5 or tile == 8:
                        self.lista_obstaculos.append(tile_data)
                    elif tile == 3: 
                        water = Water(img, x * tamanho, y * tamanho)
                        water_group.add(water)
                    elif tile == 6:
                        player = Jogador('player', x * tamanho, y *tamanho,PLAYER_VEL,2.50)#tamanhos do personagem(Lucas)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 7:
                        enemy = Jogador('enemy', x * tamanho, y * tamanho,1, 2.00)
                        enemy_group.add(enemy)
                    elif tile == 9:
                        cure_potion = Potion(img, x * tamanho, y * tamanho)
                        cure_potion_group.add(cure_potion)

        return player, health_bar, enemy
    def draw(self):
        for tile in self.lista_obstaculos:
            tile[1][0] += scroll
            tela.blit(tile[0], tile[1])

class Jogador(pygame.sprite.Sprite):
    PLAYER_VEL = 1
    #INICIO DAS VARIAVEIS PRINCIPAIS
    def __init__(self, char_type, x, y,vel, scale):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        ##self speed
        self.x_vel = vel
        self.y_vel = 0
        ####EDICOES####
        self.hit = False
        self.damage_timer = 1000
        self.tempo = 0
        self.hurt = False
        ########
        self.mask = None
        #####
        self.animation_list = []
        #mudanca 
        self.flip = False
        self.virar = 1
        #####
        self.fall = False
        self.jump_count = False
        self.ataque = False
        self.width = 55
        self.height = 120
        ####
        self.health = 100
        self.max_health = 100
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.walkCount = 0
        self.idling = False
        self.idling_counter = 0

###CARREGAR IMAGENS DO PERSONAGEM#######
        animações_personagem = ['Idle', 'Walk', 'Attack', 'Death', 'Hurt']
        for animation in animações_personagem:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            numero_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(numero_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
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
        self.check_alive()


    def update_animation(self):
        #update animation
        ANIMATION_DELAY = 100
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
          self.virar = -1

        if mover_direita:
          dx = self.x_vel
          self.flip = False
          self.virar = 1 

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

        if pygame.sprite.spritecollideany(player, enemy_group): 
                enemy = pygame.sprite.spritecollideany(player, enemy_group) 
                if player.ataque == True and enemy.alive: 
                    enemy.health = 0 
                    enemy.update_action(4) 
                    enemy_group.remove(enemy) 

                else: # se o jogador não está atacando 
                    if enemy.alive:
                        self.hurt = True
                        current_time = pygame.time.get_ticks() # obtém o tempo atual em milissegundos
                        if current_time - player.damage_timer > 1000: # se passou mais de um segundo desde o último dano
                            if player.alive: 
                                player.health -= 20 # toma dano 
                            player.damage_timer = current_time # atualiza o temporizador de dano
        else:
            self.hurt = False

        #se cair em um buraco
        if self.rect.bottom > altura:
            self.health = 0
                        
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > largura + 0:
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        #update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > largura - SCROLL_THRESH and bg_scroll < (world.level_length * tamanho) - largura) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                scroll = -dx
            
        return scroll

    def enemy_move(self): 
        if self.alive and player.alive: 
            if self.virar == 1:
                enemy_moving_right = True
            else:
                enemy_moving_right = False
            enemy_moving_left = not enemy_moving_right
            self.move(enemy_moving_left, enemy_moving_right)
            self.update_action(1)
            self.walkCount += 1
            if self.walkCount > 60: ##esse valor delimita o lugar até onde ele vai 
                self.virar *= -1
                self.walkCount *= -1

        self.rect.x += scroll
          
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

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

class Potion(pygame.sprite.Sprite):
    def __init__(self,img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tamanho // 2, y + (tamanho - self.image.get_height()))

    def update(self):
        self.rect.x += scroll
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()

#CRIAR GROUPS
water_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cure_potion_group = pygame.sprite.Group()

#criar botões
# start_button = button.Button(largura // 2 - 100, altura // 2 + 150 , start_img, 1)
start_button = button.Button(largura // 2 - 220, altura // 2 + 100 , start_img, 1)
tips_button = button.Button(largura // 2 + 20, altura // 2 + 100 , tips_img, 1)
restart_button = button.Button(largura // 2 - 100, altura // 2 , restart_img, 1)

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
player, health_bar,enemy =  world.process_data(lista)

font = pygame.font.Font('Minecraftia-Regular.ttf', 18)
texto = font.render(f"INIMIGOS RESTANTES: {len(enemy_group)-2}", True, (255,255,255))
pos_texto = texto.get_rect()
pos_texto.center = (1300,25)

###MUSICA#####
pygame.mixer_music.set_volume(0.3)
musica_de_fundo =pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

rodando = True
showing_game_history = True
while rodando == True:  

    if start_game == False:
        
        # tela.fill(BLACK)

        ###Carrega imagem de fundo Menu
        

        content_table_menu_bg = pygame.image.load('menu_img/ufpe_alagada_ia.png')
        content_table_menu_bg = pygame.transform.scale(content_table_menu_bg, (largura + 100, altura + 100))
        tela.blit(content_table_menu_bg, (0,0))
        
        ###Carrega nome do jogo
        font_title = pygame.font.Font('Minecraftia-Regular.ttf', 46)
        text = font_title.render('APÓS A ENCHENTE', True, WHITE)
        text_rect_title = text.get_rect()
        text_rect_title.center = (largura // 2, altura // 2 - 130)
        tela.blit(text,text_rect_title)

        #Se tiver mostrando a história
        if showing_game_history == True:
            mensagens = [
                'Durante um período de chuva muito forte em Recife a UFPE sofreu um perigoso alagamento!',
                'Era tudo o que a legião de ratos escondidos nos esgotos do CIn precisava',
                'para invadir e sequestrar a tia Edilene a fim de conseguir acesso a todo o CIn',
                'Ajude Lucas a matar o máximo de ratos no subsolo do Centro de Informática'
            ]
            spacing = -95
            for mensagem in mensagens:
                spacing += 45
                text = font.render(mensagem, True, WHITE)
                text_rect_description = text.get_rect()
                text_rect_description.center = (largura // 2, altura // 2 + spacing)
                tela.blit(text,text_rect_description)
        else:
            
            mensagens = {
                '0':('Água de Leptospirose é morte instantânea!', 'aguaVenenosa', (1000, 225), (450, 225)),
                '1':('Movimentação e ataque em           + espaço', 'setasTeclado', (815,275)),
                '2':('Ache a poção e recupere vida!', 'potion', (915,333), (540, 333)),
                '4':('FIQUE ATENTO À SUA HEALTH BAR E BOA SORTE NO ESGOTO, GUERREIRO!', 'idlePerson', (1150, 390), (300, 390))
            }
            
            spacing = -125
            for mensagem in mensagens.values():

                spacing += 55
                text = font.render(mensagem[0], True, WHITE)
                text_rect_description = text.get_rect()
                text_rect_description.center = (largura // 2, altura // 2 + spacing)
                tela.blit(text,text_rect_description)

                #carrega imagem
                img_menu = pygame.image.load(f'menu_img/{mensagem[1]}.png').convert_alpha()
                img_menu = pygame.transform.scale(img_menu, (50, 50))
                tela.blit(img_menu, mensagem[2])

                try:
                    rotated_img = pygame.transform.flip(img_menu, True, False)
                    tela.blit(rotated_img, mensagem[3])
                except:
                    pass
                
            
        if showing_game_history == True and  tips_button.draw(tela):
            showing_game_history = False

        elif showing_game_history == False and tips_button.draw(tela):
            showing_game_history = True
        
        if start_button.draw(tela):
            start_game = True
    else:
        
        imagens()
        world.draw()
        clock.tick(FPS)
        health_bar.draw(player.health)
        player.update()
        player.draw() 

        for enemy in enemy_group:
            enemy.update()
            enemy.enemy_move()
            enemy.draw()


        water_group.update()
        water_group.draw(tela)

        cure_potion_group.update()
        cure_potion_group.draw(tela)
        ##TEXTO##
        inimigos_vivos = len(enemy_group)-2
        texto = font.render(f"INIMIGOS RESTANTES: {inimigos_vivos}", True, (255,255,255))
        pos_texto = texto.get_rect()
        pos_texto.center = (1300,25)
        tela.blit(texto,pos_texto)
        ###MUSICA##

        inimigos_vivos = len(enemy_group)-2

        if player.alive:
            if (mover_direita or mover_esquerda) and player.fall == False and player.ataque == False and player.hurt == False:
                player.update_action(1) #walk
            elif player.ataque:
                player.update_action(2) #attack
            elif player.hurt:
                player.update_action(4) #hurt
            else:
                player.update_action(0)#0: idle


            scroll = player.move(mover_esquerda,mover_direita) 
            bg_scroll -= scroll
        if not player.alive or not inimigos_vivos:
            scroll = 0
            if player.alive:
                mensagem = 'Parabéns, parsa'
            else:
                mensagem = 'Se desse mal, parsa'
            
            font_title = pygame.font.Font('Minecraftia-Regular.ttf', 46)
            text = font_title.render(mensagem, True, WHITE)
            text_rect_title = text.get_rect()
            text_rect_title.center = (largura / 2, altura / 2)
            tela.blit(text,text_rect_title)

            if restart_button.draw(tela):
                bg_scroll = 0
                lista = reset_level()

                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            lista[x][y] = int(tile)
                world = World()
                player, health_bar,enemy =  world.process_data(lista)
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
