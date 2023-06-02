# from interfaces.IForm import *
from .base_form import BaseForm,Color,HitResult,Ray,MatplotlibRenderer
from Geometry3D import Point, Vector, ConvexPolygon, Parallelogram, x_unit_vector, y_unit_vector,  z_unit_vector, distance
from Geometry3D.calc.intersection import inter_convexpolygon_halfline
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer

# pour le moment cette classe n'est pas utilisée, mais elle sera sans doute utilisée pour créer les murs
class Surface (BaseForm) :
    def __init__(self, base_p: Point, length: float, width: float, color_name: str, shininess: float, transparency: float, reflection: float, orientation:str='horizontal') -> None:
        super().__init__(color_name=color_name, shininess=shininess, reflection=reflection, transparency=transparency)
        self.__base_p: Point = base_p
        self.__width: float = width
        self.__length: float = length
        v1, v2 = self.__findVectors(orientation, width=width, length=length)
        self.__surface : ConvexPolygon = Parallelogram(base_point=base_p, v1=v1, v2=v2)
    
    def hit(self, ray: Ray) -> HitResult:
        half_line = ray.toHalfLine()
        intersection : Point = inter_convexpolygon_halfline(self.__surface,half_line)
        if intersection is None :
            return HitResult(hit=False)
        ray_origin = ray.origin()
        dist = distance(ray_origin, intersection)
        n : Vector = self.__surface.plane.n
        return HitResult(hit=True,hit_point=intersection,ray_origin=ray.origin(), distance=dist, normal=n,color=self._color,geometry_ref=self, shininess=self._shininess, reflection=self._reflection, transparency=self._transparency)

    def addToPlotTest(self, r: MatplotlibRenderer):
        #r.add((self.__surface, self.__color_name,1),normal_length=10)
        pass
    
    def __findVectors(self, location: str, width: float, length: float) -> tuple[Vector,Vector] :
        v1: Vector = x_unit_vector() * width
        v2: Vector = y_unit_vector() * length
        if (location == 'vertical') :
            v1 = z_unit_vector() * width
        return v1,v2

