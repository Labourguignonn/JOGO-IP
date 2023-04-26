import pygame
from os import listdir
from os.path import isfile,join

def virar(sprites):
    return[pygame.transform.flip(sprite,True,False) for sprite in sprites]

#BAIXAR AS IMAGENS DO SPRITE E TODAS AS IMAGENS DE DIREITA PARA ESQUERDA E VICE E VERSA
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
            sprites.append(pygame.transform.scale(surface,(100,120)))#TAMANHO DO PERSONAGEM PRINCIPAL(LUCAS)
        
        if direction:
            all_sprites[image.replace(".png", "") + "_direita"] = sprites
            all_sprites[image.replace(".png", "") + "_esquerda"] = virar(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites
