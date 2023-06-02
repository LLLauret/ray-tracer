from Geometry3D import Vector, Renderer

from math import radians, cos, sin

class Actors :
    def __init__(self, json:object) -> None:
        x = radians(json["orientation"]["x"])
        y = radians(json["orientation"]["y"])
        z = radians(json["orientation"]["z"])
        self.direction = Vector(x,y,z)
        self.color = json["color"]

