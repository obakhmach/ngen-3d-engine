import cv2
import numpy as np
import math

from src.model.models import ObjModel
from src.model.models import DummyCubeModel

from ..tool.tools import parametrical_line_point
from ..tool.tools import normals_to_degrees


def world_needed(cls):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)) and '_' not in attr:
            def decorator(f):
                def wrapper(*args, **kwargs):
                    if isinstance(args[0], cls) and args[0].world is None:
                        raise ValueError('Renderer can not be used without attaching it to world.')

                    return f(*args, **kwargs)
                
                return wrapper

            setattr(cls, attr, decorator(getattr(cls, attr)))
    return cls


@world_needed
class DummyOpencvRenderer:
    DEFAULT_CHANNELS = 3
    DEFAULT_BACKGROUND_COLOR = (0, 0, 0)

    def __init__(self,
                 channels=None,
                 background_color=None):
        if channels is None:
            channels = self.DEFAULT_CHANNELS

        if background_color is None:
            background_color = self.DEFAULT_BACKGROUND_COLOR

        self._channels = channels
        self._background_color = background_color

    @property
    def world(self):
    	return self._world
    
    @world.setter
    def world(self, value):
        if value.camera is None:
            raise ValueError('The world without camera can not be rendered.')

        self._world = value

        self._background = np.zeros((self._world.camera.projective_plane_height,
        	                         self._world.camera.projective_plane_width,
        	                         self._channels), dtype=np.uint8)

        self._background[:] = self._background_color
        self._scene = self._background.copy()

    def _draw_obj(self, points, normals, surfaces, color):
        image = self._scene

        surface_describtion = {}

        for surface in surfaces:
            contour_points = points[surface[:,0].astype(int) - 1].astype(int)
            contour_normals = normals[surface[:,1].astype(int) - 1]

            surface_points = []

            for contour_normal, contour_point in zip(contour_normals, contour_points):
                surface_point = [contour_point[0], contour_point[1], contour_normal[0], contour_normal[1], contour_normal[2]]

                surface_points.append(surface_point)

            surface_points = np.array(surface_points)

            surface_normal = (np.mean(contour_normals[:, 0]), np.mean(contour_normals[:, 1]), np.mean(contour_normals[:, 2]))

            if surface_describtion.get(surface_normal):
                surface_describtion[surface_normal].append(surface_points)

            else:
                surface_describtion[surface_normal] = [surface_points]

        keys = surface_describtion.keys()

        keys = sorted(keys, key=lambda x: (x[2], -x[0], -x[1]))

        for key in keys:
            surface_data = surface_describtion[key]
            surface_data = np.array(surface_data)

            surface_contours = surface_data[:,:,0:2].astype(np.int)

            for contour in surface_contours:
                cv2.drawContours(image, [contour], 0, color, -1)
                cv2.drawContours(image, [contour], 0, (50, 50, 50), 4)

        self._scene = image

    def _render_obj(self, model):
        viewed_points, viewed_normals = self._world.camera.view(model)
        viewed_surfaces = model._surfaces
        viewed_color = model.color

        return self._draw_obj(viewed_points, viewed_normals, viewed_surfaces, viewed_color)

    def _render_dummy_cube(self, model):
        points = self._world.camera.view(model)

        return self._draw_cube(points)

    def render(self):
        def distance(x1, y1, z1, x2, y2, z2):
            return math.sqrt((x2 - x1)**2 + (y2 - y2)**2 + (z2 - z1)**2)

        c = self._world.camera

        models = sorted(self._world.models, 
                        key=lambda m: -distance(m.pos_x,
                                                m.pos_y,
                                                m.pos_z,
                                                c.pos_x,
                                                c.pos_y,
                                                c.pos_z),
                        reverse=True)

        for model in models:
            if isinstance(model, ObjModel):
                self._render_obj(model)

            elif isinstance(model, DummyCubeModel):
                self._render_dummy_cube(model)

    def show(self):
        cv2.imshow('Scene', self._scene)

    def clear(self):
        key = cv2.waitKey(33)
        self._scene = self._background.copy()

        return key