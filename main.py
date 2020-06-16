import pygame
from os import path
import random
import time
from Lenhador import Tronco
from Lenhador import Player
from Lenhador import Galho
from Lenhador import load_assets
img_dir = path.join(path.dirname(__file__), 'img')
fnt_dir = path.join(path.dirname(__file__), 'font')


WIDTH = 800
HEIGHT = 600

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


VIDA = 10

GALHO_LISTA = [(450, HEIGHT - 120),
               (200, HEIGHT - 270),
               (200, HEIGHT - 420),
               (450, HEIGHT - 570),
               (450, HEIGHT - 720)]

background = pygame.image.load(path.join(img_dir, 'fundo.jpg'))
background = pygame.transform.scale(background, (800, 600))
background_rect = background.get_rect()

imginicio = pygame.image.load(path.join(img_dir, 'Tela de inicio.png'))
imginicio = pygame.transform.scale(imginicio, (800, 600))
imgfundo_rect = imginicio.get_rect()



pygame.init()


assets = load_assets(img_dir, fnt_dir)

score_font = assets["score_font"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Lumberjack")

previous_time = pygame.time.get_ticks()

all_sprites = pygame.sprite.Group()
galho = pygame.sprite.Group()

tronco = Tronco()
player = Player()
all_sprites.add(tronco)
all_sprites.add(player)

font = pygame.font.SysFont("C:\Windows\Fonts\Arial.ttf", 72)
text = font.render("Pontos: {0}".format(player.pontos), True, YELLOW)
textRect = text.get_rect()
textRect.center = (WIDTH // 2 - 300, 50)

for branch in GALHO_LISTA:
    g = Galho(*branch)
    all_sprites.add(g)
    galho.add(g)

try:
    
    running = True
    menu = True

    while menu:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    menu = False

        screen.fill(BLACK)
        screen.blit(imginicio, imgfundo_rect)
        pygame.display.flip()

    while running:

        #clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.pos = 170
                    player.image = pygame.image.load(path.join(img_dir, 'LenhadorD.png')).convert_alpha()

                if event.key == pygame.K_LEFT:
                    player.pos = -220
                    player.image = pygame.image.load(path.join(img_dir, 'LenhadorE.png')).convert_alpha()
                    player.image = pygame.transform.scale(player.image, (120, 120))

                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    
                    player.score = 1
                    text = font.render("Pontos: {0}".format(
                        player.pontos), True, YELLOW)
                    textRect = text.get_rect()
                    textRect.center = (WIDTH // 2 - 300, 50)

                    for branch in galho:
                        branch.rect.y += 100
                        if branch.rect.top >= HEIGHT:
                            branch.kill()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.pos = 0
                    player.image = pygame.image.load(path.join(img_dir, 'LenhadorE.png')).convert_alpha()
                    player.image = pygame.transform.scale(player.image, (120, 120))

                if event.key == pygame.K_RIGHT:
                    player.pos = 0
                    player.image = pygame.image.load(path.join(img_dir, 'LenhadorD.png')).convert_alpha()
                    player.image = pygame.transform.scale(player.image, (120, 120))

        if len(galho) < 4:
            lista_posicao = [200, 450]
            random.shuffle(lista_posicao)
            g = Galho(lista_posicao[0], 40)
            all_sprites.add(g)
            galho.add(g)

        

        if VIDA <= 0:
            running = False

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, galho, False,pygame.sprite.collide_mask)
        if hits:
            VIDA-=1
            print("PONTOS: ", player.pontos-1)
            running = False
            
        

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(text, textRect)
        all_sprites.draw(screen)

        text_surface = score_font.render(chr(9829) * VIDA, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (WIDTH/2-100, HEIGHT - 530)
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()


finally:
    pygame.quit()
