import numpy as np
import re


class SimpleObjParser:
    def __init__(self, path):
        self._path = path
        self._comments = []

    def parse(self):
        vertexes = []
        surfaces = []
        normals = []

        comment_regex = re.compile('^# (.*)')
        surface_regex = re.compile('^f (.*)')
        normal_regex = re.compile('^vn (.*)')
        vertex_regex = re.compile('^v (.*)')
        name_regex = re.compile('^g (.*)')

        with open(self._path) as f:
            lines = f.readlines()

            self._comments.append(lines)

        for line in lines:
            if comment_regex.match(line):
        	    pass

            elif surface_regex.match(line):
                if '//' in line:
                    surface = np.array([np.array([float(v.replace('/n', '')) for v in surface.split('//')]) 
                                            for surface 
                                            in line.split(' ')[1:] 
                                            if surface not in ['', '\n']], dtype=np.float)
                else:
                    surface = np.array([np.array([float(v.replace('/n', '')) for v in surface.split('/')]) 
                                            for surface 
                                            in line.split(' ')[1:] 
                                            if surface not in ['', '\n']], dtype=np.float)

                surfaces.append(surface)

            elif normal_regex.match(line):
                normal = np.array([float(normal.replace('/n', '')) 
                                       for normal 
                                       in line.split(' ')[1:] 
                                       if normal not in ['', '\n']], dtype=np.float)

                normals.append(normal)

            elif vertex_regex.match(line):
                vertex = [float(vertex.replace('/n', '')) 
                          for vertex 
                          in line.split(' ')[1:] 
                          if vertex not in ['', '\n']]

                vertex.append(1)

                vertex = np.array(vertex, dtype=np.float)

                vertexes.append(vertex)

            elif name_regex.match(line):
                self._name = line

        vertexes = np.array(vertexes)
        normals = np.array(normals)
        surfaces = np.array(surfaces)

        return vertexes, normals, surfaces
