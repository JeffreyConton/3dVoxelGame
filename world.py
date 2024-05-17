from chunk import Chunk
import settings

class World:
    def __init__(self):
        self.seed = settings.WORLD_SEED  # Use seed from settings
        self.chunk = Chunk((0, 0, 0), self.seed)  # Single test chunk at the origin
        self.vertex_count = 0
        self.voxel_count = 0

    def render(self):
        self.vertex_count = 0
        self.voxel_count = 0
        self.chunk.render()
        self.vertex_count += self.chunk.vertex_count
        self.voxel_count += self.chunk.voxel_count