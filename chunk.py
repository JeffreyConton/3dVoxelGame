from voxel import Voxel
import numpy as np
import noise
from OpenGL.GL import *
import settings

class Chunk:
    def __init__(self, position, seed):
        self.position = position
        self.size = settings.CHUNK_SIZE  # Use chunk size from settings
        self.voxels = np.empty(self.size, dtype=object)
        self.seed = seed
        self.vertex_count = 0
        self.voxel_count = 0
        self.generate_voxels()
        self.vbo = None
        self.generate_vbo()

    def generate_voxels(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    world_x = x + self.position[0] * self.size[0]
                    world_y = y + self.position[1] * self.size[1]
                    world_z = z + self.position[2] * self.size[2]
                    height = self.generate_height(world_x, world_z)
                    if world_y <= height:
                        self.voxels[x, y, z] = Voxel((x, y, z), self)
                        self.voxel_count += 1
                    else:
                        self.voxels[x, y, z] = None

    def generate_height(self, x, z):
        scale = settings.CHUNK_HEIGHT_SCALE  # Use height scale from settings
        max_height = settings.CHUNK_MAX_HEIGHT  # Use max height from settings
        height = noise.pnoise2(x / scale, z / scale, octaves=settings.NOISE_OCTAVES, persistence=settings.NOISE_PERSISTENCE, lacunarity=settings.NOISE_LACUNARITY, repeatx=settings.NOISE_REPEAT, repeaty=settings.NOISE_REPEAT, base=self.seed)
        return int((height + 1) / 2 * max_height)  # Normalize to range [0, max_height]

    def generate_vbo(self):
        vertices = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if self.voxels[x, y, z] is not None:
                        vertices.extend(self.voxels[x, y, z].get_vertex_data())

        self.vertex_count = len(vertices) // 7  # 3 for position and 4 for color

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(vertices, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def render(self):
        if self.vbo is None:
            return

        glPushMatrix()
        glTranslatef(self.position[0] * self.size[0], self.position[1] * self.size[1], self.position[2] * self.size[2])
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 7 * 4, None)
        glColorPointer(4, GL_FLOAT, 7 * 4, ctypes.c_void_p(3 * 4))
        glDrawArrays(GL_QUADS, 0, self.vertex_count)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glPopMatrix()