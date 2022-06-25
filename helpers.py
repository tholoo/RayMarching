import numpy as np


def normalize(vec):
    # return vec / np.linalg.norm(vec)
    return vec / np.sqrt((vec ** 2).sum())


def rotate(vec, angle):
    angle = np.deg2rad(angle)
    x, y = vec
    cos, sin = np.cos(angle), np.sin(angle)
    return np.array((cos * x - sin * y, sin * x + cos * y))
