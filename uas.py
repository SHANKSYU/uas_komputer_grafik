
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Inisialisasi Pygame
pygame.init()
width, height = 1024, 768
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Komputer Grafik - Ujian SIF509")

# Setup viewport dan proyeksi
glViewport(0, 0, width, height)
glEnable(GL_DEPTH_TEST)

# Bagi layar menjadi dua viewport
def set_viewport_3d():
    glViewport(0, 0, width // 2, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / 2) / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def set_viewport_2d():
    glViewport(width // 2, 0, width // 2, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-5, 5, -5, 5)
    glMatrixMode(GL_MODELVIEW)

# Vertices kubus
cube_vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

cube_edges = (
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
)

def draw_cube():
    glBegin(GL_LINES)
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()

# Persegi 2D (awal: persegi satuan di pusat)
square_vertices = np.array([
    [-1, -1],
    [1, -1],
    [1, 1],
    [-1, 1]
], dtype=np.float32)

def draw_square(transformed_vertices):
    glBegin(GL_LINE_LOOP)
    for v in transformed_vertices:
        glVertex2f(v[0], v[1])
    glEnd()

# State kubus 3D
cube_pos = [0.0, 0.0, -5.0]
cube_rot = [0.0, 0.0, 0.0]  # x, y, z
cube_scale = 1.0

# State persegi 2D
square_pos = [0.0, 0.0]
square_angle = 0.0
square_scale = 1.0
shear_x = 0.0
shear_y = 0.0
reflect_x = False
reflect_y = False

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # === KONTROL KUBUS 3D ===
            if event.key == pygame.K_w:
                cube_pos[2] += 0.2
            elif event.key == pygame.K_s:
                cube_pos[2] -= 0.2
            elif event.key == pygame.K_a:
                cube_pos[0] -= 0.2
            elif event.key == pygame.K_d:
                cube_pos[0] += 0.2
            elif event.key == pygame.K_q:
                cube_pos[1] += 0.2
            elif event.key == pygame.K_e:
                cube_pos[1] -= 0.2
            elif event.key == pygame.K_UP:
                cube_rot[0] += 5
            elif event.key == pygame.K_DOWN:
                cube_rot[0] -= 5
            elif event.key == pygame.K_LEFT:
                cube_rot[1] += 5
            elif event.key == pygame.K_RIGHT:
                cube_rot[1] -= 5
            elif event.key == pygame.K_r:
                cube_rot[2] += 5
            elif event.key == pygame.K_f:
                cube_rot[2] -= 5
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                cube_scale *= 1.1
            elif event.key == pygame.K_MINUS:
                cube_scale /= 1.1

            # === KONTROL PERSEGI 2D ===
            elif event.key == pygame.K_i:
                square_pos[1] += 0.2
            elif event.key == pygame.K_k:
                square_pos[1] -= 0.2
            elif event.key == pygame.K_j:
                square_pos[0] -= 0.2
            elif event.key == pygame.K_l:
                square_pos[0] += 0.2
            elif event.key == pygame.K_u:
                square_angle += 5
            elif event.key == pygame.K_o:
                square_angle -= 5
            elif event.key == pygame.K_RIGHTBRACKET:
                square_scale *= 1.1
            elif event.key == pygame.K_LEFTBRACKET:
                square_scale /= 1.1
            elif event.key == pygame.K_h:
                shear_x += 0.1
            elif event.key == pygame.K_g:
                shear_y += 0.1
            elif event.key == pygame.K_m:
                reflect_x = not reflect_x
            elif event.key == pygame.K_n:
                reflect_y = not reflect_y
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Clear buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # === Gambar Kubus 3D (kiri) ===
    set_viewport_3d()
    glLoadIdentity()
    glTranslatef(*cube_pos)
    glRotatef(cube_rot[0], 1, 0, 0)
    glRotatef(cube_rot[1], 0, 1, 0)
    glRotatef(cube_rot[2], 0, 0, 1)
    glScalef(cube_scale, cube_scale, cube_scale)
    glColor3f(1.0, 0.5, 0.0)
    draw_cube()

    # === Gambar Persegi 2D (kanan) ===
    set_viewport_2d()
    glLoadIdentity()
    glTranslatef(square_pos[0], square_pos[1], 0)

    # Terapkan transformasi pada vertex
    verts = square_vertices.copy()

    # Skala
    verts *= square_scale

    # Rotasi
    angle_rad = math.radians(square_angle)
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    rot_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    verts = verts @ rot_matrix.T

    # Shearing
    shear_matrix = np.array([[1, shear_x], [shear_y, 1]])
    verts = verts @ shear_matrix.T

    # Refleksi
    if reflect_x:
        verts[:, 0] *= -1
    if reflect_y:
        verts[:, 1] *= -1

    glColor3f(0.0, 1.0, 1.0)
    draw_square(verts)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()