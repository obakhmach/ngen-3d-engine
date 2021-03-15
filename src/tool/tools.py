import numpy as np
import math


def rotate(points, x_angle_deg, y_angle_deg, z_angle_deg):
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

    x_rotated = np.matmul(points[:,:], rotation_matrix_x.T)
    xy_rotated = np.matmul(x_rotated[:,:], rotation_matrix_y.T)

    return np.matmul(xy_rotated[:,:], rotation_matrix_z.T)


def translate(points, x, y, z):
    translation_matrix = np.array([[1, 0, 0, x],
                                   [0, 1, 0, y],
                                   [0, 0, 1, z],
                                   [0, 0, 0, 1]])
    
    # We use tranpont matrix here because we change the order of their multiplication
    # The right order is trans_mtrix * points
    return np.matmul(points[:, :], translation_matrix.T)


def scale(points, x, y, z):
    scale_matrix = np.array([[x, 0, 0, 0],
    	                     [0, y, 0, 0],
    	                     [0, 0, z, 0],
    	                     [0, 0, 0, 1]])
    
    # We use tranpont matrix here because we change the order of their multiplication
    # The right order is trans_mtrix * points
    return np.matmul(points[:, :], scale_matrix.T)