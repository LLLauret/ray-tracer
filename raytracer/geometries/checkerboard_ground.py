from .base_form import BaseForm,Color,HitResult,Ray,MatplotlibRenderer
from Geometry3D import Point, Segment, Vector,ConvexPolygon,Parallelogram, x_unit_vector, y_unit_vector, z_unit_vector, distance
from Geometry3D.calc.intersection import inter_convexpolygon_halfline

# Représentation du sol en damier
class CheckerBoardGround (BaseForm) :
    def __init__(self, base_p: Point, length: float, width: float, color_name: str, shininess: float, reflection: float, orientation:str='horizontal') -> None:
        super().__init__(color_name=color_name,shininess=shininess,reflection=reflection)
        self.__base_p: Point = base_p
        self.__width: float = width
        self.__length: float = length
        v1, v2 = self.__findVectors(orientation, width=width, length=length)
        self.__surface : ConvexPolygon = Parallelogram(base_point=base_p, v1=v1, v2=v2)
    
    def hit(self, ray: Ray) -> HitResult:
        half_line = ray.toHalfLine()
        intersection : Point = inter_convexpolygon_halfline(self.__surface,half_line)
        ray_origin = ray.origin()
        if intersection is None :
            return HitResult(hit=False)
        # lorsqu'il s'agit d'un plan, l'intersection d'une ligne peut être un segment
        if isinstance(intersection, Segment) :
            intersection = intersection.start_point if distance(intersection.start_point, ray_origin) < distance(intersection.end_point,ray_origin) else intersection.end_point 
        
        dist = distance(ray_origin, intersection)
        n : Vector = self.__surface.plane.n
        color = self.__damierColor(point=intersection)
        return HitResult(hit=True, hit_point=intersection, ray_origin=ray_origin, distance=dist, normal=n,color=color,geometry_ref=self, shininess=self._shininess, reflection=self._reflection)

    def addToPlotTest(self, r: MatplotlibRenderer):
        #r.add((self.__surface, self.__color_name,1),normal_length=10)
        pass
    
    def __findVectors(self, location: str, width: float, length: float) -> tuple[Vector,Vector] :
        v1: Vector = x_unit_vector() * width
        v2: Vector = y_unit_vector() * length
        if (location == 'vertical') :
            v1 = z_unit_vector() * width
        return v1,v2

    # détermine la couleur à renvoyer en fonction du point sur le plan
    def __damierColor (self, point: Point) -> Color :
        x_dist = abs(point.x - self.__base_p.x)
        y_dist = abs(point.y - self.__base_p.y)
        x_step = self.__width / 20
        y_step = self.__length / 20
        nb_x = x_dist // x_step
        nb_y = y_dist // y_step
        # l'aspect binaire du damier permet de retrouver facilement la couleur 
        # en fonction du nombre de carreaux parcourus
        if (nb_x + nb_y) % 2 == 0 :
            return Color.fromName('black')
        return self._color