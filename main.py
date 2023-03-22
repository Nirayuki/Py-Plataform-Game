import pygame
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

# Variaveis ----------------------------------------------------------------

SCREEN_WIDTH, SCREEN_HEIGTH = 640, 420
FPS = 60
JUMP_FORCE = 10
GRAVITY_FORCE = 10
IS_COLLISION = False

CHOICE_OBSTACULO = choice([0, 1])

main_dir = os.path.dirname(__file__)
img_dir = os.path.join(main_dir, 'Assets')
sound_dir = os.path.join(main_dir, 'Sounds')

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Plataform Game")


# Colors ----------------------------------------------------------------

BLACK = (0, 0, 0)
WHITE = (225, 225, 225)

# Images ----------------------------------------------------------------

SPRITE_SHEET = pygame.image.load(os.path.join(img_dir, 'dinoSpritesheet.png'))

# Sounds ----------------------------------------------------------------

SOUND_COLLISION = pygame.mixer.Sound(os.path.join(sound_dir, 'sons_death_sound.wav'))
SOUND_COLLISION.set_volume(1)

# Class ----------------------------------------------------------------

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Criando um array para segurar todas as imagens para animação
        self.img_dinossauro = []

        self.jump_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'sons_jump_sound.wav'))
        self.jump_sound.set_volume(1)

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

        # Criando mascara para verificar colisão depois
        self.mask = pygame.mask.from_surface(self.image)

        self.postition_y_initial = SCREEN_HEIGTH - 64 - 96//2 # Divido por 96//2 para pegar o ponto 0,0 pq o rect.center pega o pongo central da imagem, já o rect.x pega o ponto 0 do x,y da imagem

        self.rect.center = (100, SCREEN_HEIGTH - 64)

        self.pulo = False

    def pular(self):
        self.pulo = True
        self.jump_sound.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 150:
                self.pulo = False
            self.rect.y -= JUMP_FORCE
        else:
            if self.rect.y < self.postition_y_initial:
                self.rect.y += GRAVITY_FORCE
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
        # Movimentando 10px para esquerda
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
        # Movimentando 10px para esquerda
        self.rect.x -= 10


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

         # Procurando a imagem dentro do SPRITE_SHEET
        self.image = SPRITE_SHEET.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2)) # 64px

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.choice_obs = CHOICE_OBSTACULO

        self.rect.center = (SCREEN_WIDTH, SCREEN_HEIGTH - 64)

        self.rect.x = SCREEN_WIDTH


    def update(self):
        if self.choice_obs == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = SCREEN_WIDTH
            # Movimentando 10px para esquerda
            self.rect.x -= 10

class Fly_Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.img_dino = []

        for i in range(3,5):
            img = SPRITE_SHEET.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.img_dino.append(img)


        self.index = 0
        self.image = self.img_dino[self.index]

        # Essa função indentifica que eu quero criar um retângulo e adicionar a imagem dentro dele básicamente...
        self.rect = self.image.get_rect()

        # Criando mascara para verificar colisão depois
        self.mask = pygame.mask.from_surface(self.image)

        self.choice_obs = CHOICE_OBSTACULO

        self.rect.center = (SCREEN_WIDTH, 250)

        self.rect.x = SCREEN_WIDTH

    def update(self):
        if self.choice_obs == 1:
            if self.index > 1:
                self.index = 0
            self.index += 0.20
            self.image = self.img_dino[int(self.index)]
            if self.rect.topright[0] < 0:
                self.rect.x = SCREEN_WIDTH
            self.rect.x -= 10
# Main ----------------------------------------------------------------


# Criando um grupo de Sprite para poder desenhar e dar update em todos os Itens
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()



# Adicionando o Dino
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
    

# Adicionando Cacto
cacto = Cacto()
all_sprites.add(cacto)
obstaculos.add(cacto)

# Adicionando Fly_Dino
fly_dino = Fly_Dino()
all_sprites.add(fly_dino)
obstaculos.add(fly_dino)

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
                if dino.rect.y != dino.postition_y_initial:
                    pass
                else:
                    dino.pular()

    # Criando colisão com o dino e os obstaculos
    collision = pygame.sprite.spritecollide(dino, obstaculos, False, pygame.sprite.collide_mask) # Adicionando a Flag, tipo de colisão, no meu caso escolhi o mask, mas existe o Rect e Radious

    all_sprites.draw(SCREEN)

    if cacto.rect.topright[0] <= 0 or fly_dino.rect.topright[0] <= 0:
        CHOICE_OBSTACULO = choice([0 , 1])
        cacto.rect.x = SCREEN_WIDTH
        fly_dino.rect.x = SCREEN_WIDTH

        cacto.choice_obs = CHOICE_OBSTACULO
        fly_dino.choice_obs = CHOICE_OBSTACULO

    if collision and IS_COLLISION == False:
        SOUND_COLLISION.play()
        IS_COLLISION = True
    if IS_COLLISION == True:
        pass
    else:
        all_sprites.update()
   
        
    pygame.display.flip() # update display
    


pygame.quit()