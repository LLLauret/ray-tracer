from copy import deepcopy
from .base_processor import BaseProcessor, Color, HitResult, List, IProcessor
from interfaces.IForm import IForm
from ray.ray_manufacture import RayManufacture,Ray
from Geometry3D import Point, Vector, x_unit_vector, y_unit_vector
from math import pow

class OcclusionProcessor (BaseProcessor) :
    def __init__(self, geometries : List[IForm],ray_manuf: RayManufacture, min_distance: float = 0.01) -> None:
        super().__init__()
        self.__geometries : List[IForm] = geometries
        self.__ray_manuf : RayManufacture = ray_manuf 
        self.__min_distance : float = min_distance
    
    def setNext(self, handler: IProcessor) -> IProcessor:
        return super().setNext(handler)
    
    def handle(self, hit_result: HitResult) -> Color:
        
        # détermine le ratio d'occlusion et 
        occlusion_ratio = self.__occlusionRatio(hit_result=hit_result)
        
        if occlusion_ratio != 0 :
            # print (f"occlusion appearing : {occlusion_ratio} , {hit_result.geometry}")
            hit_result.color = hit_result.color.ratio( 1 - occlusion_ratio )
        
        if self._next_handler is not None :    
            return self._next_handler.handle(hit_result=hit_result)
        
        return hit_result.color

    # détermine le ratio d'occlusion
    def __occlusionRatio(self, hit_result : HitResult) -> float :
        result = 0
        ray_index: int = 0
        occlusion_rays : List[Ray] = self.__occlusionRays(hit_result.hit_point, hit_result.normal)
        if ray_index > 4 and occlusion_rays.__len__() == 0 :
            return 0
        for r in occlusion_rays :
            for g in self.__geometries : 
                if g == hit_result.geometry :
                    continue
                hit = g.hit(ray=r)
                if (hit.distance <= self.__min_distance) :
                    result += 1
        
        return result / occlusion_rays.__len__()
    
    # crée la liste des rayons secondaires
    def __occlusionRays (self, origin : Point, normal: Vector) -> List[Ray] :
        ray_list : List[Ray] = [ ]
        vector_list : List[Vector] = self.__findVectors(normal=normal)
        
        # instanciation des rayons
        for v in vector_list : 
            ray_list.append(self.__ray_manuf.createRay(origin=origin, through=deepcopy(origin).move(v=v)))
        
        return ray_list
    
    # trouve la direction des rayons secondaires
    def __findVectors (self, normal : Vector) -> List[Vector] :

        vector_list : List[Vector] = [ ]

        n : Vector = normal.normalized()
        
        side_v = n.cross(x_unit_vector())
        # il se peut que le cross product ne fonctionne pas 
        # si la normale est déjà dans la direction de l'axe x
        try :
            side_v : Vector = side_v.normalized()
        except :
            side_v = n.cross(y_unit_vector())
            side_v = side_v.normalized()

        # vecteur perpendiculaire à la normale et à side_v
        orth_side_v = side_v.cross(n).normalized()
        opposite_side_v = side_v * (-1)
        opposite_orth_side_v = orth_side_v * (-1)

        # vecteurs de bases
        vector_list.append(n)
        vector_list.append(side_v)
        vector_list.append(orth_side_v)
        vector_list.append(opposite_side_v)
        vector_list.append(opposite_orth_side_v)
        
        # vecteurs à 45 degres de la normal    
        vector_list.append((opposite_side_v + n).normalized())
        vector_list.append((side_v + n).normalized())
        vector_list.append((orth_side_v + n).normalized())
        vector_list.append((opposite_orth_side_v + n).normalized())

        # vecteurs intermédiaires orthogonaux à la normales
        # vector_list.append((side_v + orth_side_v).normalized())
        # vector_list.append((side_v + opposite_orth_side_v).normalized())
        # vector_list.append((opposite_side_v + orth_side_v).normalized())
        # vector_list.append((opposite_side_v + opposite_orth_side_v).normalized())

        return vector_list