from OpenGL.GL import *
import random

class Voxel:
    def __init__(self, position, chunk):
        self.position = position
        self.chunk = chunk
        self.colors = self.generate_random_pastel_colors()

    def generate_random_pastel_colors(self):
        def random_pastel_color():
            return [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), 1.0]  # RGBA
        return [random_pastel_color() for _ in range(6)]

    def is_exposed(self, neighbor):
        x, y, z = self.position
        nx, ny, nz = neighbor
        if 0 <= nx < self.chunk.size[0] and 0 <= ny < self.chunk.size[1] and 0 <= nz < self.chunk.size[2]:
            return self.chunk.voxels[nx, ny, nz] is None
        return True

    def get_vertex_data(self):
        x, y, z = self.position
        vertex_data = []
        faces = [
            [(x, y, z), (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z)],  # Front face
            [(x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)],  # Back face
            [(x, y, z), (x, y, z + 1), (x, y + 1, z + 1), (x, y + 1, z)],  # Left face
            [(x + 1, y, z), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x + 1, y + 1, z)],  # Right face
            [(x, y, z), (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y, z)],  # Bottom face
            [(x, y + 1, z), (x, y + 1, z + 1), (x + 1, y + 1, z + 1), (x + 1, y + 1, z)]  # Top face
        ]

        neighbors = [
            (x, y, z - 1), (x, y, z + 1),  # Front, Back
            (x - 1, y, z), (x + 1, y, z),  # Left, Right
            (x, y - 1, z), (x, y + 1, z)   # Bottom, Top
        ]

        for i, face in enumerate(faces):
            if self.is_exposed(neighbors[i]):
                color = self.colors[i]
                for vertex in face:
                    vertex_data.extend(vertex)
                    vertex_data.extend(color)  # Include color information

        return vertex_data