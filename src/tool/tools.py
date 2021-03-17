import numpy as np
import math

def calc_rotation_matrix(x_angle_deg, y_angle_deg, z_angle_deg):
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

def calc_translation_matrix(move_x, move_y, move_z):
    return np.array([[1, 0, 0, move_x],
                     [0, 1, 0, move_y],
                     [0, 0, 1, move_z],
                     [0, 0, 0, 1]])


def calc_scaling_matrix(x, y, z):
    return np.array([[x, 0, 0, 0],
    	             [0, y, 0, 0],
    	             [0, 0, z, 0],
    	             [0, 0, 0, 1]])

def calc_projection_matrix(field_of_view_angle_deg, aspect_ratio, far, near):
    field_of_view_angle_rad = math.radians(field_of_view_angle_deg)
    field_of_view = 1.0 / math.tan(field_of_view_angle_rad / 2.0)  

    return np.array([[field_of_view * aspect_ratio, 0, 0, 0],
                     [0, field_of_view, 0, 0],
                     [0, 0, (far + near) / (far - near), 1],
                     [0, 0, (2 * near * far) / (near - far), 0]])