import pygame
import numpy as np
import math
from tractament_imatges import img_to_3d_points
DOT_COLOR = (255, 100, 127)
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

points = []
angle = 0
pts3d = img_to_3d_points()


projectionMatrix = np.matrix([[height/2, 0, width/2],
                             [0, height/2, height/2]])

#load button images
start_img = pygame.image.load('imgFaces/base/img08_V2_1_face_Pol_sense_sostre.jpeg').convert_alpha()
exit_img = pygame.image.load('imgFaces/base/img08_V2_2_face_Pol_sense_sostre.jpeg').convert_alpha()

#create button instances
#start_button = button.Button(600, 360, start_img, 0.5)
#exit_button = button.Button(600, 500, exit_img, 0.6)

# MAIN LOOP
while True:
    clock.tick(30)
    screen.fill((255, 255, 255))

    rotation = np.matrix([[math.cos(angle), -math.sin(angle), 0],
                         [math.sin(angle), math.cos(angle), 0],
                         [0, 0, 1]])

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    for point in pts3d:
        projected2d = projectionMatrix * rotation * point.reshape((3, 1))
        pygame.draw.circle(screen, DOT_COLOR, (int(projected2d[0][0]), int(projected2d[1][0])), 2)

    angle += 0.01
    pygame.display.update()

"""
import pygame
import sys

# initializing the constructor
pygame.init()

# screen resolution
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (0, 0, 0)

# light shade of the button
color_light = (255, 255, 255)

# dark shade of the button
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color)

while True:

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is terminated
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.quit()

    # fills the screen with a color
    screen.fill((60, 25, 60))

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()

    # if mouse is hovered on a button it
    # changes to lighter shade
    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
        pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])

    else:
        pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])

    # superimposing the text onto our button
    screen.blit(text, (width / 2 + 50, height / 2))

    # updates the frames of the game
    pygame.display.update()"""
