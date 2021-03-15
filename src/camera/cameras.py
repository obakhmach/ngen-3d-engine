import math
import numpy as np

from ..tool.tools import rotate
from ..tool.tools import translate


class PerspectiveCamera:
    def __init__(self,
                 world,
                 pos_x=None,
                 pos_y=None, 
                 pos_z=None,
    	         angle_x_deg=None,
    	         angle_y_deg=None,
    	         angle_z_deg=None, 
    	         field_of_view_angle_deg=None, 
    	         aspect_ratio=None,
    	         near=None,
    	         far=None):
        if pos_x is None:
            pos_x = 0

        if pos_y is None:
            pos_y = 0

        if pos_z is None:
            pos_z = 0

        if angle_x_deg is None:
            angle_x_deg = 0

        if angle_y_deg is None:
            angle_y_deg = 0

        if angle_z_deg is None:
            angle_z_deg = 0

        if field_of_view_angle_deg is None:
            field_of_view_angle_deg = 70

        if aspect_ratio is None:
            aspect_ratio = 1

        if near is None:
            near = 20

        if far is None:
            far = 50
   
        self._world = world
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z
        self._angle_x_deg = angle_x_deg
        self._angle_y_deg = angle_y_deg
        self._angle_z_deg = angle_z_deg
        self._field_of_view_angle_deg = field_of_view_angle_deg
        self._aspect_ratio = aspect_ratio
        self._near = near
        self._far = far

    @property
    def pos_x(self):
    	return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        self._pos_x = value

    @property
    def pos_y(self):
    	return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        self._pos_y = value

    @property
    def pos_z(self):
    	return self._pos_z

    @pos_z.setter
    def pos_z(self, value):
        self._pos_z = value

    @property
    def angle_x_deg(self):
    	return self._angle_x_deg

    @angle_x_deg.setter
    def angle_x_deg(self, value):
        self._angle_x_deg = value

    @property
    def angle_y_deg(self):
    	return self._angle_y_deg

    @angle_y_deg.setter
    def angle_y_deg(self, value):
        self._angle_y_deg = value

    @property
    def angle_z_deg(self):
    	return self._angle_z_deg

    @angle_z_deg.setter
    def angle_z_deg(self, value):
        self._angle_z_deg = value

    @property
    def field_of_view_angle_deg(self):
    	return self._field_of_view_angle_deg

    @field_of_view_angle_deg.setter
    def field_of_view_angle_deg(self, value):
        self._field_of_view_angle_deg = value

    @property
    def aspect_ratio(self):
    	return self._aspect_ratio

    @aspect_ratio.setter
    def spect_ratio(self, value):
        self._aspect_ratio = value

    @property
    def world(self):
    	return self._world

    def move_x(self, value):
        self._pos_x += value

    def move_y(self, value):
        self._pos_y += value

    def move_z(self, value):
        self._pos_z -= value

    def rotate_x(self, value):
        self._angle_x_deg += value

    def rotate_y(self, value):
        self._angle_y_deg += value

    def rotate_z(self, value):
        self._angle_z_deg += value
    
    @staticmethod
    def orthographic_project(points, field_of_view_angle_deg, aspect_ratio, far, near):
        field_of_view_angle_rad = math.radians(field_of_view_angle_deg)
        field_of_view = 1.0 / math.tan(field_of_view_angle_rad / 2.0)  

        projection_matrix = np.array([[field_of_view * aspect_ratio, 0, 0, 0],
                                      [0, field_of_view, 0, 0],
                                      [0, 0, (far + near) / (far - near), 1],
                                      [0, 0, (2 * near * far) / (near - far), 0]])

        return np.matmul(points[:,:], projection_matrix)
    
    @staticmethod
    def perspective_division(points, width, height):
        d2_points = np.ones((points.shape[0], 2), dtype=int)

        for i, point in enumerate(points):
            x = point[0]
            y = point[1]
            w = point[3]

            if w > 0:
                new_x = ((x * width) / (2 * w)) + (width / 2)
                new_y = ((y * height) / (2 * w)) + (height / 2)

            else:
                new_x = np.nan
                new_y = np.nan

            d2_point = np.array([new_x, new_y]).astype(int)

            d2_points[i] = d2_point

        return d2_points


    def view(self, model, width, height):
        points = model.points
        points = translate(points, self.pos_x, self.pos_y, self.pos_z)
        points = rotate(points, self.angle_x_deg, self.angle_y_deg, self.angle_z_deg)

        points = self.orthographic_project(points, 
                                           70,
                                           1,
                                           20,
                                           50)

        return self.perspective_division(points, width, height)

        