import cv2
import numpy as np
import math

from src.model.models import ObjModel
from src.model.models import DummyCubeModel

from ..tool.tools import parametrical_line_point


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

    def _draw_obj(self, points, normals, surfaces, normal_lines):
        image = self._scene
        data = {}

        for surface in surfaces:
            contour_points = points[surface[:,0].astype(int) - 1].astype(int)
            contour_normals = normals[surface[:,1].astype(int) - 1]

            ax = contour_points[0][0]
            bx = contour_points[1][0]
            cx = contour_points[2][0]
            ay = contour_points[0][1]
            by = contour_points[1][1]
            cy = contour_points[2][1]

            s = int(abs((ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) / 2))

            if contour_normals[:,2].min() > 0: # and contour_normals[:,1].min() == 0:
                print(contour_normals)
                if not data.get(s):
                    data[s] = [surface]

                else:
                    data[s].append(surface)

        
        keys = sorted(data)

        print(keys)

        # Render surfaces
        # for surface in surfaces:
        #     contour_points = points[surface[:,0].astype(int) - 1].astype(int)
        #     contour_normals = normals[surface[:,1].astype(int) - 1]

        #     if contour_normals[:,2].min() >= 0:
        #         cv2.drawContours(image, [contour_points], 0, (150, 100, 120), -1)

        for key in keys:
            s = data.get(key)
            for surface in s:
                contour_points = points[surface[:,0].astype(int) - 1].astype(int)
                contour_normals = normals[surface[:,1].astype(int) - 1]

                if contour_normals[:,2].min() >= 0:
                    cv2.drawContours(image, [contour_points], 0, (150, 100, 120), -1)

            for surface in s:
                contour_points = points[surface[:,0].astype(int) - 1].astype(int)
                contour_normals = normals[surface[:,1].astype(int) - 1]

                if contour_normals[:,2].min() >= 0:
                    cv2.drawContours(image, [contour_points], 0, (150, 255, 120), 1)

      
        # contour_points = points[surfaces[6][:,0].astype(int) - 1].astype(int)
        # contour_normals = normals[surfaces[6][:,1].astype(int) - 1]

        # print(contour_normals)

        # mc = contour_points[:,0].max() - (self.world.camera.   .projective_plane_width / 2)
        # co = 30 / self.world.camera.projective_plane_width

        # angle_deg = abs(math.radians(co* mc))
        # # print(math.degrees(contour_normals[2][2]))

        # # breakpoint()
        # # # exit()
        # cv2.drawContours(image, [contour_points], 0, (150, 100, 255), -1)




        # for i in range(0, len(surfaces), 1):
        #     surface = surfaces[i]
        #     contour_points = points[surface[:,0].astype(int) - 1].astype(int)
        #     contour_normals = normals[surface[:,1].astype(int) - 1]
        #     contour_normal_lines = normal_lines[i]


            # if contour_normals[:,2:3].min() >= 0 and not np.isnan(contour_normal_lines).any():
            #     print(contour_normals)
            #     cv2.drawContours(image, [contour_points], 0, (100, 100, 120), -1)
            #     cv2.drawContours(image, [contour_points], 0, (0,0,255), 1)


            # center = contour_points.mean(0).astype(int)
            # image = cv2.circle(image, (center[0], center[1]), 8, (255, 255, 0), -1)
                

            # for j, (point, n, nl) in enumerate(zip(contour_points, contour_normals, contour_normal_lines)):
            #     point_start = nl[0].astype(int)
            #     point_end = nl[1].astype(int)



            #     if n[2] >= 0:
            #         col = (0, 110, 200)
            #         image = cv2.circle(image, (point[0] + 1, point[1] + 1), 4, (0, 0, 255), -1)
            #         image = cv2.line(image, (point_start[0], point_start[1]), (point_end[0], point_end[1]), col, 1, 1)

            #     else:
            #         col = (255, 0,0)
            #         image = cv2.circle(image, (point[0] + 1, point[1] + 1), 4, (255, 0, 0), -1)
            #         image = cv2.line(image, (point_start[0], point_start[1]), (point_end[0], point_end[1]), col, 1, 1)
                    

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
        points, n, nl = self._world.camera.view(model)

        return self._draw_obj(points, n, model._surfaces, nl)

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