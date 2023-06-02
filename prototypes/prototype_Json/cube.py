from Geometry3D import Point, Vector, Renderer, ConvexPolyhedron
from math import radians, cos, sin
from actors import *

class Cube(Actors) :
    def __init__(self, json:object) -> None:
        super().__init__(json["cube"])
        self.position = Point(
            json["cube"]["origin"]["x"],
            json["cube"]["origin"]["y"],
            json["cube"]["origin"]["z"],
        )
        longueur = json["cube"]["length"]
        #calculer l'orientation préalablement
        self.geometry = ConvexPolyhedron.Parallelepiped(
            self.position,
            Vector(longueur,0,0),
            Vector(0,longueur,0),
            Vector(0,0,longueur)
            )
    
    def addToPlotTest(self , r: Renderer) :
        r.add((self.geometry, self.color, 1), normal_length=0)