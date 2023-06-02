from copy import deepcopy
from .base_processor import *
from ray.ray_manufacture import *
from math import sqrt, pow
from Geometry3D.utils import get_eps
from interfaces.IForm import IForm

class SimpleRefractionProcessor (BaseProcessor) :
    def __init__(self, ray_manuf : RayManufacture, geometries: List[IForm]) -> None:
        super().__init__()
        self.__ray_manuf = ray_manuf
        self.__geometries : List[IForm] = geometries
    
    
    def handle(self, hit_result: HitResult) -> Color:
        
        if not hit_result.transparency and self._next_handler is not None :
            return self._next_handler.handle(hit_result=hit_result)
        
        if (hit_result.reflection != 0) and self._next_handler is not None :
            hit_result.color = hit_result.color.add(self._next_handler.handle(hit_result=hit_result))

            # rayon qui traverse la geométrie
            refracted_ray : Ray = self.__refractedRay(hit_result=hit_result,n_from=1, n_to=hit_result.refraction)
            
            # hitResult qui révèle le point de sortie de la géométrie.
            refracted_end_hit : HitResult = hit_result.geometry.hit(refracted_ray)
            refracted_end_hit.camera_position = hit_result.camera_position
            refracted_end_hit.rebounds = hit_result.rebounds

            # cas limite qui se produit avec le cube, à cause de la librairie
            if not refracted_end_hit.hit : 
                return hit_result.color
            
            try :
                # rayon qui ressort de la géométrie est refracté de nouveau
                outgoing_ray : Ray = self.__refractedRay(hit_result=refracted_end_hit,n_from= hit_result.refraction, n_to=1)
            
            # en cas de réflexion totale
            except :
                # on utilise la direction de la première réfraction pour sortir de la géométrie
                outgoing_ray : Ray = refracted_ray
            
            # ray-casting avec outgoing_ray
            nearest_hit = self.__nearestReboundHit(ray=outgoing_ray, hit_result=refracted_end_hit)
            next_color : Color = self._next_handler.handle(nearest_hit)
            hit_result.color = hit_result.color.add(next_color.ratio(1 - hit_result.reflection))
            return hit_result.color
            
            
    def __refractedRay(self, hit_result: HitResult, n_from: float, n_to: float) -> Ray :
        # formule issue de wikipedia
        refraction_ratio : float = n_from / n_to
        incident_ray : Vector = Vector(hit_result.ray_origin, hit_result.hit_point).normalized()
        
        cos_incident : float = hit_result.normal * incident_ray * (-1)

        cos_refracted : float = sqrt( 1 - pow(refraction_ratio,2) * (1 - pow(cos_incident,2)))
        
        a : Vector = refraction_ratio * incident_ray
        if cos_incident < 0 :
            cos_refracted *= -1
        b : Vector = (refraction_ratio * cos_incident - cos_refracted) * hit_result.normal
        direction = a + b
        #get_eps(), n'a pas l'air d'être suffisant avec les modèles de la librairie Geometry3D, il ne fait pas de différence
        shifted_hit_point = deepcopy(hit_result.hit_point).move(incident_ray * get_eps() * 100) 
        refracted_ray = self.__ray_manuf.createRay(origin=shifted_hit_point, through=deepcopy(shifted_hit_point).move(direction))
        return refracted_ray
    
    # vérifie l'intersection la plus proche pour un rayon donné    
    def __nearestReboundHit(self, ray: Ray, hit_result: HitResult) -> HitResult :
        rebound_hit = HitResult(hit=False)
        for g in self.__geometries :
            if g is hit_result.geometry :
                continue # on ne fait pas de test pour la géométrie concernée par le hit_result
            temp = g.hit(ray)
            if temp.hit is True and temp.distance < rebound_hit.distance :
                rebound_hit = temp
        # on renseigne la position de la caméra dans le rebond
        rebound_hit.camera_position = deepcopy(hit_result.camera_position)
        rebound_hit.rebounds = deepcopy(hit_result.rebounds)
        return rebound_hit