import numpy as np


def calc_rotation_matrix(x_angle_deg, y_angle_deg, z_angle_deg):
    x_angle_rad = np.radians(x_angle_deg)
    y_angle_rad = np.radians(y_angle_deg)
    z_angle_rad = np.radians(z_angle_deg)

    rotation_matrix_x = np.array([[1, 0, 0, 0],
                                  [0, np.cos(x_angle_rad), -np.sin(x_angle_rad), 0],
                                  [0, np.sin(x_angle_rad), np.cos(x_angle_rad), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_y = np.array([[np.cos(y_angle_rad), 0, -np.sin(y_angle_rad), 0],
                                  [0, 1, 0, 0],
                                  [np.sin(y_angle_rad), 0, np.cos(y_angle_rad), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_z = np.array([[np.cos(z_angle_rad), -np.sin(z_angle_rad), 0, 0],
                                  [np.sin(z_angle_rad), np.cos(z_angle_rad), 0, 0],
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
    field_of_view_angle_rad = np.radians(field_of_view_angle_deg)
    field_of_view = 1.0 / np.tan(field_of_view_angle_rad / 2.0)  

    return np.array([[field_of_view * aspect_ratio, 0, 0, 0],
                     [0, field_of_view, 0, 0],
                     [0, 0, (far + near) / (far - near), 1],
                     [0, 0, (2 * near * far) / (near - far), 0]])


def normals_to_degrees(normals):
    # The normal is the projection of the sinle sized vector on the each of coordinates.
    # So the normal_x =  single_size_vector_scalar * cos(angle_to_x_axe) = 1 * cos(angle_to_x_axe)
    # So the normal_x = cos(angle_to_x_axe).
    # So the angle_to_x_axe_degrees = degrees(arccos(angle_to_x_axe))
    return np.degrees(np.arccos(normals[:,:]))


def degrees_to_normals(degrees):
    # The normal is the projection of the sinle sized vector on the each of coordinates.
    # So the normal_x =  single_size_vector_scalar * cos(angle_to_x_axe) = 1 * cos(angle_to_x_axe)
    # So the normal_x = cos(angle_to_x_axe).
    # So the angle_to_x_axe_degrees = degrees(arccos(angle_to_x_axe))
    return np.round(np.cos(np.radians(degrees[:,:])), 3)


def parametrical_line_point(point, normal, distance):
    normal_a = normal[0]
    normal_b = normal[1]
    normal_c = normal[2]
    x = point[0]
    y = point[1]
    z = point[2]

    new_point_x = x + normal_a * distance 
    new_point_y = y + normal_b * distance 
    new_point_z = z + normal_c * distance 

    return np.array([new_point_x, new_point_y, new_point_z, 1])