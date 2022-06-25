import pyglet
import numpy as np
from config import *


class Circle(pyglet.shapes.Circle):
    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwrgs, batch=batch)

    def sdf(self, point):
        return np.linalg.norm(point - np.array(self.position)) - self.radius
