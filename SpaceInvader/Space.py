import pygame
from pygame.locals import *
import sys


pygame.init()

clock = pygame.time.Clock()
pantalla = pygame.display.set_mode((750, 700), 0, 32)#tamaño de la pantalla

pygame.mouse.set_visible(0)

pygame.display.set_caption("Space Innvaders")


fuente = pygame.font.Font(None, 30)
Texto_vidas = fuente.render("Vidas:", 0, (255, 255, 255))
# nave
ship = pygame.image.load("imagenes/nave.png")  # cargamos la imagen

ship_top = pantalla.get_height() - ship.get_height()
ship_left = pantalla.get_width() / 2 - ship.get_width() / 2  # para centrarle a la imagen de la nave

pantalla.blit(ship, (ship_left, ship_top))

# disparo laser
shot = pygame.image.load("imagenes/laser.png")
shoot_y = 0

# fondo
background = pygame.image.load('imagenes/espacio.png').convert()
luna = pygame.image.load("imagenes/superficieLuna.jpg")

#vidas
vidas = pygame.image.load('imagenes/laser.png').convert()

pygame.mixer.music.load("sonido/fondo.mp3")
pygame.mixer.music.play(-1)



while True:
    clock.tick(80)
    pantalla.fill((0, 0, 0))
    pantalla.blit(background, (0, 0))
    pantalla.blit(luna, (0, 600))
    pantalla.blit(vidas, (600, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            shoot_y = 500
            shoot_x = x
            pygame.mixer.music.load("sonido/shoot.wav")
            pygame.mixer.music.play(1)
        if shoot_y > 0:
            pantalla.blit(shot, (shoot_x, shoot_y))
            shoot_y -= 10

    pantalla.blit(Texto_vidas, (500, 10))


    x, y = pygame.mouse.get_pos()  # toma las posiciones segun el mouse

    pantalla.blit(ship, (x - ship.get_width() / 2, ship_top))  # posicion de la nave en el centro

    #cronometro
    Tiempo = pygame.time.get_ticks()/1000
    contador = fuente.render("Tiempo: "+str(Tiempo),0,(255,255,255))
    pantalla.blit(contador,(10,10))

    pygame.display.update()


