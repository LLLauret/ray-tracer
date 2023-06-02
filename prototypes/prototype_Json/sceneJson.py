import json
import math as Math
from camera import Camera 
from cube import *
from sphere import *
from Geometry3D import Renderer, Point, Vector, Segment, Parallelepiped

jsonFile = open(file="scene.json")
jsonData = json.loads(jsonFile.read())

c = Camera(jsonData["scene"]["camera"])
#cube = Parallelepiped(Point(2.5,10,2.5), Vector(5,0,0), Vector(0,5,0), Vector(0,0,5))
cube = Cube(jsonData["scene"]["geometries"][0])
sphere = Sphere(jsonData["scene"]["geometries"][1])
r = Renderer()
c.addToTestPlot(r)
cube.addToPlotTest(r)
sphere.addToPlotTest(r)
#r.add((cube, 'green', 1), normal_length=10)

print(c)

r.show()