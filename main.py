import os
import random
import pygame
from pygame import mixer
import math

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# titulo e icono
pygame.display.set_caption("Space Adventure")

# ruta de la imagen icono
ruta_carpeta = os.path.dirname(os.path.abspath(__file__))
subcarpeta = "images"
ruta_icono = os.path.join(ruta_carpeta, subcarpeta, "astronave.png")
ruta_fondo = os.path.join(ruta_carpeta, subcarpeta, "fondo.jpg")
fondo = pygame.image.load(ruta_fondo)

# icono
icono = pygame.image.load(ruta_icono)
pygame.display.set_icon(icono)

# agregar musica
ruta_musica_fondo = os.path.join(
    "C:/Users/santiago/Desktop/proyectos web/Python/Dia 10/sonidos", "MusicaFondo.mp3")
ruta_musica_disparo = os.path.join(
    "C:/Users/santiago/Desktop/proyectos web/Python/Dia 10/sonidos", "disparo.mp3")
ruta_musica_golpe = os.path.join(
    "C:/Users/santiago/Desktop/proyectos web/Python/Dia 10/sonidos", "Golpe.mp3")
mixer.init()
mixer.music.load(ruta_musica_fondo)
mixer.music.set_volume(0.3)
mixer.music.play(-1)


# variable Nave
ruta_nave = os.path.join(ruta_carpeta, subcarpeta, "transbordador.png")
img_nave = pygame.image.load(ruta_nave)
nave_x = 368
nave_y = 500
nave_x_cambio = 0

# variables enemigo
ruta_enemigo = os.path.join(ruta_carpeta, subcarpeta, "enemigo.png")
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load(ruta_enemigo))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# variables de las balas
ruta_balas = os.path.join(ruta_carpeta, subcarpeta, "bala.png")
img_balas = pygame.image.load(ruta_balas)
balas_x = 0
balas_y = 500
balas_x_cambio = 0
balas_y_cambio = 3
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)


def texto_final():
    mi_fuente_final = fuente_final.render(
        "JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (180, 200))

# Funcion mostrar puntaje


def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# funcion nave
def nave(x, y):
    pantalla.blit(img_nave, (x, y))


# funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion disparar
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_balas, (x + 16, y + 10))


# Funcion colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# loop del juego
se_ejecuta = True
while se_ejecuta:

    # imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # iterar eventos
    for evento in pygame.event.get():
        # evento cerrar pantalla
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # evento precionar teclas
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_LEFT:
                nave_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                nave_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound(ruta_musica_disparo)
                sonido_bala.play()
                if not bala_visible:
                    balas_x = nave_x
                    disparar_bala(balas_x, balas_y)

        # evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                nave_x_cambio = 0

    # modificar ubicacion de la nave
    nave_x += nave_x_cambio

    # mantener dentro de los bordes a la nave
    if nave_x <= 0:
        nave_x = 0
    elif nave_x >= 736:
        nave_x = 736

     # modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin de juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # mantener dentro de los bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], balas_x, balas_y)
        if colision:
            sonido_colision = mixer.Sound(ruta_musica_golpe)
            mixer.music.set_volume(0.1)
            sonido_colision.play()
            balas_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    if balas_y <= -64:
        balas_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(balas_x, balas_y)
        balas_y -= balas_y_cambio

    nave(nave_x, nave_y)

    mostrar_puntaje(texto_x, texto_y)

    # actualizar
    pygame.display.update()
