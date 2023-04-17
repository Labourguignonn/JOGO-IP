import pygame
from pygame.locals import *
from sys import exit
from os import listdir
from os.path import isfile,join

pygame.init()
pygame.display.set_caption("Jogo esgoto")
largura = 1500
altura = 700

tela = pygame.display.set_mode((largura,altura))

background = pygame.image.load("Esgoto/sewer.png").convert_alpha()
background = pygame.transform.scale(background, (largura,altura))

FPS = 50
PLAYER_VEL = 1 
def virar(sprites):
    return[pygame.transform.flip(sprite,True,False) for sprite in sprites]
#BAIXAR AS IMAGENS DO SPRITE

def baixar_sprite(dir1,width,height,direction = False):
    path = join(dir1)
    images = [f for f in listdir(path) if isfile(join(path,f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range (sprite_sheet.get_width() // width):
            surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale(surface,(100,140)))#TAMANHO DO PERSONAGEM PRINCIPAL(LUCAS)
        
        if direction:
            all_sprites[image.replace(".png", "") + "_direita"] = sprites
            all_sprites[image.replace(".png", "") + "_esquerda"] = virar(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites



#CLASSE QLQR PERSONAGEM
class Jogador(pygame.sprite.Sprite):
    GRAVITY = 0.1
    SPRITES = baixar_sprite("personagem",48,50, True)
    ANIMATION_DELAY = 100

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "esquerda"
        self.animation_count = 0
        self.fall_count = 0
    
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def mover_esquerda(self,vel):
      self.x_vel = -vel
      if self.direction != "esquerda":
        self.direction = "esquerda"
        self.animation_count = 0
    
    def mover_direita(self,vel):
        self.x_vel = vel
        if self.direction != "direita":
          self.direction = "direita"
          self.animation_count = 0
    def loop(self, fps):
        #self.y_vel += min(0.1, (self.fall_count/fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.fall_count += 0.1
        self.update_sprite()
    
    def update_sprite(self):
      sprite_sheet = "Idle"
      if self.x_vel != 0:
        sprite_sheet = "Walk"
      sprite_sheet_name = sprite_sheet + "_" + self.direction
      sprites = self.SPRITES[sprite_sheet_name]
      sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
      self.sprite = sprites[sprite_index]
      self.animation_count += 1
      self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    
    def draw(self,tela):
        tela.blit(self.sprite, (self.rect.x,self.rect.y))




player = Jogador(100,100,80,80)#tamanhos do personagem(Lucas)

def movimento(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.mover_esquerda(float(PLAYER_VEL))
    if keys[pygame.K_RIGHT]:
        player.mover_direita(float(PLAYER_VEL))
    
    
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
    
    # parte do personagem carreagndo na tela(Lucas)
    player.loop(FPS) 
    movimento(player)
    player.draw(tela) 

    pygame.display.update()
