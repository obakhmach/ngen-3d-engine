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

    model = DummyCubeModel(scale_x=50, scale_y=50, scale_z=50)
    
    world.camera.pos_z = -400
    
    world.add_model(model)
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



        world.update()
        world.render()
        world.show()

        

