import numpy as np
import pygame
from tractament_imatges import img_to_3d_points
from clientUser import *


PORT=3389
IP='34.172.166.240'


# Creem la classe SpriteObject, la qual s'utilitza durant tota l'aplicació per tal de visualitzar i interactuar amb
# els punts que es visualitzaran, ja siguin els punts 3D donats per l'algorisme SIFT implementat durant l'assignatura
# de Visió per Computador com els punts dibuixats pel cirurgià.
class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, sprite_x, sprite_y, color, surf=5):
        super().__init__()
        self.surf = surf
        self.original_image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, color, (2.5, 2.5), 2)
        self.hover_image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.hover_image, color, (2.5, 2.5), 2)
        pygame.draw.circle(self.hover_image, (0, 255, 255), (2.5, 2.5), 2, 4)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(sprite_x, sprite_y))
        self.hover = False
        self.inLine = False  # Posem a True si està a la línia actual pintada. Posar a False en cas que es cliqui
        # el botó d'esborrar línia actual.
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        # self.hover = self.rect.collidepoint(mouse_pos)
        self.hover = self.rect.collidepoint(mouse_pos) and any(mouse_buttons)
        self.image = self.hover_image if self.hover else self.original_image

    def select(self):
        self.inLine = True

    def unselect(self):
        self.inLine = False

    def die(self, x, y):
        for lastLineDot in lineToDraw:
            if lastLineDot.rect.x == x and lastLineDot.rect.y == y:
                lineToDraw.remove(lastLineDot)


def convert_to_2d(point=[0, 0, 0]):
    return [point[0] * (point[2] * .3), point[1] * (point[2] * .3)]


pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MultiArm")
clock = pygame.time.Clock()

sprite_object = SpriteObject(*screen.get_rect().center, (128, 128, 0))

# TODO. Inicialitzar variables:
map3dDots = pygame.sprite.Group()
entireDrawLinePointsList = []
drawLinePoints = []  # Aqui guardarem la llista de punts per dibuixar
lineToDraw = pygame.sprite.Group()

pointsSent = pygame.sprite.Group()
pointsSentList = []

"""Check stillCounting and mouseClickTimer functionality.
IDEA: When a dot (mapDot) is clicked, we select it and add to the lineToDraw group.
If we click it again, we should be able to erease it and unselect the mapDot (mapDot.unselect()) to be able to
 select again later. Some time should be given between actions."""
stillCounting = False
mouseClickTimer = 0
buttonDown = False
timerDown = 0

saveCurrentLine = False
cameraUsed = False

# PALETA DE COLORS:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)

# Carregar imatges dels botons.
image1 = pygame.image.load("img/app/bisturi.png")
image2 = pygame.image.load("img/app/rotulador.png")
image3 = pygame.image.load("img/app/apagar.png")


# Función para mostrar texto en un botón
def draw_button_text(text, x, y):
    font = pygame.font.SysFont(None, 24)
    button_text = font.render(text, True, BLACK)
    button_rect = button_text.get_rect()
    button_rect.center = (x, y)
    screen.blit(button_text, button_rect)

def reset(map3dDots, entireDrawLinePointsList, drawLinePoints, lineToDraw, pointsSent, pointsSentList):
    # map3dDots.empty()  # Treure si no volem fer el reset de càmera
    lineToDraw.empty()
    pointsSent.empty()

    entireDrawLinePointsList = []  # Treure si no volem fer el reset de càmera.
    drawLinePoints = []  # Aqui guardarem la llista de punts per dibuixar
    pointsSentList = []
    return map3dDots, entireDrawLinePointsList, drawLinePoints, lineToDraw, pointsSent, pointsSentList


def realitzar_fotos(map3dDotsList, conn=False):
    if not conn:
        pts3d = img_to_3d_points()
    else:
        pts3d = np.array(map3dDotsList)
    pts3d += 2
    pts3d *= 10
    map3dDots.empty()
    for pt in pts3d:
        pt2d = convert_to_2d([pt[0], pt[1], pt[2]])
        # dot = SpriteObject(screen.get_width() // 3, screen.get_height() // 3, (255, 0, 0))
        dot = SpriteObject(pt2d[0], pt2d[1], (255, 0, 0))
        map3dDots.add(dot)
    return map3dDots


connected = True
try:
    socket_conn = connectionSocket(IP, PORT)
except ConnectionRefusedError:
    connected = False
# ===================================================
#                    MAIN LOOP
# ===================================================

run = True
while run:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # Dibuixar botons d'imatges.
    screen.blit(image1, (screen_width - 100, screen_height - 150))
    screen.blit(image2, (screen_width - 100, screen_height - 250))
    screen.blit(image3, (screen_width - 100, screen_height - 350))  # Apagar

    # Dibuixar botons de text.
    pygame.draw.rect(screen, RED, (screen_width - 150, screen_height - 450, 120, 40))  # Eliminar últim.
    pygame.draw.rect(screen, RED, (screen_width - 150, screen_height - 550, 120, 40))  # Enviar
    pygame.draw.rect(screen, RED, (screen_width - 150, screen_height - 650, 120, 40))  # Reset
    if not cameraUsed:
        pygame.draw.rect(screen, RED, (screen_width - 150, screen_height - 750, 120, 40))  # Càmera

    # Mostrar texto en los botones de texto
    draw_button_text("Eliminar últim", screen_width - 90, screen_height - 430)
    draw_button_text("Enviar", screen_width - 90, screen_height - 530)
    draw_button_text("Reset", screen_width - 90, screen_height - 630)
    if not cameraUsed:
        draw_button_text("Càmera", screen_width - 90, screen_height - 730)  # Càmera

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttonDown = True
            mouse_pos = pygame.mouse.get_pos()
            # Comprovar si s'ha fet clic en el primer botó d'imatge.
            if screen_width - 100 <= mouse_pos[0] <= screen_width - 50 and screen_height - 150 <= mouse_pos[
                1] <= screen_height - 100:
                print("Primer botó clicat --> Seleccionar el bisturí.")
                # Enviar al ROBOT ordre de canviar capçal
                if connected:
                    communicationClient(socket_conn, "TOOLCHG")
            # Comprovar si s'ha fet clic en el segon botó d'imatge.
            elif screen_width - 100 <= mouse_pos[0] <= screen_width - 50 and screen_height - 250 <= mouse_pos[
                1] <= screen_height - 200:
                print("Segon botó clicat --> Seleccionar el rotulador.")
                # Enviar al ROBOT ordre de canviar capçal
                if connected:
                    communicationClient(socket_conn, "TOOLCHG")
            elif screen_width - 100 <= mouse_pos[0] <= screen_width - 50 and screen_height - 350 <= mouse_pos[
                1] <= screen_height - 300:
                print("Tercer botó clicat --> Apagar")
                # Enviar al ROBOT senyal per apagar-se i apagar també l'app
                if connected:
                    communicationClient(socket_conn, "TURN_OFF")
                run = False
            # Comprovar si s'ha fet clic en el primer botó de text.
            # TODO. ELIMINAR ÚLTIM TRAÇ
            elif screen_width - 150 <= mouse_pos[0] <= screen_width - 30 and screen_height - 450 <= mouse_pos[
                1] <= screen_height - 410:
                print("Eliminant l'últim traç . . .")
                if len(entireDrawLinePointsList) >= 1:
                    toDelete = entireDrawLinePointsList[-1]
                    for elem in toDelete:
                        elem[1].kill()
                    entireDrawLinePointsList.pop()
            # Comprovar si s'ha fet clic en el segon botó de text.
            # TODO. ENVIAR PUNTS . . .
            elif screen_width - 150 <= mouse_pos[0] <= screen_width - 30 and screen_height - 550 <= mouse_pos[
                1] <= screen_height - 510:
                print("Enviant punts al robot . . .")
                toSend = entireDrawLinePointsList[-1]
                # pointsSentList.append(toSend)
                for elem in toSend:
                    obj = SpriteObject(elem[0][0], elem[0][1], ORANGE)
                    pointsSent.add(obj)
                    elem[1].kill()
                    elem[1] = obj
                    pointsSentList.append(elem)

                # Enviar els punts al ROBOT
                if connected:
                    communicationClient(socket_conn, "MOVE", pointsSentList)

            # Comprovar si s'ha fet clic en el tercer botó de text.
            # TODO. RESET
            elif screen_width - 150 <= mouse_pos[0] <= screen_width - 30 and screen_height - 650 <= mouse_pos[
                1] <= screen_height - 610:
                print("WIP, podria fer un reset, borrant tot menys el núvol de punts.")
                map3dDots, entireDrawLinePointsList, drawLinePoints, lineToDraw, pointsSent, pointsSentList = reset(
                    map3dDots, entireDrawLinePointsList, drawLinePoints, lineToDraw, pointsSent, pointsSentList)
            # TODO. CÀMERA
            elif screen_width - 150 <= mouse_pos[0] <= screen_width - 30 and screen_height - 750 <= mouse_pos[
                1] <= screen_height - 710 and not cameraUsed:
                cameraUsed = True
                # Enviar els punts al ROBOT
                if connected:
                    map3dDotsList = communicationClient(socket_conn, "PHOTO")
                    map3dDots = realitzar_fotos(map3dDotsList, connected)

                map3dDots = realitzar_fotos(map3dDots, connected)

        elif event.type == pygame.MOUSEBUTTONUP:
            buttonDown = False

    if buttonDown and timerDown <= 0:
        timerDown = 10
        lineDot = SpriteObject(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], (0, 0, 0))
        drawLinePoints.append([(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), lineDot])
        lineToDraw.add(lineDot)

    if not buttonDown:
        if len(drawLinePoints) == 1:
            last_sprite = lineToDraw.sprites()[-1]
            last_sprite.kill()
            drawLinePoints = []
        elif len(drawLinePoints) > 1:
            entireDrawLinePointsList.append(drawLinePoints)
            drawLinePoints = []
            print("Guardat!! Len entireDrawLinePointsList: ", len(entireDrawLinePointsList))

    if timerDown >= 0:
        timerDown -= 1
        # print(timerDown)

    if mouseClickTimer >= 0:
        mouseClickTimer -= 1  # Timer en el qual comptarem

    map3dDots.draw(screen)  # Dibuixar els punts del mapa de punts 3D.
    lineToDraw.draw(screen)  # Dibuixar els punts seleccionats com a lineToDraw.
    pointsSent.draw(screen)  # Dibuixar els punts que ja s'han enviat.
    # Dibuixar totes les línies ja guardades:
    for traçada in entireDrawLinePointsList:
        for i in range(len(traçada) - 1):
            x_ini_tra = traçada[i][0][0]
            y_ini_tra = traçada[i][0][1]
            x_fin_tra = traçada[i + 1][0][0]
            y_fin_tra = traçada[i + 1][0][1]
            pygame.draw.line(screen, (0, 255, 0), (x_ini_tra, y_ini_tra), (x_fin_tra, y_fin_tra), 2)

    # Dibuixar la línia o traçada actual
    for i in range(len(drawLinePoints) - 1):
        x_ini_act = drawLinePoints[i][0][0]
        y_ini_act = drawLinePoints[i][0][1]
        x_fin_act = drawLinePoints[i + 1][0][0]
        y_fin_act = drawLinePoints[i + 1][0][1]
        pygame.draw.line(screen, (0, 0, 0), (x_ini_act, y_ini_act), (x_fin_act, y_fin_act), 2)

    for i, item in enumerate(pointsSentList):
        if i < len(pointsSentList) - 1:
            next_item = pointsSentList[i + 1]
        else:
            # next_item = None
            break
        x_ini_sent = item[0][0]
        y_ini_sent = item[0][1]
        x_fin_sent = next_item[0][0]
        y_fin_sent = next_item[0][1]
        pygame.draw.line(screen, ORANGE, (x_ini_sent, y_ini_sent), (x_fin_sent, y_fin_sent), 2)

    pygame.display.flip()  # Per només actualitzar una part de la pantalla en comptes de tota cada vegada.

pygame.quit()
exit()


"""
def main_loop():
    run = True
    while run:
        clock.tick(60)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSE BUTTON DOWN DETECTED")
                # buttonDown = True
                mouseClickTimer = 5
                stillCounting = True
            elif event.type == pygame.MOUSEBUTTONUP and len(drawLinePoints) > 1:
                saveCurrentLine = True
                # sleep(0.2)  # Sleep per evitar que al realitzar una nova traçada, el primer punt s'enllaci amb l'últim de
                # l'anterior.
            elif pygame.mouse.get_pressed()[0]:
                try:
                    buttonDown = True
                except AttributeError:
                    pass

        map3dDots.update()
        for mapDot in map3dDots:
            if mapDot.hover and mapDot.inLine and mouseClickTimer > 0:
                mapDot.unselect()
                print("mapDot UNSELECTED")
            elif mapDot.hover and not mapDot.inLine and mouseClickTimer <= 0:
                print("mapDot.hover detected AFTER update")
                print("Pos: ", mapDot.rect)
                print("Before mapDot.inLine: ", mapDot.inLine)
                mapDot.select()
                print("AFTER mapDot.inLine: ", mapDot.inLine)
                print("Pos --> (x, y) = (", mapDot.rect[0], ", ", mapDot.rect[1], ").")
                drawLinePoints.append((mapDot.rect[0], mapDot.rect[1]))
                lineDot = SpriteObject(mapDot.rect[0] + 2.25, mapDot.rect[1] + 2.25, (0, 0, 0))
                lineToDraw.add(lineDot)
            elif buttonDown and timerDown <= 0:
                print("Pos Ratolí --> (x, y) = (", mapDot.rect[0], ", ", mapDot.rect[1], ").")
                drawLinePoints.append((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                lineDot = SpriteObject(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], (0, 0, 0))
                lineToDraw.add(lineDot)
                buttonDown = False
                timerDown = 5
        if timerDown >= 0:
            timerDown -= 1
            print(timerDown)
        map3dDots.draw(screen)  # Dibuixar els punts del mapa de punts 3D.
        lineToDraw.draw(screen)  # Dibuixar els punts seleccionats com a lineToDraw.

        # Dibuixar totes les línies ja guardades:
        for traçada in entireDrawLinePointsList:
            for i in range(len(traçada) - 1):
                x_fin = traçada[i + 1][0]
                y_fin = traçada[i + 1][1]
                x_ini = traçada[i][0]
                y_ini = traçada[i][1]
                pygame.draw.line(screen, (0, 255, 0), (x_ini, y_ini), (x_fin, y_fin), 2)

        # Dibuixar la línia o traçada actual
        for i in range(len(drawLinePoints) - 1):
            x_ini = drawLinePoints[i][0]
            y_ini = drawLinePoints[i][1]
            x_fin = drawLinePoints[i + 1][0]
            y_fin = drawLinePoints[i + 1][1]
            pygame.draw.line(screen, (0, 0, 0), (x_ini, y_ini), (x_fin, y_fin), 2)

        pygame.display.flip()  # Per només actualitzar una part de la pantalla en comptes de tota cada vegada.

        if saveCurrentLine:
            saveCurrentLine = False
            entireDrawLinePointsList.append(drawLinePoints)
            drawLinePoints = []
            print("Guardat!! Len entireDrawLinePointsList: ", len(entireDrawLinePointsList))

        if stillCounting:
            mouseClickTimer -= 1  # Timer en el qual comptarem
            if mouseClickTimer <= 0:
                stillCounting = False

    pygame.quit()
    exit()
"""
