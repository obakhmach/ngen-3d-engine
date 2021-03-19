from path import Path
from src.model.models import ObjModel
from src.model.models import DummyCubeModel
from src.camera.cameras import PerspectiveCamera
from src.render.renderers import DummyOpencvRenderer
from src.world.worlds import World


VIEWPORT_WIDTH = 900
VIEWPORT_HEIGHT = 900

if __name__ == '__main__':
    camera = PerspectiveCamera(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    renderer = DummyOpencvRenderer()
    world = World()

    world.camera = camera
    world.renderer = renderer

    model_obj_path = str(Path('data') / 'cube.obj')
    model = ObjModel(model_obj_path, scale_x=10, scale_y=10, scale_z=10)


    world.add_model(model)
    world.camera.move_z(-40)
    
    world.update()

    while True:
        key = world.clear()

        if key == ord('w'):
            world.camera.move_z(1)

        elif key == ord('s'):
            world.camera.move_z(-1)

        elif key == ord('a'):
            world.camera.move_x(-1)

        elif key == ord('d'):
            world.camera.move_x(1)

        elif key == ord('t'):
            world.camera.rotate_x(5)

        elif key == ord('g'):
            world.camera.rotate_x(-5)

        elif key == ord('f'):
            world.camera.rotate_y(5)

        elif key == ord('h'):
            world.camera.rotate_y(-5)

        elif key == ord('o'):
            world.models[0].rotate_y(10)

        elif key == ord('p'):
            world.models[0].rotate_y(-10)

        # for model in world.models:

        #     model.rotate_z(4)
        #     model.rotate_y(3)


        world.update()
        world.render()
        world.show()

        

