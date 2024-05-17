from chunk import Chunk

class World:
    def __init__(self):
        self.seed = 0  # Use a fixed seed for debugging
        self.chunk = Chunk((0, 0, 0), self.seed)  # Single test chunk at the origin

    def render(self):
        self.chunk.render()