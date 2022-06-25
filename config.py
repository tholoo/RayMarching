from pyglet.graphics import Batch

WIDTH, HEIGHT = 800, 800
MIN_WH = min(WIDTH, HEIGHT)
BG_COLOR = 60, 60, 70

batch = Batch()

# How close should the point be before detecting as hit
EPSILON = 0.5
# How many steps should the ray take
MAX_MARCHING_STEPS = 40

POV = 45
ROTATION_SPEED = 5

# Less = More Lines
COUNT = 1

DEBUG = False
