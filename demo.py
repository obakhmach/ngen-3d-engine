
import math


from random import randint
from path import Path
from src.model.models import ObjModel
from src.model.models import DummyCubeModel
from src.camera.cameras import PerspectiveCamera
from src.render.renderers import DummyOpencvRenderer
from src.world.worlds import World


VIEWPORT_WIDTH = 1000
VIEWPORT_HEIGHT = 1000

if __name__ == '__main__':
    camera = PerspectiveCamera(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    renderer = DummyOpencvRenderer()
    world = World()

    world.camera = camera
    world.renderer = renderer
    angle = 0
    radius = -800

    model_obj_path = str(Path('data') / 'cube.obj')
    model1 = ObjModel(model_obj_path, scale_x=100, scale_y=500, scale_z=100, pos_x=0, pos_z=0)
    model2 = ObjModel(model_obj_path, scale_x=130, scale_y=120, scale_z=100, pos_x=300, color=(79, 160, 247))
    model3 = ObjModel(model_obj_path, scale_x=110, scale_y=110, scale_z=100, pos_x=-300, pos_y=-300, color=(186, 79, 247))
    model4 = ObjModel(model_obj_path, scale_x=20, scale_y=20, scale_z=20, pos_x=-200, pos_y=200, color=(186, 79, 247))
    model5 = ObjModel(model_obj_path, scale_x=20, scale_y=20, scale_z=20, pos_x=-200, pos_y=200, color=(186, 79, 247))
    model6 = ObjModel(model_obj_path, scale_x=20, scale_y=20, scale_z=20, pos_x=-200, pos_y=200, color=(186, 79, 247))
    model7 = ObjModel(model_obj_path, scale_x=20, scale_y=20, scale_z=20, pos_x=-200, pos_y=200, color=(186, 79, 247))
    model8 = ObjModel(model_obj_path, scale_x=20, scale_y=20, scale_z=20, pos_x=-200, pos_y=200, color=(186, 79, 247))
    model9 = ObjModel(model_obj_path, scale_x=20, scale_y=20, scale_z=20, pos_x=-200, pos_y=200, color=(186, 79, 247))


    world.add_model(model1)
    world.add_model(model2)
    world.add_model(model3)
    world.add_model(model4)
    world.add_model(model5)
    world.add_model(model6)
    world.add_model(model7)
    world.add_model(model8)
    world.add_model(model9)
    world.camera.move_z(radius)
    
    world.update()


    while True:
        key = world.clear()

        if key == ord('w'):

            world.camera.move_z(20)

        elif key == ord('s'):
            world.camera.move_z(-20)

        if key == ord('q'):
            world.camera.move_y(20)

        elif key == ord('e'):
            world.camera.move_y(-20)

        elif key == ord('a'):
            world.camera.move_x(-20)

        elif key == ord('d'):
            world.camera.move_x(20)

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


        angle += 5

        z = int(math.cos(math.radians(angle)) * radius)
        x = int(math.sin(math.radians(angle)) * radius)

        z4 = int(math.cos(math.radians(angle*4)) * radius/8)
        x4 = int(math.sin(math.radians(angle*4)) * radius/8)

        
        camera._angle_y_deg += 5
        camera._pos_x = x
        camera.pos_z = z

        model4.pos_x = x4
        model4.pos_z = z4
        model4.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        model4.pos_y = int(math.sin(angle/100) * 250)

        model5.pos_x = x4
        model5.pos_z = z4
        model5.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        model5.pos_y = int(math.sin(angle/100) * 250) + 40

        model6.pos_x = x4
        model6.pos_z = z4
        model6.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        model6.pos_y = int(math.sin(angle/100) * 250) + 90

        model7.pos_x = x4
        model7.pos_z = z4
        model7.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        model7.pos_y = int(math.sin(angle/100) * 250) - 40

        model8.pos_x = x4
        model8.pos_z = z4
        model8.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        model8.pos_y = int(math.sin(angle/100) * 250) - 90

        model9.pos_x = x4
        model9.pos_z = z4
        model9.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        model9.pos_y = int(math.sin(angle/100) * 250) -  140

        for model in world.models[5:9]:
            model.rotate_z(4)
            model.rotate_y(3)
            model.rotate_x(5)

        world.update()
        world.render()
        world.show()
       