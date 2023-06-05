"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tractament_imatges import img_to_3d_points

def draw_mesh(points, indices, transparency):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 1.0, 1.0, transparency)  # Configura el color con transparencia
    for triangle in indices:
        for vertex_index in triangle:
            if vertex_index < len(points):
                glVertex3fv(points[vertex_index])
    glEnd()

    glDisable(GL_BLEND)
    glDisable(GL_DEPTH_TEST)



def normalize_points(points):
    min_val = min(min(p) for p in points)
    max_val = max(max(p) for p in points)
    range_val = max_val - min_val

    normalized_points = []
    for p in points:
        normalized_p = [(2 * ((v - min_val) / range_val) - 1) for v in p]
        normalized_points.append(normalized_p)

    return normalized_points

def img_to_mesh_indices(points3D):
    # Generar los índices de los triángulos del mesh
    indices = []

    num_points_x = len(points3D[0])  # Número de puntos en el eje x
    num_points_y = len(points3D)  # Número de puntos en el eje y

    for i in range(num_points_y - 1):
        for j in range(num_points_x - 1):
            # Triángulo 1
            indices.append([i * num_points_x + j, (i + 1) * num_points_x + j, i * num_points_x + j + 1])
            # Triángulo 2
            indices.append([(i + 1) * num_points_x + j, (i + 1) * num_points_x + j + 1, i * num_points_x + j + 1])

    return indices



def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    puntos = img_to_3d_points()

    normalized_points = normalize_points(puntos)
    indices = img_to_mesh_indices(puntos)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslate(0.0, 0.0, -5)
    rotate_camera = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                rotate_camera = not rotate_camera

        # Control de la cámara con el ratón
        mouse_x, mouse_y = pygame.mouse.get_rel()
        if rotate_camera and pygame.mouse.get_pressed()[0]:
            glRotatef(mouse_x, 0, 1, 0)
            glRotatef(mouse_y, 1, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_mesh(normalized_points, indices, 0.5)
        pygame.display.flip()
        pygame.time.wait(10)

main()

"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tractament_imatges import img_to_3d_points


def draw_points(points):
    glBegin(GL_POINTS)
    for i, point in enumerate(points):
        glColor3f(1.0, 0.0, 0.0)  # Color de visualización de los puntos
        glVertex3fv(point)
    glEnd()


def normalize_points(points):
    min_val = min(min(p) for p in points)
    max_val = max(max(p) for p in points)
    range_val = max_val - min_val

    normalized_points = []
    for p in points:
        normalized_p = [(2 * ((v - min_val) / range_val) - 1) for v in p]
        normalized_points.append(normalized_p)

    return normalized_points


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("MultiArm")
    puntos = img_to_3d_points()
    normalized_points = normalize_points(puntos)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslate(0.0, 0.0, -5)

    selected_point = -1  # Punto inicialmente no seleccionado

    rotate_camera = True  # Indica si el movimiento de la cámara está habilitado

    glClearColor(1.0, 1.0, 1.0, 1.0)  # Establecer el color de fondo a blanco

    print("Starting main Loop: ")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not rotate_camera:
                    # To implement . . .
                    a = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                rotate_camera = not rotate_camera

        # Control de la cámara con el ratón
        mouse_x, mouse_y = pygame.mouse.get_rel()
        if rotate_camera and pygame.mouse.get_pressed()[0]:
            glRotatef(mouse_x, 0, 1, 0)
            glRotatef(mouse_y, 1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT)
        draw_points(normalized_points)
        pygame.display.flip()
        pygame.time.wait(10)


main()
