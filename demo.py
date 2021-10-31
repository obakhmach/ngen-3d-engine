
import math


from random import randint
from path import Path
from src.model.models import ObjModel
from src.camera.cameras import PerspectiveCamera
from src.render.renderers import DummyOpencvRenderer
from src.world.worlds import World


VIEWPORT_WIDTH = 600
VIEWPORT_HEIGHT = 600

if __name__ == '__main__':
    camera = PerspectiveCamera(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    renderer = DummyOpencvRenderer()
    world = World()

    world.camera = camera
    world.renderer = renderer
    angle = 0
    radius = 1800

    rabit_path = str(Path('data') / 'rabit')
    letter_f_path = str(Path('data') / 'letter_f')
    letter_u_path = str(Path('data') / 'letter_u')
    letter_c_path = str(Path('data') / 'letter_c')
    letter_k_path = str(Path('data') / 'letter_k')
    spaceship_path = str(Path('data') / 'spaceship')

    letter_f_model = ObjModel(letter_f_path, scale_x=80, scale_y=100, scale_z=100, pos_x=-150*4, pos_y=-200, color=(79, 160, 247))
    letter_u_model = ObjModel(letter_u_path, scale_x=80, scale_y=100, scale_z=100, pos_x=-50*4, pos_y=-200, color=(66, 345, 72))
    letter_c_model = ObjModel(letter_c_path, scale_x=80, scale_y=100, scale_z=100, pos_x=50*4, pos_y=-200, color=(245, 66, 90))
    letter_k_model = ObjModel(letter_k_path, scale_x=80, scale_y=100, scale_z=100, pos_x=150*4, pos_y=-200, color=(245, 66, 242))
    rabit_model = ObjModel(rabit_path, scale_x=18, scale_y=18, scale_z=18, pos_x=0, pos_y=370, angle_z_deg=0, angle_x_deg=-90, color=(245, 66, 242))
    spaceship_model = ObjModel(spaceship_path, scale_x=4, scale_y=4, scale_z=4, pos_x=0, pos_y=-570, angle_z_deg=0, angle_x_deg=-30, color=(150, 150, 150))


    world.add_model(letter_f_model)
    world.add_model(letter_u_model)
    world.add_model(letter_c_model)
    world.add_model(letter_k_model)
    world.add_model(rabit_model)
    world.add_model(spaceship_model)    

    world.camera.move_z(radius)

    world.camera.rotate_y(180)
    world.camera.rotate_z(180)
    
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
            world.models[1].move_x(-20)

        elif key == ord('d'):
            world.models[1].move_x(20)

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

        for model in world.models[0:4]:
            model.rotate_y(4)
            model.rotate_x(0)


        world.models[4].rotate_z(3)
        world.models[5].rotate_z(3)

        world.update()
        world.render()
        world.show()
       