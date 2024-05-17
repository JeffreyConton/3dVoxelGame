from voxel import Voxel
import numpy as np
import noise

class Chunk:
    def __init__(self, position, seed):
        self.position = position
        self.size = (32, 32, 32)  # Set chunk size to 32x32x32
        self.voxels = np.empty(self.size, dtype=object)
        self.seed = seed
        self.generate_voxels()

    def generate_voxels(self):
        print(f"Generating voxels for chunk at {self.position}")
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    world_x = x + self.position[0] * self.size[0]
                    world_y = y + self.position[1] * self.size[1]
                    world_z = z + self.position[2] * self.size[2]
                    height = self.generate_height(world_x, world_z)
                    if world_y <= height:
                        self.voxels[x, y, z] = Voxel((world_x, world_y, world_z))
                    else:
                        self.voxels[x, y, z] = None

    def generate_height(self, x, z):
        scale = 100.0  # Adjust scale as needed
        max_height = 32  # Maximum height of terrain
        height = noise.pnoise2(x / scale, z / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=self.seed)
        return int((height + 1) / 2 * max_height)  # Normalize to range [0, max_height]

    def render(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if self.voxels[x, y, z] is not None:
                        self.voxels[x, y, z].render()