from Geometry3D import Point, Vector, HalfLine, Segment
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from Geometry3D.calc import distance

class Ray :
    def __init__ (self, origin:Point, point:Point) :
        self.__origin = origin
        self.__point = point
        

    def addToTestPlot (self, r:MatplotlibRenderer, color:str) :
        r.add(((Segment(self.__origin, self.__point)),color, 1))

    # méthode qui est utilisée pour les intersections avec les modèles de la librairie
    def toHalfLine (self) -> HalfLine :
        return HalfLine(self.__origin, Vector(self.__origin, self.__point))
    
    def direction(self) -> Vector :
        return Vector(self.__origin, self.__point)

    def origin(self) -> Point :
        return self.__origin
    
    # retourne la longueur d'un rayon
    def norm(self) -> float :
        return distance(self.__origin, self.__point)
    