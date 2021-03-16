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
            field_of_view_angle_deg = 2

        if aspect_ratio is None:
            aspect_ratio = 1

        if near is None:
            near = 20

        if far is None:
            far = 100
   
        self._world = world
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z
        self._pos_x_before = pos_x
        self._pos_y_before = pos_y
        self._pos_z_before = pos_z
        self._angle_x_deg = angle_x_deg
        self._angle_y_deg = angle_y_deg
        self._angle_z_deg = angle_z_deg
        self._angle_x_deg_before = angle_x_deg
        self._angle_y_deg_before = angle_y_deg
        self._angle_z_deg_before = angle_z_deg
        self._field_of_view_angle_deg = field_of_view_angle_deg
        self._aspect_ratio = aspect_ratio
        self._near = near
        self._far = far
        self._prev_transform = None

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
        self._pos_z += value

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

        return np.matmul(points[:,:], projection_matrix.T)
    
    @staticmethod
    def perspective_division(points, width, height):
        d2_points = np.ones((points.shape[0], 2))

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

            d2_point = np.array([new_x, new_y])

            d2_points[i] = d2_point

        return d2_points

    def _calc_rotate_matrix(self, x_angle_deg, y_angle_deg, z_angle_deg):
        x_angle_rad = math.radians(x_angle_deg)
        y_angle_rad = math.radians(y_angle_deg)
        z_angle_rad = math.radians(z_angle_deg)

        rotation_matrix_x = np.array([[1, 0, 0, 0],
                                      [0, math.cos(x_angle_rad), -math.sin(x_angle_rad), 0],
                                      [0, math.sin(x_angle_rad), math.cos(x_angle_rad), 0],
                                      [0, 0, 0, 1]])
    
        rotation_matrix_y = np.array([[math.cos(y_angle_rad), 0, -math.sin(y_angle_rad), 0],
                                      [0, 1, 0, 0],
                                      [math.sin(y_angle_rad), 0, math.cos(y_angle_rad), 0],
                                      [0, 0, 0, 1]])

        rotation_matrix_z = np.array([[math.cos(z_angle_rad), -math.sin(z_angle_rad), 0, 0],
                                      [math.sin(z_angle_rad), math.cos(z_angle_rad), 0, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])

        rotation_matrix_xy = np.matmul(rotation_matrix_x, rotation_matrix_y)

        return np.matmul(rotation_matrix_xy, rotation_matrix_z)

    def _calc_translate_matrix(self, move_x, move_y, move_z):
        return np.array([[1, 0, 0, move_x],
                         [0, 1, 0, move_y],
                         [0, 0, 1, move_z],
                         [0, 0, 0, 1]])


    def view(self, model, width, height):
        delta_x = self._pos_x - self._pos_x_before
        delta_y = self._pos_y - self._pos_y_before
        delta_z = self._pos_z - self._pos_z_before
        delta_angle_x_deg = self._angle_x_deg - self._angle_x_deg_before
        delta_angle_y_deg = self._angle_y_deg - self._angle_y_deg_before
        delta_angle_z_deg = self._angle_z_deg - self._angle_z_deg_before
        points = model.points

        tranlate_matrix = self._calc_translate_matrix(delta_x, delta_y, delta_z)
        rotate_matrix = self._calc_rotate_matrix(delta_angle_x_deg, delta_angle_y_deg, delta_angle_z_deg)

        transform_matrix = np.matmul(rotate_matrix, tranlate_matrix)

        if self._prev_transform is None:
            prev_tranlate_matrix = self._calc_translate_matrix(self._pos_x, self.pos_y, self.pos_z)
            prev_rotate_matrix = self._calc_rotate_matrix(self._angle_x_deg, self._angle_y_deg, self._angle_z_deg)

            self._prev_transform = np.matmul(rotate_matrix, tranlate_matrix)

        transform_matrix = np.matmul(transform_matrix, self._prev_transform)
        points = np.matmul(points[:,:], transform_matrix.T)

        self._prev_transform = transform_matrix

        points = self.orthographic_project(points, 
                                           self._field_of_view_angle_deg,
                                           self._aspect_ratio,
                                           self._far,
                                           self._near)


        self._pos_x_before = self._pos_x
        self._pos_y_before = self._pos_y
        self._pos_z_before = self._pos_z
        self._angle_x_deg_before = self.angle_x_deg
        self._angle_y_deg_before = self.angle_y_deg
        self._angle_z_deg_before = self.angle_z_deg

        return self.perspective_division(points, width, height)

        