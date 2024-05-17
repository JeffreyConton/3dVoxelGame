import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from world import World
import math
import os
import sys
import settings


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    pygame.init()
    display = (settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera variables
    camera_pos = settings.CAMERA_START_POS[:]
    camera_rot = [0, 0]  # Rotation in pitch (up/down) and yaw (left/right)

    world = World()

    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    sensitivity = settings.CAMERA_SENSITIVITY
    move_speed = settings.CAMERA_MOVE_SPEED
    mouse_locked = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouse_locked = not mouse_locked
                    pygame.mouse.set_visible(not mouse_locked)
                    pygame.event.set_grab(mouse_locked)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not mouse_locked:
                    mouse_locked = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_pos[2] -= move_speed * math.cos(math.radians(camera_rot[1]))
            camera_pos[0] += move_speed * math.sin(math.radians(camera_rot[1]))
        if keys[pygame.K_s]:
            camera_pos[2] += move_speed * math.cos(math.radians(camera_rot[1]))
            camera_pos[0] -= move_speed * math.sin(math.radians(camera_rot[1]))
        if keys[pygame.K_a]:
            camera_pos[2] -= move_speed * math.sin(math.radians(camera_rot[1]))
            camera_pos[0] -= move_speed * math.cos(math.radians(camera_rot[1]))
        if keys[pygame.K_d]:
            camera_pos[2] += move_speed * math.sin(math.radians(camera_rot[1]))
            camera_pos[0] += move_speed * math.cos(math.radians(camera_rot[1]))
        if keys[pygame.K_SPACE]:
            camera_pos[1] += move_speed
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            camera_pos[1] -= move_speed

        if mouse_locked:
            mouse_movement = pygame.mouse.get_rel()
            camera_rot[1] += mouse_movement[0] * sensitivity
            camera_rot[0] += mouse_movement[1] * sensitivity  # Correct the pitch movement direction
            camera_rot[0] = max(-90, min(90, camera_rot[0]))  # Clamp pitch

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(camera_rot[0], 1, 0, 0)
        glRotatef(camera_rot[1], 0, 1, 0)
        glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

        stats = {
            'fps': clock.get_fps(),
            'vertices': 0,
            'chunks': 0,
            'voxels': 0
        }

        world.render(camera_pos)

        stats['vertices'] = world.vertex_count
        stats['chunks'] = len(world.chunks)
        stats['voxels'] = world.voxel_count

        clear_console()
        print(f"FPS: {stats['fps']:.2f}")
        print(f"Vertices: {stats['vertices']}")
        print(f"Chunks: {stats['chunks']}")
        print(f"Voxels: {stats['voxels']}")
        sys.stdout.flush()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()