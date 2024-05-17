from OpenGL.GL import *
import random

class Voxel:
    def __init__(self, position):
        self.position = position
        self.colors = self.generate_random_pastel_colors()

    def generate_random_pastel_colors(self):
        def random_pastel_color():
            return [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]

        return [random_pastel_color() for _ in range(6)]

    def render(self):
        x, y, z = self.position
        vertices = [
            (x, y, z), (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z),  # Front face
            (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x, y + 1, z + 1),  # Back face
            (x, y, z), (x, y, z + 1), (x, y + 1, z + 1), (x, y + 1, z),  # Left face
            (x + 1, y, z), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x + 1, y + 1, z),  # Right face
            (x, y, z), (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y, z),  # Bottom face
            (x, y + 1, z), (x, y + 1, z + 1), (x + 1, y + 1, z + 1), (x + 1, y + 1, z)  # Top face
        ]

        faces = [
            (0, 1, 2, 3),  # Front
            (4, 5, 6, 7),  # Back
            (8, 9, 10, 11),  # Left
            (12, 13, 14, 15),  # Right
            (16, 17, 18, 19),  # Bottom
            (20, 21, 22, 23)  # Top
        ]

        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glColor3f(*self.colors[i])
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()