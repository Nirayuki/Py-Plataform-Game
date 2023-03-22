import pygame
import os
from random import randrange

pygame.init()

# Variaveis ----------------------------------------------------------------

SCREEN_WIDTH, SCREEN_HEIGTH = 640, 420
FPS = 60
JUMP_FORCE = 10
GRAVITY_FORCE = 20

main_dir = os.path.dirname(__file__)
img_dir = os.path.join(main_dir, 'Assets')

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Plataform Game")


# Colors ----------------------------------------------------------------

BLACK = (0, 0, 0)
WHITE = (225, 225, 225)

# Images ----------------------------------------------------------------

SPRITE_SHEET = pygame.image.load(os.path.join(img_dir, 'dinoSpritesheet.png'))


# Class ----------------------------------------------------------------

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Criando um array para segurar todas as imagens para animação
        self.img_dinossauro = []

        # Criando um loop para a quantidade de imagens que o sprite tem
        for i in range(3):
            img = SPRITE_SHEET.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.img_dinossauro.append(img)

        # Para animação estou criando o sistema de animações.
        self.index = 0
        self.image = self.img_dinossauro[self.index]

        # Essa função indentifica que eu quero criar um retângulo e adicionar a imagem dentro dele básicamente...
        self.rect = self.image.get_rect()

        self.postition_y_initial = SCREEN_HEIGTH - 64 - 96//2 # Divido por 96//2 pq o rect.y pega o ponto 0 do x,y da imagem, já o rect.center pega o ponto central

        self.rect.center = (100, SCREEN_HEIGTH - 64)

        self.pulo = False

    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                print(self.rect.y)
                self.pulo == False
            self.rect.y -= 20
        else:
            if self.rect.y < self.postition_y_initial:
                self.rect.y += 20
            else:
                self.rect.y = self.postition_y_initial

        if self.index > 2:
            self.index = 0
        self.index += 0.20
        self.image = self.img_dinossauro[int(self.index)]
    

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    	# Procurando a imagem dentro do SPRITE_SHEET
        self.image = SPRITE_SHEET.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))

        # Essa função indentifica que eu quero criar um retângulo e adicionar a imagem dentro dele básicamente...
        self.rect = self.image.get_rect()

        # Randomizando onde a nuvem vai nascer no eixo Y
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = SCREEN_WIDTH - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10

class Ground(pygame.sprite.Sprite):
    def __init__(self, position_x):
        pygame.sprite.Sprite.__init__(self)

        # Procurando a imagem dentro do SPRITE_SHEET
        self.image = SPRITE_SHEET.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2)) # 64px

        # Essa função indentifica que eu quero criar um retângulo e adicionar a imagem dentro dele básicamente...
        self.rect = self.image.get_rect()

        # Colocando na tela o ground
        self.rect.x = position_x * 64
        self.rect.y = SCREEN_HEIGTH - 64

    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
        self.rect.x -= 10

# Main ----------------------------------------------------------------


# Criando um grupo de Sprite para poder desenhar e dar update em todos os Itens
all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)


# Aqui eu estou criando 4 nuvens e adicionando no meu grupo de sprites chamado all_sprites
for i in range(4):
    cloud = Clouds()
    all_sprites.add(cloud)


# Adicionando o Ground
for i in range(int(SCREEN_WIDTH * 2//64)): # Dividino o tamanho da tela por 64px para poder preencher toda a tela
    ground = Ground(i)
    all_sprites.add(ground)

run = True
clock = pygame.time.Clock()
while run:
    SCREEN.fill(WHITE)
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.pular()

    all_sprites.draw(SCREEN)
    all_sprites.update()

    pygame.display.flip() # update display
    


pygame.quit()