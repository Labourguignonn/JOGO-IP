import pygame
import os
from os.path import isfile,join
class Potion(pygame.sprite.Sprite):

	def __init__(self,img, x, y,tamanho):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tamanho // 2, y + (tamanho - self.image.get_height()))
	
	def update(self,scroll):
		self.rect.x += scroll
	

	

	
	def kill(self):
		self.kill()
