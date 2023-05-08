import pygame
import csv
import os
from os.path import isfile,join
from life import HealthBar
from water import Water
from game_variables import *
from game_functions import *

pygame.init()

class World():
    def __init__(self):
        self.lista_obstaculos = []
    
    #ASSOCIAR OS TILES AS CLASSES
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
        # Velocidade do personagem
        self.x_vel = vel
        self.y_vel = 0
        # Fatores auxiliares
        self.hit = False
        self.damage_timer = 1000
        self.tempo = 0
        self.hurt = False
        self.mask = None
        self.animation_list = []
        # Mudança 
        self.flip = False
        self.virar = 1
        # Ações
        self.fall = False
        self.jump_count = False
        self.ataque = False
        self.width = 55
        self.height = 120
        # Atributos
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
            # Resetar lista temporária de imagens
            temp_list = []
            # Contar número de arquivos na pasta
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
        # variável de delay da animação
        ANIMATION_DELAY = 100
        # atualizar a imagem dependendo do frame atual
        self.image = self.animation_list[self.action][self.frame_index]
        # checar se tempo o bastante passou desde o último update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #se acabar a animação, voltar para a primeira da sequência
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1       
            else:
                self.frame_index = 0
                
    def update_action(self, new_action):
        #checar se nova ação é diferente da última
        if new_action != self.action:
            self.action = new_action
            # atualizar
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    #MOVIMENTO DO PERSONAGEM E COLISÕES
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
    

        #CHECAR COLISÃO(x,y)
        scroll = 0
        for tile in world.lista_obstaculos:
            #checar colisão na direção horizontal
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0  
            ##checar colisão na direção vertical##
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #checar a colisão com blocos acima
                if self.y_vel < 0:
                    self.y_vel = 0
                    dy = tile[1].bottom - self.rect.top
                #checar colisão com chão abaixo
                elif self.y_vel >= 0:
                    self.y_vel = 0
                    self.fall = False
                    self.jump_count = False
                    dy = tile[1].top - self.rect.bottom
        ##checar colisão com a água##
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        #checar colisão com inimigo
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

        # se cair em um buraco
        if self.rect.bottom > altura:
            self.health = 0
                        
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > largura + 0:
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > largura - SCROLL_THRESH and bg_scroll < (world.level_length * tamanho) - largura) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                scroll = -dx
            
        return scroll
    
    #CRIAÇÃO DO INIMIGO
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



world = World()
player, health_bar,enemy =  world.process_data(lista)
rodando = True
showing_game_history = True
while rodando == True:  

    if start_game == False:

        ###Carrega imagem de fundo Menu
        menu_inicial(showing_game_history)
                   
        if showing_game_history == True and  tips_button.draw(tela):
            showing_game_history = False

        elif showing_game_history == False and tips_button.draw(tela):
            showing_game_history = True
        
        if start_button.draw(tela):
            start_game = True
    else:
        
        imagens(tela)
        world.draw()
        clock.tick(FPS)
        
        ## UPDATES E DRAWS DE CLASSES E GRUPOS ##
        # health bar
        health_bar.draw(player.health)
        
        # player
        player.update()
        player.draw() 
        
        # enemy
        for enemy in enemy_group:
            enemy.update()
            enemy.enemy_move()
            enemy.draw()

        # water group
        water_group.update(scroll)
        water_group.draw(tela)
        
        # cure potion
        cure_potion_group.update()
        cure_potion_group.draw(tela)
        
        ##TEXTO##
        inimigos_vivos = len(enemy_group)-2
        texto = font.render(f"INIMIGOS RESTANTES: {inimigos_vivos}", True, (255,255,255))
        pos_texto = texto.get_rect()
        pos_texto.center = (1300,25)
        tela.blit(texto,pos_texto)

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
                mensagem = 'Parabéns! O CIn está livre de ameaças e você salvou a tia Edilene'
            else:
                mensagem = 'Foi de arrasta pra cima!!!'
            
            pygame.draw.rect(tela, BLACK, pygame.Rect(30, 30, 60, 60))
            

            font_title = pygame.font.Font('menu_img/Minecraftia-Regular.ttf', 46)
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
        # pressionar teclas
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
