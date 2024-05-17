from chunk import Chunk
import settings
import math

class World:
    def __init__(self):
        self.seed = settings.WORLD_SEED  # Use seed from settings
        self.chunks = {}
        self.render_distance = settings.RENDER_DISTANCE
        self.generate_initial_chunks()

    def generate_initial_chunks(self):
        for x in range(-self.render_distance, self.render_distance + 1):
            for z in range(-self.render_distance, self.render_distance + 1):
                self.create_chunk(x, z)

    def create_chunk(self, cx, cz):
        position = (cx, 0, cz)
        self.chunks[(cx, cz)] = Chunk(position, self.seed)

    def get_chunk(self, cx, cz):
        if (cx, cz) not in self.chunks:
            self.create_chunk(cx, cz)
        return self.chunks[(cx, cz)]

    def render(self, camera_pos):
        self.vertex_count = 0
        self.voxel_count = 0

        chunk_x = int(camera_pos[0] // settings.CHUNK_SIZE[0])
        chunk_z = int(camera_pos[2] // settings.CHUNK_SIZE[2])

        for x in range(chunk_x - self.render_distance, chunk_x + self.render_distance + 1):
            for z in range(chunk_z - self.render_distance, chunk_z + self.render_distance + 1):
                chunk = self.get_chunk(x, z)
                chunk.render()
                self.vertex_count += chunk.vertex_count
                self.voxel_count += chunk.voxel_count