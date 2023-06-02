from actors import *

from Geometry3D import Point, Vector, ConvexPolyhedron, Renderer

class Sphere (Actors):
    def __init__(self, json) :
        super().__init__(json["sphere"])
        self.center =  Point(
            json["sphere"]["center"]["x"],
            json["sphere"]["center"]["y"],
            json["sphere"]["center"]["z"],
        )
        rayon = json["sphere"]["radius"]
        self.geometry = ConvexPolyhedron.Sphere(self.center,rayon)
    
    def addToPlotTest(self , r : Renderer) :
        r.add((self.geometry, self.color, 1), normal_length=0)