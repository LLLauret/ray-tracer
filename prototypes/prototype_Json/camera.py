from Geometry3D import Point, Vector, Segment, Renderer
import math as Math

class Camera :
    def __init__(self, json:object) -> None:
        self.position = Point(
            json["position"]["x"],
            json["position"]["y"],
            json["position"]["z"],
        )
        hor = json["direction"]["horizontal"]
        hor = Math.radians(hor)
        ver = json["direction"]["vertical"]
        ver = Math.radians(ver)
        y = Math.cos(hor) * Math.cos(ver)
        x = Math.sin(hor) * Math.cos(ver)
        z = Math.sin(ver)
        self.focal = json["focal"]
        self.direction = Vector(x,y,z) * self.focal

    def __str__(self) -> str:
        return ("Camera : x:{0} , y:{1}, direction = {2}, distance focale :{3}".format(self.position.x,self.position.y, self.direction, self.focal))

    def addToTestPlot (self, r : Renderer) :
        r.add((Point(self.position), 'red', 10), normal_length = 1)
        r.add((Segment(self.position, self.direction), 'red', 2), normal_length = 0)
