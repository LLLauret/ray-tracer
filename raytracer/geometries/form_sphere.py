# from interfaces.IForm import *
from .base_form import BaseForm, Color, Ray, HitResult, MatplotlibRenderer
from Geometry3D import Point, Vector, Sphere, distance
from numpy import sqrt
from copy import deepcopy


class FormSphere (BaseForm) : # l'orientation de la sphère n'est pas utilisée pour le moment
    def __init__(self, center: Point, radius: float, color_name: str, shininess: float, reflection: float, transparency: bool, refraction: float, x_angle=0, y_angle=0, z_angle=0) :
        super().__init__(color_name=color_name, shininess=shininess, reflection=reflection, transparency=transparency, refraction=refraction)
        self.__center = center
        self.__radius = radius
        self.__geometry = Sphere(center, radius)
        
    def addToPlotTest(self,r: MatplotlibRenderer):
        r.add((self.__geometry, self._color_name, 1), normal_length=0)
        r.add((self.__center, self._color_name, 10), normal_length=0)
    
    def get_center(self) -> Point:
        return self.__center
    
    # trouve l'intersection la plus proche : -> Point | None
    def __findNearestIntersection(self,ray: Ray) -> Point:
        ray_direction: Vector = ray.direction().normalized()
        ray_origin = ray.origin()
        ray_to_center = Vector(self.__center, ray_origin)
        b = 2 * (ray_direction * ray_to_center)
        c = (ray_to_center.length() ** 2) - (self.__radius ** 2)
        delta = b**2 - 4*c
        # Si delta positif : 2 solutions
        if delta > 0 :
            t1 = (-b + sqrt(delta)) / 2
            t2 = (-b - sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                # on choisit la distance la plus courte
                distance = min(t1, t2)
                point = Point(deepcopy(ray_origin).move(ray_direction * distance))
                return point
            elif t1 > 0 :
                point = Point(deepcopy(ray_origin).move(ray_direction * t1))
                return point
            # else :
            #     point = Point(deepcopy(ray_origin).move(ray_direction * t2))
            #     return point
        return None #type: ignore

    def hit(self, ray: Ray) -> HitResult:
        nearest_intersection : Point = self.__findNearestIntersection(ray)
        if nearest_intersection is None :
            return HitResult(hit=False)
        dist : float = distance(ray.origin(), nearest_intersection)
        normal : Vector = Vector(self.__center,nearest_intersection).normalized()
        return HitResult(hit=True, hit_point=nearest_intersection,ray_origin=ray.origin() ,distance=dist, normal=normal, color=self._color, geometry_ref=self, shininess=self._shininess, reflection=self._reflection, transparency=self._transparency, refraction=self._refraction)
