from .base_form import BaseForm,Ray,Color,HitResult
from Geometry3D import Point,Vector, HalfLine, x_unit_vector, z_unit_vector, y_unit_vector, ConvexPolygon, ConvexPolyhedron,Parallelepiped, distance
from typing import List
from Geometry3D.calc.intersection import inter_convexpolygon_halfline
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from pygame import math as pgm
from copy import deepcopy

class FormCube (BaseForm) :
    def __init__(self,length : float, center:Point, color_name: str, shininess: float, reflection: float, transparency: bool, refraction: float, x_angle=0, y_angle=0, z_angle=0) :
        super().__init__(color_name=color_name, shininess=shininess, reflection=reflection, transparency=transparency, refraction=refraction)
        self.__length = length
        # détermination du point de base pour la création du parallelepipede
        basePoint = self.__findBasePoint(center=deepcopy(center), length=length)
        # vecteurs guides pour la création du Parallelepipede
        v1,v2,v3 = self.__findBaseVectors(x=x_angle,y=y_angle,z=z_angle, length=length)
        geometry : ConvexPolyhedron = Parallelepiped(base_point=basePoint, v1=v1, v2=v2, v3=v3)
        # déplacement du cube selon le centre souhaité
        actual_center = geometry.center_point
        moving_vector = Vector(actual_center, center)
        for plg in geometry.convex_polygons :
            plg.move(moving_vector)

        self.__center = center
        self.__faces : List[ConvexPolygon] = geometry.convex_polygons #type: ignore
        
    
    def __findBasePoint(self,center:Point, length: float) -> Point :
        dist = length / 2
        center.move(y_unit_vector() * -dist)
        center.move(z_unit_vector() * -dist)
        center.move(x_unit_vector() * -dist)
        return center

    def __findBaseVectors(self,x:float, y:float, z:float, length: float) -> tuple[Vector,Vector,Vector]:
        # vecteurs normalisés de bases
        vx = pgm.Vector3(1,0,0)
        vy = pgm.Vector3(0,1,0)
        vz = pgm.Vector3(0,0,1)
        
        # rotations des vecteurs selon les angles souhaités
        # PyGames.Vector3 n'a pas la même norme de repère que Geometry3D.Vector
        # rotation sur l'axe des z :
        vx.rotate_z_ip(y)
        vy.rotate_z_ip(y)
        vz = vx.cross(vy)
        #rotation sur l'axe des x :
        vz.rotate_x_ip(x)
        vy.rotate_x_ip(x)
        vx.rotate_x_ip(x)
        #rotation sur l'axe des y :
        vz.rotate_y_ip(z)
        vx.rotate_y_ip(z)
        vy.rotate_y_ip(z) 

        # adaptation des Vector3 -> Vector, pour utiliser Geometry3D
        v1 = self.__Vector3toVector(vec=vx, l=length)
        v2 = self.__Vector3toVector(vec=vy, l=length) 
        v3 = self.__Vector3toVector(vec=vz, l=length)
        
        return v1,v2,v3
        
    def addToPlotTest(self,r: MatplotlibRenderer):
        r.add((ConvexPolyhedron(self.__faces), self._color_name, 1), normal_length=0)
        r.add((self.__center, self._color_name, 10), normal_length=0)

    def __Vector3toVector(self, vec:pgm.Vector3, l: float) -> Vector :
        vec.scale_to_length(l)
        return Vector(vec.x, -vec.z, vec.y) #type: ignore
    
    # Trouve l'intersection la plus proche avec le rayon, -> tuple[Point, ConvexPolygon] | None
    def __findNearestIntersection (self, half_line:HalfLine) -> tuple[Point, ConvexPolygon] :
        # la mémoization a été retirée car elle cause des artefacts au rendu
        nearest_hit : tuple[Point, ConvexPolygon] = None #type: ignore
        for cpg in self.__faces :
            # test des intersections renvoie None | Point
            point = inter_convexpolygon_halfline(cpg=cpg, h=half_line)
            if isinstance(point,Point) :
                if nearest_hit is None or distance(point, half_line.point) < (distance(nearest_hit[0],half_line.point)) : 
                    nearest_hit = (point, cpg)
                    # on sauve le dernier polygon atteint (memoization) - retirée
        return nearest_hit

    def hit(self, ray: Ray) -> HitResult:
        intersection : tuple[Point, ConvexPolygon] = self.__findNearestIntersection(ray.toHalfLine())
        if intersection is None :
            return (HitResult(hit=False))
        # sinon il y a intersection en un point :
        pt : Point = intersection[0]
        dist = distance(ray.origin(), pt)
        face : ConvexPolygon = intersection[1]
        normal : Vector = (face.plane.n).normalized()
        color : Color = self._color

        return HitResult(hit=True, hit_point=pt, ray_origin=ray.origin(), distance=dist, normal=normal, color=color, geometry_ref=self, reflection=self._reflection, shininess=self._shininess, transparency=self._transparency, refraction=self._refraction)