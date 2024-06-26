# settings.py

# Display settings
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Camera settings
CAMERA_START_POS = [0, 16, 30]
CAMERA_SENSITIVITY = 0.1
CAMERA_MOVE_SPEED = 0.5

# Chunk settings
CHUNK_SIZE = (32, 32, 32)
CHUNK_HEIGHT_SCALE = 100.0
CHUNK_MAX_HEIGHT = 32

# World settings
WORLD_SEED = 0
RENDER_DISTANCE = 4  # Number of chunks to render in each direction

# Noise settings
NOISE_OCTAVES = 6
NOISE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2.0
NOISE_REPEAT = 1024