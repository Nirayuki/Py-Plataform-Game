import pygame 
from pygame.locals import *
import os


pygame.init()

# Images ----------------------------------------------------------------


# Variaveis ----------------------------------------------------------------

SCREEN_WIDTH, SCREEN_HEIGTH = 1200, 720 
FPS = 60


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Plataform Game")



# Colors ----------------------------------------------------------------

GREEN = (124,252,0)
WHITE = (225, 225, 225)

# Class ----------------------------------------------------------------

class Sapo(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        self.sprites.append(pygame.image.load('Assets/attack_1.png'))
        self.sprites.append(pygame.image.load('Assets/attack_2.png'))
        self.sprites.append(pygame.image.load('Assets/attack_3.png'))
        self.sprites.append(pygame.image.load('Assets/attack_4.png'))
        self.sprites.append(pygame.image.load('Assets/attack_5.png'))
        self.sprites.append(pygame.image.load('Assets/attack_6.png'))
        self.sprites.append(pygame.image.load('Assets/attack_7.png'))
        self.sprites.append(pygame.image.load('Assets/attack_8.png'))
        self.sprites.append(pygame.image.load('Assets/attack_9.png'))
        self.sprites.append(pygame.image.load('Assets/attack_10.png'))
        self.index = 0
        self.image = self.sprites[int(self.index)]
        self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))

        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100

        self.animar = False

    def update(self):
        if self.animar == True:
            self.index += 0.20
            if self.index >= len(self.sprites):
                self.index = 0
                self.animar = False
            self.image = self.sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))

    def atacar(self):
        self.animar = True
     
# Funções ----------------------------------------------------------------

run = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
sapo = Sapo()
all_sprites.add(sapo)

while run:
    SCREEN.fill(GREEN)
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == KEYDOWN:
            sapo.atacar()
    

    all_sprites.draw(SCREEN)
    all_sprites.update()
    pygame.display.flip() # update display
    


pygame.quit()