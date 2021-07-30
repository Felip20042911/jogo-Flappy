from typing import NewType
import pygame, random
from pygame.locals import *

largura_tela = 400
altura_tela = 700


velocidade_game = 10
velocidade = 10
gravidade = 1


altura_chao = 100 
largura_chao = largura_tela * 2


altura_cano = 500
largura_cano = 80
diferença_cano = 150



class passaro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagens = [
            pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\bluebird-upflap.png').convert_alpha(),
            pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\bluebird-midflap.png').convert_alpha(),
            pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\bluebird-downflap.png').convert_alpha()
        ]

        self.imagem_inicial = 0
        self.image = pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\bluebird-upflap.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = largura_tela / 2
        self.rect[1] = altura_tela / 2
        self.speed = velocidade
        

    def update(self):
        self.imagem_inicial = (self.imagem_inicial + 1) % 3
        self.image = self.imagens[ self.imagem_inicial ]

        #update da altura
        self.speed += gravidade

        self.rect[1] += self.speed



    def pulo(self): 
        self.speed = -velocidade



class chao(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (largura_chao, altura_chao))
        
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] =  xpos
        self.rect[1] = altura_tela - altura_chao


    def update(self):
        self.rect[0] -= velocidade_game


class cano(pygame.sprite.Sprite):
    def __init__(self, inverso, xpos, ytamanho):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (largura_cano, altura_cano))


        self.rect = self.image.get_rect()
        self.rect[0] = xpos


        if inverso:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ytamanho)    

        else:
            self.rect[1] = altura_tela - ytamanho

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= velocidade_game


def criar_canos(xpos):
    tamanho = random.randint(150, 400)
    pipe = cano(False, xpos, tamanho)
    pipe_invertido = cano(True, xpos, altura_tela - tamanho - diferença_cano)
    return(pipe, pipe_invertido)


def fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])



pygame.init()

tela = pygame.display.set_mode((largura_tela, altura_tela))

pygame.display.set_caption('Flappy Bird')


#back ground
back_ground = pygame.image.load(r'C:\Users\FELIPE\Documents\GitHub\Projetos\jogo\background-day.png')
back_ground = pygame.transform.scale(back_ground, (largura_tela, altura_tela))

clock = pygame.time.Clock()


#bird
bird_group = pygame.sprite.Group()
bird = passaro()
bird_group.add(bird)


#chão
ground_group = pygame.sprite.Group()
for i in range(2):
    ground = chao(largura_tela * i)
    ground_group.add(ground) 


#pipe
pipe_group = pygame.sprite.Group()
for i in range(2):
    canos = criar_canos(largura_tela * i + 750)
    
    pipe_group.add(canos[0])
    pipe_group.add(canos[1])



while True:
    clock.tick(30)
    for event in pygame.event.get():


        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.pulo() 


    tela.blit(back_ground, (0, 0))


    if fora_da_tela(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground =  chao(largura_chao - 410)
        ground_group.add(new_ground) 

    if fora_da_tela(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        new_pipe = criar_canos(largura_tela * 2)
    
        pipe_group.add(new_pipe[0])
        pipe_group.add(new_pipe[1])



    bird_group.update()
    ground_group.update()
    pipe_group.update()
    
    
    
    bird_group.draw(tela)
    pipe_group.draw(tela)
    ground_group.draw(tela) 

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or 
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        #GAME OVER
        break

    pygame.display.update()



pygame.quit()
