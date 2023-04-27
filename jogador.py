import pygame
from os import listdir
from os.path import isfile,join
from funçoes import *
from main import World
pygame.init()
#GAME WINDOW
largura = 1500
altura = 640
#lower
margem = 100

rows = 16
#side
tamanho = altura // rows
margem_lado = 300
PLAYER_VEL = 1
SCROLL_THRESH = 200

bg_scroll = 0
screen_scroll = 0
tela = pygame.display.set_mode((largura, altura + margem))

#CLASSE PERSONAGEM PRINCIPAL
class Jogador(pygame.sprite.Sprite):
    GRAVITY = 0.1
    SPRITES = baixar_sprite("personagem",48,50, True)
    ANIMATION_DELAY = 50
    #INICIO DAS VARIAVEIS PRINCIPAIS
    def __init__(self, char_type, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
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
        
    #FUNCAO SOMA A VEL NA POSICAO PRA ANDAR
    def move(self, dx, dy):
        ####################
        if self.char_type == 'player':
            if self.rect.left + dx < -50 or self.rect.right + dx > largura + 50:
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        if self.char_type == 'player':
            if (self.rect.right > largura - SCROLL_THRESH and bg_scroll < (World.level_length * tamanho) - largura)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll
        
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
    ######mudanca#######
          self.y_vel = -5
          self.jump_count = True

        #FUNCAO QUE VAI VERIFICAR O QUE O PERSONAGEM FAZ A CADA FRAME
    def loop(self, fps):
        self.y_vel += min(0.05, (self.fall_count/6*fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.checar_chao(self.y_vel)
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
    
    def checar_chao(self,dy):
        if self.rect.bottom + dy > 563:
            self.y_vel =  0
            self.jump_count = False
    
    def movimento(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.mover_esquerda(PLAYER_VEL)
        if keys[pygame.K_RIGHT]:
            self.mover_direita(PLAYER_VEL)