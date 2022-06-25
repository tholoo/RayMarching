import pyglet

from random import uniform
import numpy as np

from config import *
from objects import Circle
from helpers import normalize, rotate

# config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(WIDTH, HEIGHT)

background = pyglet.shapes.Rectangle(0, 0, WIDTH, HEIGHT, color=BG_COLOR, batch=batch)

r = 25
circles = []
for i in range(10):
    circle = Circle(uniform(0, WIDTH), uniform(0, HEIGHT), uniform(r / 2, r * 2), color=(150, 40, 60))
    circles.append(circle)

point = Circle(WIDTH / 2, HEIGHT / 2, r / 2)
# debug = Circle(point.x, point.y, r, color=(0, 255, 0))
# debug.opacity = 50
mousePos = WIDTH / 2, HEIGHT / 2


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mousePos
    mousePos = x, y


@window.event
def on_draw():
    # window.clear()
    batch.draw()


# angle = 0
points = []
lines = []

midY = HEIGHT / 2
lineW = WIDTH / POV
angleChange = 0


def update(dt):
    global points, lines, povDebug, angleChange
    # global angle
    points = []
    lines = []

    point.position = mousePos
    point_pos = np.array(point.position)

    setFirst, first, last = False, None, None
    povDebug = [[], []]
    povDebug[0] = pyglet.shapes.Line(*point.position, *point.position + rotate(np.array((0, 1)), angleChange) * midY,
                                     batch=batch)

    for angle in np.arange(angleChange, POV + angleChange, COUNT):
        looking_dir = rotate(np.array((0, 1)), angle)

        hit, depth, pos = raymarch(point_pos, looking_dir, DEBUG)
        if hit:
            if not setFirst: first = pos; setFirst = True
            last = pos
            p = Circle(*pos, r / 10)
            p.opacity = 150
            points.append(p)
            # mid = np.interp(depth ** 2, [0, WIDTH * HEIGHT], [HEIGHT, 0])
            mid = np.interp(depth, [0, MIN_WH], [midY, 0])
            brightness = int(np.interp(depth ** 2, [0, WIDTH * HEIGHT], [255, 0]))
            x = WIDTH - (angle - angleChange) * lineW

            line = pyglet.shapes.Line(x, midY - mid, x, midY + mid, lineW,
                                      color=(brightness, brightness, brightness), batch=batch)
            line.opacity = 160
            lines.append(line)

            # angle += dt * ROTATION_SPEED
            # angle %= POV
    # if setFirst:
    #     povDebug = pyglet.shapes.Triangle(point.position[0], point.position[1], first[0], first[1], last[0],
    #                                       last[1],
    #                                       batch=batch)
    #     povDebug.opacity = 10

    angleChange += 1
    povDebug[1] = pyglet.shapes.Line(*point.position, *point.position + looking_dir * midY, batch=batch)


def raymarch(pos, looking_dir, debug=False):
    global debugs

    debugs = []
    depth = 0
    hit = False

    for i in range(MAX_MARCHING_STEPS):
        min_sdf = scene_sdf(pos)

        if 0 <= min_sdf < EPSILON:
            hit = True
            break  # Hit

        elif min_sdf < 0:
            break

        if 0 < pos[0] < WIDTH and 0 < pos[1] < HEIGHT:
            if debug:
                debug = Circle(pos[0], pos[1], min_sdf, color=(255, 255, 255))
                debug.opacity = 20
                debugs.append(debug)

            depth += min_sdf
            pos = pos + min_sdf * looking_dir

            # if debug:
            #     debug = Circle(pos[0], pos[1], r / 5, color=(0, 0, 0))
            #     debugs.append(debug)
        else:
            break  # Didn't hit

    if debug:
        if (hit):
            for debug in debugs:
                debug.color = (0, 255, 0)

        (x, y), (x2, y2) = point.position, pos
        debugs.append(pyglet.shapes.Line(x, y, x2, y2, batch=batch))

    return hit, depth, pos


def scene_sdf(point):
    min_sdf = np.inf

    for circle in circles:
        sdf = circle.sdf(point)
        min_sdf = min(min_sdf, sdf)

    return min_sdf if min_sdf != np.inf else False


pyglet.clock.schedule_interval(update, 1 / 60.)

if __name__ == '__main__':
    pyglet.app.run()
