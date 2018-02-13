from pygame import *
import sys
from random import shuffle, randrange, choice

#todo     R    G    B
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

SCREEN = display.set_mode((800, 650)) #todo tamaño de nuestra ventana de juego
FONT = "fonts/space_invaders.ttf" #todo tipo de letra
IMG_NAMES = ["ship", "enemy1_1", "enemy1_2", "enemy2_1", "enemy2_2", "enemy3_1", "enemy3_2",
             "explosionblue", "explosiongreen", "explosionpurple", "laser", "enemylaser"] #todo cargamos las imagenes
IMAGES = {name: image.load("images/{}.png".format(name)).convert_alpha()
          for name in IMG_NAMES} #todo llamamos a las imagenes del anterior arreglo y lo convertimos en el formato a decuado


class calseNaveEspacial(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)  #todo inicializamos los sprite
        self.ImagenNave = image.load("imagenes/nave.png")  #todo cargamos la imagen
        self.ImagenNave = transform.scale(self.ImagenNave, (90, 90))  #todo le damos el tamaño de la nave
        self.rect = self.ImagenNave.get_rect(topleft=(375, 540))  #todo nos devolvera un rectangulo de la imagen
        self.speed = 5  #todo velocidad de la nave

    def update(self, keys, *args):
        if keys[K_LEFT] and self.rect.x > 10:#todo damos el limite hasta donde puede llegar la nave
            self.rect.x -= self.speed#todo mov de la nave a la IZQ y velocidad
        if keys[K_RIGHT] and self.rect.x < 740:#todo limite de la derecha
            self.rect.x += self.speed#todo mov de la nave a la derecha
        game.screen.blit(self.ImagenNave, self.rect)


class claseProyectil(sprite.Sprite):
    def __init__(self, xpos, ypos, direction, speed, filename, side): #todo parametros (x, y, velocidad, nomArchivo, tamaño)
        sprite.Sprite.__init__(self)
        self.image = IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))#todo tamaño del rectangulo para la imagen a cargar
        self.speed = speed#todo velocidad del proyectil
        self.direction = direction
        self.side = side
        self.filename = filename

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        print(self.rect.y)
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()


class claseInvasor(sprite.Sprite):
    def __init__(self, row, column):
        sprite.Sprite.__init__(self)

        #todo atributos
        self.row = row
        self.column = column
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.direction = 1
        self.rightMoves = 15
        self.leftMoves = 30
        self.moveNumber = 0
        self.moveTime = 600
        self.firstTime = True
        self.movedY = False;
        self.columns = [False] * 10
        self.aliveColumns = [True] * 10
        self.addRightMoves = False
        self.addLeftMoves = False
        self.numOfRightMoves = 0
        self.numOfLeftMoves = 0
        self.timer = time.get_ticks()

    def update(self, keys, currentTime):

        if currentTime - self.timer > self.moveTime:
            self.movedY = False;
            #todo mov en x (der) y baja
            if self.moveNumber >= self.rightMoves and self.direction == 1:
                self.direction *= -1
                self.moveNumber = 0
                self.rect.y += 35
                self.movedY = True
                if self.addRightMoves:
                    self.rightMoves += self.numOfRightMoves
                if self.firstTime:
                    self.rightMoves = self.leftMoves;
                    self.firstTime = False;
                self.addRightMovesAfterDrop = False
            #todo mov en x (izq) controla que baje(-1)
            if self.moveNumber >= self.leftMoves and self.direction == -1:
                self.direction *= -1
                self.moveNumber = 0
                self.rect.y += 35
                self.movedY = True
                if self.addLeftMoves:
                    self.leftMoves += self.numOfLeftMoves
                self.addLeftMovesAfterDrop = False
            #todo mov en x para que empiece el movimiento
            if self.moveNumber < self.rightMoves and self.direction == 1 and not self.movedY:
                self.rect.x += 10
                self.moveNumber += 1
            #todo cuando llega al tope de mov en x (der)y baja(-1)
            if self.moveNumber < self.leftMoves and self.direction == -1 and not self.movedY:
                self.rect.x -= 10
                self.moveNumber += 1

            self.index += 1
            #todo controla la lista de los invasores para cargar y no se desvorde
            if self.index >= len(self.images):
                self.index = 0#todo controla que no se desvorde las imagenes de la lista

            #todo controla la velocidad en que bajan los invasores
            self.image = self.images[self.index]

            self.timer += self.moveTime
        game.screen.blit(self.image, self.rect)



    def load_images(self):
        images = {0: ["1_2", "1_1"],
                  1: ["2_2", "2_1"],
                  2: ["2_2", "2_1"],
                  3: ["3_1", "3_2"],
                  4: ["3_1", "3_2"],
                  }
        img1, img2 = (IMAGES["enemy{}".format(img_num)] for img_num in images[self.row])
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))


class Explosion(sprite.Sprite):
    def __init__(self, xpos, ypos, row, ship):
        sprite.Sprite.__init__(self)
        self.isShip = ship
        if ship:
            self.ImagenNave = image.load("imagenes/nave.png")  #todo cargamos la imagen
            self.ImagenNave = transform.scale(self.ImagenNave, (80, 80))  #todo le damos el tamaño de la nave
            self.rect = self.ImagenNave.get_rect(topleft=(xpos, ypos))

        else:#todo efecto de la explosion del invasor
            self.row = row
            self.load_image()
            self.image = transform.scale(self.image, (40, 35)) #todo escala del laser
            self.rect = self.image.get_rect(topleft=(xpos, ypos))
            game.screen.blit(self.image, self.rect)

        self.timer = time.get_ticks()

    def update(self, keys, tiempoActual):
        if self.isShip:
            if tiempoActual - self.timer > 300 and tiempoActual - self.timer <= 600:
                game.screen.blit(self.ImagenNave, self.rect)
            if tiempoActual - self.timer > 900:
                self.kill()  #todo remueve el sprite del grupo
        else: #todo el tiempo que le toma en desaparecer el efecto de explosion del invasor
            if tiempoActual - self.timer <= 100:
                game.screen.blit(self.image, self.rect)
            if tiempoActual - self.timer > 100 and tiempoActual - self.timer <= 200:
                self.image = transform.scale(self.image, (50, 45))
                game.screen.blit(self.image, (self.rect.x - 6, self.rect.y - 6))
            if tiempoActual - self.timer > 400:
                self.kill()  #todo remueve el sprite del grupo

    # todo metodo para cargar la imagen del invasor cuando explota
    def load_image(self):
        imgColors = ["purple", "blue", "blue", "green", "green"]
        self.image = IMAGES["explosion{}".format(imgColors[self.row])]


class claseVida(sprite.Sprite):
    def __init__(self, xpos, ypos):
        sprite.Sprite.__init__(self)
        self.image = IMAGES["ship"]
        self.image = transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)


class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class SpaceInvaders(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 512)
        init()
        self.caption = display.set_caption('Space Invaders')
        self.screen = SCREEN
        self.background = image.load('imagenes/espacio.png').convert()
        self.startGame = False
        self.mainScreen = True  #todo  verdadero para que desaparesca de la pantalla
        self.gameOver = False
        self.enemyPositionDefault = 65  #todo  inicial valores para un nuevo juego
        self.enemyPositionStart = self.enemyPositionDefault  # todo Contador para la posición inicial enemiga (aumentado cada nueva ronda)
        self.enemyPosition = self.enemyPositionStart  # todo Posición de partida enemiga actual

    def reset(self, score, lives, newGame=False):
        self.player = calseNaveEspacial()
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.enemyBullets = sprite.Group()
        self.reset_lives(lives)
        self.enemyPosition = self.enemyPositionStart
        self.make_enemies()
        # todo Solo crea bloqueadores en un juego nuevo, no en una nueva ronda
        if newGame:
            self.keys = key.get_pressed()
            self.clock = time.Clock()
            self.timer = time.get_ticks()
            self.noteTimer = time.get_ticks()
            self.shipTimer = time.get_ticks()
            self.score = score
            self.lives = lives
            self.create_audio()
            self.create_text()
            self.killedRow = -1
            # self.killedColumn = -1
            self.makeNewShip = False
            self.shipAlive = True
            # self.killedArray = [[0] * 10 for x in range(5)]

    def reset_lives_sprites(self):
        self.life1 = claseVida(715, 3)
        self.life2 = claseVida(742, 3)
        self.life3 = claseVida(769, 3)

        if self.lives == 3:
            self.livesGroup = sprite.Group(self.life1, self.life2, self.life3)
        elif self.lives == 2:
            self.livesGroup = sprite.Group(self.life1, self.life2)
        elif self.lives == 1:
            self.livesGroup = sprite.Group(self.life1)

    def reset_lives(self, lives):
        self.lives = lives
        self.reset_lives_sprites()

    def create_audio(self):
        self.sounds = {}
        for sound_name in ["shoot", "shoot2", "invaderkilled", "shipexplosion"]:
            self.sounds[sound_name] = mixer.Sound("sounds/{}.wav".format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound("sounds/{}.wav".format(i)) for i in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0

    def play_main_music(self, currentTime):
        moveTime = self.enemies.sprites()[0].moveTime
        if currentTime - self.noteTimer > moveTime:
            self.note = self.musicNotes[self.noteIndex]
            if self.noteIndex < 3:
                self.noteIndex += 1
            else:
                self.noteIndex = 0

            self.note.play()
            self.noteTimer += moveTime

    def create_text(self):

        self.titulo_programacion = Text(FONT, 40, "PROGRAMACION   AVANZADA", BLUE, 40, 40)  # X,Y
        self.titulo_autores1 = Text(FONT, 20, "BY: IZA JORGE", BLUE, 550, 500)
        self.titulo_autores2 = Text(FONT, 20, "TIPAN JENNY", BLUE, 590, 540)
        self.titulo_autores3 = Text(FONT, 20, "CORO ANDRES", BLUE, 590, 580)
        self.titulo_SpaceInvader = Text(FONT, 60, "Space  Invaders", YELLOW, 140, 200)
        self.titulo_pres_tecla = Text(FONT, 25, "Press  any  key  to  continue", GREEN, 201, 350)
        self.titulo_boton_inicio = Text(FONT, 25, "Star Game:", RED, 200, 410)
        self.titulo_boton_salir = Text(FONT, 25, "Exit:", RED, 300, 510)
        self.gameOverText = Text(FONT, 50, "Game Over", WHITE, 250, 270)
        self.nextRoundText = Text(FONT, 50, "Next Round", WHITE, 240, 280)
        self.scoreText = Text(FONT, 20, "Score", WHITE, 5, 5)
        self.livesText = Text(FONT, 20, "Lives ", WHITE, 640, 5)

    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0 and self.shipAlive:
                        if self.score < 500: #todo disparos con un solo laser si el score es menor a 500 pts
                            bullet = claseProyectil(self.player.rect.x + 23, self.player.rect.y + 5, -1, 15, "laser","center")
                            self.bullets.add(bullet)
                            self.allSprites.add(self.bullets)
                            self.sounds["shoot"].play()
                        else: #todo doble laser cuando el score pasa los 500 pts
                            leftbullet = claseProyectil(self.player.rect.x + 8, self.player.rect.y + 5, -1, 15, "laser",
                                                        "left")
                            rightbullet = claseProyectil(self.player.rect.x + 38, self.player.rect.y + 5, -1, 15,
                                                         "laser", "right")
                            self.bullets.add(leftbullet)
                            self.bullets.add(rightbullet)
                            self.allSprites.add(self.bullets)
                            self.sounds["shoot2"].play()

    def make_enemies(self):
        enemies = sprite.Group()
        for row in range(5):
            for column in range(10):
                enemy = claseInvasor(row, column)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = self.enemyPosition + (row * 45)
                enemies.add(enemy)

        self.enemies = enemies
        self.allSprites = sprite.Group(self.player, self.enemies, self.livesGroup)

    def make_enemies_shoot(self):
        columnList = []
        for enemy in self.enemies:
            columnList.append(enemy.column)

        columnSet = set(columnList)
        columnList = list(columnSet)
        shuffle(columnList)
        column = columnList[0]
        enemyList = []
        rowList = []

        for enemy in self.enemies:
            if enemy.column == column:
                rowList.append(enemy.row)
        row = max(rowList)
        for enemy in self.enemies:
            if enemy.column == column and enemy.row == row:
                if (time.get_ticks() - self.timer) > 700:
                    self.enemyBullets.add(
                        claseProyectil(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5, "enemylaser", "center"))
                    self.allSprites.add(self.enemyBullets)
                    self.timer = time.get_ticks()

    def calculate_score(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        score = scores[row]
        self.score += score
        return score

    def create_main_menu(self):
        self.ImagenEpn = image.load("imagenes/escudoEpn.png")  #todo cargamos la imagen
        self.ImagenEpn = transform.scale(self.ImagenEpn, (150, 150))  #todo  le damos el tamaño de la nave
        self.ImagenBoton = image.load("imagenes/navePintada.png")
        self.ImagenBoton = transform.scale(self.ImagenBoton, (50, 50))  #todo  para cambiar la escal de la imagen

        self.screen.blit(self.ImagenEpn, (650, 20))  # todo crea el espacio para la imagen
        self.screen.blit(self.ImagenBoton, (400, 400))  #todo  boton star
        self.screen.blit(self.ImagenBoton, (400, 500))

        # evento del mouse clic
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                print("evento mouse X" + str(x) + " y: " + str(y))
                if (x >= 400 and x <= 440 and y >= 400 and y <= 440):
                    self.startGame = True
                    self.mainScreen = False
                if (x >= 400 and x <= 440 and y >= 500 and y <= 540):
                    sys.exit()

    def check_collisions(self):
        # todo detecta la colision entre laser
        colicion_entre_laser = sprite.groupcollide(self.bullets, self.enemyBullets, True, False)
        if colicion_entre_laser:
            for value in colicion_entre_laser.values():
                for currentSprite in value:
                    self.enemyBullets.remove(currentSprite)
                    self.allSprites.remove(currentSprite)

                # todo detecta si nuestra nave le llego al invasor con el laser
        enemigo_destruido_laser = sprite.groupcollide(self.bullets, self.enemies, True, False)
        if enemigo_destruido_laser:
            for value in enemigo_destruido_laser.values():
                for currentSprite in value:
                    self.sounds["invaderkilled"].play()
                    self.killedRow = currentSprite.row #todo detecta cual invasor fue matado(fila)
                    self.killedColumn = currentSprite.column#todo detecta cual invasor fue matado(columna)
                    score = self.calculate_score(currentSprite.row)
                    explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.row, False)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(currentSprite)
                    self.enemies.remove(currentSprite)
                    self.gameTimer = time.get_ticks()
                    break


                # todo detecta si el invasor nos disparo a la nave
        nave_destruida_laser = sprite.groupcollide(self.enemyBullets, self.playerGroup, True, False)
        if nave_destruida_laser:
            for value in nave_destruida_laser.values():
                for playerShip in value:
                    if self.lives == 3:
                        self.lives -= 1
                        self.livesGroup.remove(self.life3)
                        self.allSprites.remove(self.life3)
                    elif self.lives == 2:
                        self.lives -= 1
                        self.livesGroup.remove(self.life2)
                        self.allSprites.remove(self.life2)
                    elif self.lives == 1:
                        self.lives -= 1
                        self.livesGroup.remove(self.life1)
                        self.allSprites.remove(self.life1)
                    elif self.lives == 0:
                        self.gameOver = True
                        self.startGame = False
                    self.sounds["shipexplosion"].play()
                    explosion = Explosion(playerShip.rect.x, playerShip.rect.y, 0, True)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(playerShip)
                    self.playerGroup.remove(playerShip)
                    self.makeNewShip = True
                    self.shipTimer = time.get_ticks()
                    self.shipAlive = False

        #todo  detecta si los invasores nos topa ala nave fin del juego
        if sprite.groupcollide(self.enemies, self.playerGroup, True, True):
            self.gameOver = True
            self.startGame = False

    # todo fin del metodo de detectar la colision

    def create_new_ship(self, createShip, currentTime):
        if createShip and (
                currentTime - self.shipTimer > 900):  # todo da el tiempo para cargar a la nueva nave efecto de explosion nave
            self.player = calseNaveEspacial()  # todo carga nueva nave despues de la explosion cuando me disparan
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.makeNewShip = False
            self.shipAlive = True

    def create_game_over(self, currentTime):
        self.screen.blit(self.background, (0, 0))
        if currentTime - self.timer < 2999:  #todo para el mensaje de game over
            print(self.timer)
            self.gameOverText.draw(self.screen)

            self.titulo_puntaje = Text(FONT, 40, "PUNTAJE:", BLUE, 200, 500)  # todo escribe el texto puntaje
            self.titulo_puntaje.draw(self.screen) #todo dibuja puntaje en la pantalla el titulo puntaje
            self.texto_puntaje = Text(FONT, 50, str(self.score), GREEN, 500, 500)  # todo imprime el puntaje
            self.texto_puntaje.draw(self.screen)#todo escribe en la pantalla el puntaje

            self.titulo_tiempoT = Text(FONT, 40, "TIEMPO:", BLUE, 200, 400)  # X,Y
            self.titulo_tiempoT.draw(self.screen)
            self.texto_tiempoT = Text(FONT, 50, str(self.timer/1000), GREEN, 500, 400)  # todo imprime el TIEMPO TOTAL DEL JUEGO
            self.texto_tiempoT.draw(self.screen)

        if currentTime - self.timer > 3000:  # todo para que se reinicie el main principal
            self.mainScreen = True

        for e in event.get():
            if e.type == QUIT:
                sys.exit()

    def main(self):
        while True:
            if self.mainScreen:
                self.reset(0, 3, True)
                self.screen.blit(self.background, (0, 0))
                # todo iniciar todos los titulos del menu principal
                self.titulo_programacion.draw(self.screen)
                self.titulo_SpaceInvader.draw(self.screen)
                self.titulo_pres_tecla.draw(self.screen)
                self.titulo_autores1.draw(self.screen)
                self.titulo_autores2.draw(self.screen)
                self.titulo_autores3.draw(self.screen)
                self.titulo_boton_inicio.draw(self.screen)
                self.titulo_boton_salir.draw(self.screen)

                self.create_main_menu()

            elif self.startGame:
                if len(self.enemies) == 0:
                    currentTime = time.get_ticks()
                    if currentTime - self.gameTimer < 3000:
                        self.screen.blit(self.background, (0, 0))
                        self.scoreText2 = Text(FONT, 20, str(self.score), GREEN, 85, 5)  # todo imprime el puntaje
                        self.scoreText.draw(self.screen)
                        self.scoreText2.draw(self.screen)
                        self.nextRoundText.draw(self.screen)
                        self.check_input()

                    if currentTime - self.gameTimer > 3000:
                        # Move enemies closer to bottom
                        self.enemyPositionStart += 35
                        self.reset(self.score, self.lives)  # todo resetea el puntaje
                        self.make_enemies()
                        self.gameTimer += 3000
                else:
                    #todo imprime en la pantalla de juego
                    currentTime = time.get_ticks()
                    self.play_main_music(currentTime)
                    self.screen.blit(self.background, (0, 0))
                    #todo cronometro
                    self.Tiempo = time.get_ticks() / 1000
                    self.texto_tiempoT = Text(FONT, 20,"TIME:  "+ str(self.Tiempo), YELLOW, 350, 20)
                    self.texto_tiempoT.draw(self.screen)
                    #todo fin del cronometro
                    self.scoreText2 = Text(FONT, 20, str(self.score), GREEN, 85, 5)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    self.livesText.draw(self.screen)
                    self.check_input()
                    self.allSprites.update(self.keys, currentTime)
                    self.explosionsGroup.update(self.keys, currentTime)
                    self.check_collisions()
                    self.create_new_ship(self.makeNewShip, currentTime)


                    if len(self.enemies) > 0:
                        self.make_enemies_shoot()

            elif self.gameOver:
                currentTime = time.get_ticks()
                # todo resetiar al enemigo empiece en la posicion
                self.enemyPositionStart = self.enemyPositionDefault
                self.create_game_over(currentTime)


            display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()