from path import Path
from src.model.models import ObjModel
from src.model.models import DummyCubeModel
from src.camera.cameras import PerspectiveCamera
from src.render.renderers import DummyOpencvRenderer
from src.world.worlds import World

import random


if __name__ == '__main__':
    # model_obj_path = str(Path('data') / 'cube.obj')
    # model = ObjModel(model_obj_path, pos_x=-10, pos_y=-10, pos_z=30, scale_x=20, scale_y=20, scale_z=20)
    world = World(PerspectiveCamera, DummyOpencvRenderer)

    for z in range(2):
        for y in range(2):
            for x in range(2):
                model = DummyCubeModel(scale_x=50, scale_y=50, scale_z=50, pos_x=340*x - 300, pos_y=340*y - 300, pos_z=340*z - 300)
                world.add_model(model)
    
    world.camera.pos_z = -400

    world.update()

    while True:
        key = world.clear()

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
            model.rotate_x(random.randint(-5, 15))
            model.rotate_y(random.randint(-5, 15))
            model.rotate_z(random.randint(-5, 15))
            model.move_x(random.randint(-10, 10))
            model.move_y(random.randint(-10, 10))
            model.move_z(random.randint(-10, 10))



        world.update()
        world.render()
        world.show()

        

