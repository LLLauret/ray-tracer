from viewport.viewport import *
from pygame.math import Vector3
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from Geometry3D import Vector, z_unit_vector, Segment
from math import radians, tan

class Camera :

    def __init__(self,position : Point, azimuth : float, elevation : float, distance:float, fov: float) :
        self.__position = position
        self.__focal = distance
        x_angle = azimuth
        y_angle = elevation
        self.__fov = radians(fov)
        self.__direction : Vector = self.__findDirection(x_angle, y_angle)

    def __str__(self) -> str:
        return ("Camera : x:{0} , y:{1}, direction = {2}, distance focale :{3}".format(self.__position.x,self.__position.y, self.__direction, self.__focal))

    # permet de déterminer la position des coins du viewport
    def __calculateCornerPoint(self, ratio : float, cadranW : int, cadranH : int) -> Point :
        semi_width = self.__focal * tan(self.__fov/2)
        semi_height = semi_width / ratio
        dirN = self.__direction.normalized()
        vecRight = dirN.cross(z_unit_vector()).normalized()
        vecUp = vecRight.cross(dirN).normalized()
        cornerPoint = copy.deepcopy(self.__position)
        cornerPoint.move(cadranW * semi_width * vecRight)  
        cornerPoint.move(cadranH * semi_height * vecUp)
        cornerPoint.move(self.__direction * self.__focal)
        return cornerPoint

    # retourne un viewport
    def createViewPort(self, width: int, height:int) ->  Viewport :
        ratio = width / height
        cornerTR = self.__calculateCornerPoint(ratio, 1, 1)
        cornerTL = self.__calculateCornerPoint(ratio, -1, 1)
        cornerBR = self.__calculateCornerPoint(ratio, 1, -1)
        cornerBL = self.__calculateCornerPoint(ratio, -1, -1)

        # Test de perpendicularite
        dirN = self.__direction.normalized()
        sontOrthosH = dirN.orthogonal((Vector(cornerTL,cornerBL).normalized()))
        sontOrthosW = dirN.orthogonal((Vector(cornerTR,cornerTL).normalized()))
        return Viewport(width=width, height=height, pts=[cornerTL, cornerTR, cornerBL, cornerBR])

    def addToTestPlot (self, r: MatplotlibRenderer, color: str) :
        r.add((Point(self.__position), color, 10), normal_length = 1)
        r.add((Segment(self.__position, self.__direction), color, 2), normal_length = 0)

    def __findDirection (self,azimuth:float, elevation: float) -> Vector:
        vec = Vector3(0,0,1)
        vec.rotate_y_ip(azimuth)
        vec.rotate_x_ip(-elevation)
        return Vector(vec.x,vec.z,vec.y)
    
    def position(self) -> Point :
        return self.__position 

    