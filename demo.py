from path import Path
from src.model.models import ObjModel
from src.model.models import DummyCubeModel
from src.camera.cameras import PerspectiveCamera
from src.render.renderers import DummyOpencvRenderer
from src.world.worlds import World


import cv2
import numpy as np
import random

def draw_obj(image, vertexes, normals, surfaces):
    for i in range(0, len(surfaces), 1):
        surface = surfaces[i]
        points = vertexes[surface[:,0].astype(int) - 1]

        cv2.drawContours(image, [points], 0, (0, 255, 0), -1)

        for point in points:
            image = cv2.circle(image, (point[0], point[1]), 4, (0, 0, 0), -1)

        cv2.drawContours(image, [points], 0, (255,0,0), 2)


def draw_cube(image, cube):
    if np.nan not in cube[0] and np.nan not in cube[1]:
        image = cv2.line(image, (cube[0][0], cube[0][1]), (cube[1][0], cube[1][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[0] and np.nan not in cube[2]:
        image = cv2.line(image, (cube[0][0], cube[0][1]), (cube[2][0], cube[2][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[2] and np.nan not in cube[3]:
        image = cv2.line(image, (cube[2][0], cube[2][1]), (cube[3][0], cube[3][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[3] and np.nan not in cube[1]:
        image = cv2.line(image, (cube[3][0], cube[3][1]), (cube[1][0], cube[1][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[4] and np.nan not in cube[5]:
        image = cv2.line(image, (cube[4][0], cube[4][1]), (cube[5][0], cube[5][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[4] and np.nan not in cube[6]:
        image = cv2.line(image, (cube[4][0], cube[4][1]), (cube[6][0], cube[6][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[6] and np.nan not in cube[7]:
        image = cv2.line(image, (cube[6][0], cube[6][1]), (cube[7][0], cube[7][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[7] and np.nan not in cube[5]:
        image = cv2.line(image, (cube[7][0], cube[7][1]), (cube[5][0], cube[5][1]), (0, 0, 255), 3)

    if np.nan not in cube[0] and np.nan not in cube[4]:
        image = cv2.line(image, (cube[0][0], cube[0][1]), (cube[4][0], cube[4][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[1] and np.nan not in cube[5]:
        image = cv2.line(image, (cube[1][0], cube[1][1]), (cube[5][0], cube[5][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[2] and np.nan not in cube[6]:
        image = cv2.line(image, (cube[2][0], cube[2][1]), (cube[6][0], cube[6][1]), (0, 0, 255), 3)
    
    if np.nan not in cube[3] and np.nan not in cube[7]:
        image = cv2.line(image, (cube[3][0], cube[3][1]), (cube[7][0], cube[7][1]), (0, 0, 255), 3)

    for point in cube:
        if np.nan not in point:
            x = int(point[0])
            y = int(point[1])
        
            image = cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    return image

if __name__ == '__main__':
    # model_obj_path = str(Path('data') / 'cube.obj')
    # model = ObjModel(model_obj_path, pos_x=-10, pos_y=-10, pos_z=30, scale_x=20, scale_y=20, scale_z=20)

    model = DummyCubeModel(scale_x=50, scale_y=50, scale_z=50)
    world = World(PerspectiveCamera, DummyOpencvRenderer)
    
    world.camera.pos_z = 500

    world.add_model(model)
    world.update()

    BACKGROUND_COLOR = (0, 0, 0)
    CHANNEL = 3
    HEIGHT = 700
    WIDTH = 800
    BACKGROUND = np.zeros((HEIGHT, WIDTH, CHANNEL), dtype=np.uint8)
    BACKGROUND[:] = BACKGROUND_COLOR

    while True:
        key = cv2.waitKey(33)
        cv2.imshow('Scene', BACKGROUND)
        draw = BACKGROUND.copy()

        if key == ord('w'):
            world.camera.move_z(10)

        elif key == ord('s'):
            world.camera.move_z(-10)

        elif key == ord('a'):
            world.camera.move_x(-10)

        elif key == ord('d'):
            world.camera.move_x(10)

        elif key == ord('t'):
            world.camera.rotate_x(5)

        elif key == ord('g'):
            world.camera.rotate_x(-5)

        elif key == ord('f'):
            world.camera.rotate_y(5)

        elif key == ord('h'):
            world.camera.rotate_y(-5)

        for model in world.models:
            model.rotate_y(10)
            points = world.camera.view(model, WIDTH, HEIGHT)

            # draw_obj(draw, points, model._normals, model._surfaces)
            draw = draw_cube(draw, points)

        world.update()

            

        cv2.imshow('Scene', draw)

