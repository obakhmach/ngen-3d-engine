from path import Path
from src.model.models import ObjModel
from src.model.models import DummyCubeModel
from src.camera.cameras import PerspectiveCamera
from src.render.renderers import DummyOpencvRenderer
from src.world.worlds import World


VIEWPORT_WIDTH = 500
VIEWPORT_HEIGHT = 500

if __name__ == '__main__':
    camera = PerspectiveCamera(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    renderer = DummyOpencvRenderer()
    world = World()

    world.camera = camera
    world.renderer = renderer

    model_obj_path = str(Path('data') / 'cube.obj')
    model1 = ObjModel(model_obj_path, scale_x=5, scale_y=6, scale_z=4, pos_x=10, pos_y=-10)
    model2 = ObjModel(model_obj_path, scale_x=4, scale_y=2, scale_z=3, pos_y=10, color=(79, 160, 247))
    model3 = ObjModel(model_obj_path, scale_x=3, scale_y=4, scale_z=4, pos_x=-10, pos_y=-10, color=(186, 79, 247))


    world.add_model(model1)
    world.add_model(model2)
    world.add_model(model3)
    world.camera.move_z(-15)
    
    world.update()

    while True:
        key = world.clear()

        if key == ord('w'):
            world.camera.move_z(3)

        elif key == ord('s'):
            world.camera.move_z(-3)

        if key == ord('q'):
            world.camera.move_y(3)

        elif key == ord('e'):
            world.camera.move_y(-3)

        elif key == ord('a'):
            world.camera.move_x(-3)

        elif key == ord('d'):
            world.camera.move_x(3)

        elif key == ord('t'):
            world.camera.rotate_x(5)

        elif key == ord('g'):
            world.camera.rotate_x(-5)

        elif key == ord('f'):
            world.camera.rotate_y(5)

        elif key == ord('h'):
            world.camera.rotate_y(-5)

        elif key == ord('o'):
            world.models[0].rotate_y(5)

        elif key == ord('p'):
            world.models[0].rotate_y(-5)

        for model in world.models:

            model.rotate_z(4)
            model.rotate_y(3)
            model.rotate_x(5)



        world.update()
        world.render()
        world.show()

        

