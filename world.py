from chunk import Chunk

class World:
    def __init__(self):
        self.seed = 0  # Use a fixed seed for debugging
        self.chunk = Chunk((0, 0, 0), self.seed)  # Single test chunk at the origin
        self.vertex_count = 0
        self.voxel_count = 0

    def render(self):
        self.vertex_count = 0
        self.voxel_count = 0
        self.chunk.render()
        self.vertex_count += self.chunk.vertex_count
        self.voxel_count += self.chunk.voxel_count