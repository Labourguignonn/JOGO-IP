import pygame

altura = 640
rows = 16
tamanho = altura // rows


class Enemy(pygame.sprite.Sprite):
    def __init__(self, char_type,img, x, y, end):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.char_type = char_type
        self.walkCount = 0
        self.path = [x, end]
        self.vel = 3
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tamanho // 2, y + (tamanho - self.image.get_height()))
        self.flip = False

        
    def draw(self,tela):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        self.move()

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    
    def update(self,scroll):
        self.rect.x += scroll
