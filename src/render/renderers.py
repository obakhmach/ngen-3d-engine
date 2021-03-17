import cv2
import numpy as np

from src.model.models import ObjModel
from src.model.models import DummyCubeModel


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


# @world_needed
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

    def _draw_obj(self, points, normals, surfaces):
        image = self._scene

        for i in range(0, len(surfaces), 1):
            surface = surfaces[i]
            contour_normals = (normals[surface[:,1].astype(int) - 1] * 100).astype(int)
            contour_points = points[surface[:,0].astype(int) - 1].astype(int)

            cv2.drawContours(image, [contour_points], 0, (0, 255, 0), -1)

            for normal, point in zip(contour_normals, contour_points):
                image = cv2.circle(image, (point[0] + 1, point[1] + 1), 4, (0, 0, 255), -1)
                image = cv2.line(image, (point[0], point[1]), (point[0] + normal[0], point[1] + normal[1]),(0, 0, 255), 1, 1)

            cv2.drawContours(image, [contour_points], 0, (255,0,0), 2)

        self._scene = image


    def _draw_cube(self, points):
        image = self._scene
        cube = points

        if not (np.isnan(np.sum(cube[0])) or np.isnan(np.sum(cube[1]))):
            image = cv2.line(image, (int(cube[0][0]), int(cube[0][1])), (int(cube[1][0]), int(cube[1][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[0])) or np.isnan(np.sum(cube[2]))):
            image = cv2.line(image, (int(cube[0][0]), int(cube[0][1])), (int(cube[2][0]), int(cube[2][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[2])) or np.isnan(np.sum(cube[3]))):
            image = cv2.line(image, (int(cube[2][0]), int(cube[2][1])), (int(cube[3][0]), int(cube[3][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[3])) or np.isnan(np.sum(cube[1]))):
            image = cv2.line(image, (int(cube[3][0]), int(cube[3][1])), (int(cube[1][0]), int(cube[1][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[4])) or np.isnan(np.sum(cube[5]))):
            image = cv2.line(image, (int(cube[4][0]), int(cube[4][1])), (int(cube[5][0]), int(cube[5][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[4])) or np.isnan(np.sum(cube[6]))):
            image = cv2.line(image, (int(cube[4][0]), int(cube[4][1])), (int(cube[6][0]), int(cube[6][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[6])) or np.isnan(np.sum(cube[7]))):
            image = cv2.line(image, (int(cube[6][0]), int(cube[6][1])), (int(cube[7][0]), int(cube[7][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[7])) or np.isnan(np.sum(cube[5]))):
            image = cv2.line(image, (int(cube[7][0]), int(cube[7][1])), (int(cube[5][0]), int(cube[5][1])), (0, 0, 255), 3)

        if not (np.isnan(np.sum(cube[0])) or np.isnan(np.sum(cube[4]))):
            image = cv2.line(image, (int(cube[0][0]), int(cube[0][1])), (int(cube[4][0]), int(cube[4][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[1])) or np.isnan(np.sum(cube[5]))):
            image = cv2.line(image, (int(cube[1][0]), int(cube[1][1])), (int(cube[5][0]), int(cube[5][1])), (0, 0, 255), 3)
        
        if not (np.isnan(np.sum(cube[2])) or np.isnan(np.sum(cube[6]))):
            image = cv2.line(image, (int(cube[2][0]), int(cube[2][1])), (int(cube[6][0]), int(cube[6][1])), (0, 0, 255), 3)
    
        if not (np.isnan(np.sum(cube[3])) or np.isnan(np.sum(cube[7]))):
            image = cv2.line(image, (int(cube[3][0]), int(cube[3][1])), (int(cube[7][0]), int(cube[7][1])), (0, 0, 255), 3)

        for point in cube:
            if not np.isnan(np.sum(point)):
                x = int(point[0])
                y = int(point[1])
        
                image = cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        self._scene = image

    def _render_obj(self, model):
        points = self._world.camera.view(model)
        normals = self._world.camera.view_normals(model)

        return self._draw_obj(points, model._normals, model._surfaces)

    def _render_dummy_cube(self, model):
        points = self._world.camera.view(model)

        return self._draw_cube(points)

    def render(self):
        for model in self._world.models:
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