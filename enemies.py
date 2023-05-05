import pygame
import os
import random

altura = 640
rows = 16
tamanho = altura // rows


class Enemy(pygame.sprite.Sprite):
    def __init__(self, char_type,img, x, y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.x = x
        self.y = y
        self.char_type = char_type
        self.walkCount = 0
        self.animation_list = []
        self.vel = 1
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tamanho // 2, y + (tamanho - self.image.get_height()))
        self.flip = False
        self.virar = 1
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        animações_personagem = ['Idle', 'Walk', 'Death', 'Hurt']
        for animation in animações_personagem:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            numero_frames = len(os.listdir(f'img/enemy/{animation}'))
            for i in range(numero_frames):
                img = pygame.image.load(f'img/enemy/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
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
    def move(self, ai_moving_left, ai_moving_right):
        


    def ai(self,scroll):
        if self.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = 50
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.walkCount += 1

                    if self.walkCount > tamanho:
                        self.virar *= -1
                        self.walkCount *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += scroll

    def draw(self,tela):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    
    def update(self,scroll):
       self.update_animation()
       self.rect.x += scroll
