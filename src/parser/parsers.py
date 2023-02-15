import re
import numpy as np

from abc import ABC
from enum import Enum
from typing import Pattern, List, Tuple
from numpy.typing import NDArray
from dataclasses import dataclass


@dataclass
class ObjParsed:
    """Class to keep all data describing specific
    obj model. Class cover only data related to the
    shape of the model ignoring model texture.
    """

    vertexes: NDArray
    normals: NDArray
    surfaces: NDArray


class ObjParser(ABC):
    def parse(self) -> ObjParsed:
        """Reads the vertices, normals and surfaces.

        Returns:
            ObjParsed: The dataclass with the data.
        """


class SimpleObjParser(ObjParser):
    """The simple class to parse obj files."""

    _path: str
    _vertices_pattern: Pattern
    _normals_pattern: Pattern
    _surfaces_pattern: Pattern

    class ObjFileStatements(Enum):
        """The regular expressions to parse the
        .obj file.
        """

        VERTICES: str = r"v\s*(-?[0-9]*\.\d+|-?\d+)\s*(-?[0-9]*\.\d+|-?\d+)\s*(-?[0-9]*\.\d+|-?\d+)"
        NORMALS: str = r"vn\s*(-?[0-9]*\.\d+|-?\d+)\s*(-?[0-9]*\.\d+|-?\d+)\s*(-?[0-9]*\.\d+|-?\d+)"
        SURFACES: str = (
            r"f\s*([0-9]*/[0-9]{0,}/[0-9]*)\s*([0-9]*/[0-9]{0,}/[0-9]*)"
            r"\s*([0-9]*/[0-9]{0,}/[0-9]*)"
        )

    def __init__(self, path: str) -> None:
        """The constructor used to inject path to
        the parser.

        Args:
            path (str): The path where .obj file located.

        Returns:
            None
        """
        self._path = path
        self._vertices_pattern = re.compile(self.ObjFileStatements.VERTICES.value)
        self._normals_pattern = re.compile(self.ObjFileStatements.NORMALS.value)
        self._surfaces_pattern = re.compile(self.ObjFileStatements.SURFACES.value)

    def _surface_statement2list(self, statement: Tuple[str]) -> List[List[int]]:
        """Transform parsed by regex surface .obj statement into
        the valid numpy.

        Args:
            statement (Tuple[str]): The statement parsed within the
                                    .obj surfaces regex. The statement
                                    example ("2//1",  "8//1",  "4//1"),
                                    ("6/4/1", "3/5/3", "7/6/5")

        Returns:
            List[List[int]]: The statement as list of three lists.
                             Example [[vertice1, normal1],
                             [vertice2, normal2], [vertice3, normal3]]
        """

        def map_function(statement_item) -> List[int]:
            """Helper map function to extract for each
            statement element (example "1//2", "1/1/1")
            only first and last number and return as a list.

            Returns:
                List[int]: The list like vertice, normal]
            """
            splited = statement_item.split("/")

            return [splited[0], splited[-1]]

        return list(map(map_function, statement))

    def parse(self) -> ObjParsed:
        """Reads the .obj file and create
        the ObjParsed dataclass based on the data in the file.

        Returns:
            ObjParsed: The dataclass with the data from the .obj file.
        """
        with open(self._path, "r") as f:
            obj_file_content = f.read()

        vertices = np.array(
            self._vertices_pattern.findall(obj_file_content), dtype=float
        )

        vertexes = np.ones((vertices.shape[0], 4), dtype=float)
        vertexes[:,0:3] = vertices


        normals = np.array(
            self._normals_pattern.findall(obj_file_content), dtype=float
        )

        normalst = np.ones((normals.shape[0], 4), dtype=float)
        normalst[:,0:3] = normals

        surfaces = np.array(
            list(
                map(
                    self._surface_statement2list,
                    self._surfaces_pattern.findall(obj_file_content),
                )
            ),
            dtype=int,
        )

        return ObjParsed(vertexes=vertexes, normals=normalst, surfaces=surfaces)

