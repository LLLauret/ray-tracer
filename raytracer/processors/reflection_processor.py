from processors.base_processor import *
from interfaces.IForm import IForm
from ray.ray_manufacture import RayManufacture, Ray
from Geometry3D import Vector
from copy import deepcopy

# traite la réflexion avec un nombre de rebond déterminé
class ReflectionProcessor(BaseProcessor) :
    def __init__(self, geometries: List[IForm], manuf_ray: RayManufacture, depth: int = 1) -> None:
        super().__init__()
        self.__geometries : List[IForm] = geometries
        self.__ray_manuf : RayManufacture = manuf_ray
        self.__depth : int = depth

    def setNext(self, handler: IProcessor) -> IProcessor:
        return super().setNext(handler)
    
    def handle(self, hit_result: HitResult) -> Color:
        if self._next_handler is None:
            return hit_result.color

        if hit_result.reflection == 0 and self._next_handler is not None :
            return self._next_handler.handle(hit_result=hit_result)
        
        return self.__recProcessing(current_hit_result=hit_result)
        
    # méthode qui détermine le rayon réfléchit en fonction du rayon incident    
    def __reflectedRay (self, hit_result: HitResult) -> Ray :
        incoming_vec: Vector = Vector(hit_result.ray_origin, hit_result.hit_point).normalized()
        n : Vector = hit_result.normal
        reflected_vec: Vector = incoming_vec - 2*(incoming_vec * n) * n
        reflected_ray = self.__ray_manuf.createRay(hit_result.hit_point, deepcopy(hit_result.hit_point).move(reflected_vec))
        return reflected_ray

    # traitement récursif de la réflexion
    def __recProcessing(self, current_hit_result: HitResult) -> Color :
        # le traitement s'arrête lorsque le nombre de rebond maximal est atteint
        # ou que la surface frappée ne réfléchit plus la lumière
        if current_hit_result.reflection == 0 and (current_hit_result.rebounds >= self.__depth) :
            return current_hit_result.color
        # trouve la géométrie refletée sur la surface actuelle
        reflected_ray = self.__reflectedRay(hit_result=current_hit_result)
        next_hit = self.__nearestReboundHit(ray=reflected_ray, hit_result=current_hit_result)
        # En cas d'intersection :
        if next_hit.hit and self._next_handler is not None :
            # prépare la récursion
            next_hit.rebounds += 1
            # calcul de la prochaine illumination ramené à la reflectivité actuelle : I1*R0
            next_color = self._next_handler.handle(hit_result=next_hit).ratio(current_hit_result.reflection)
            # mélange des couleurs : I = I0 + I1*R0
            next_hit.color = current_hit_result.color.add(next_color)
            # ajustement du ratio de la reflection pour la prochaine étape : R = R0*R1
            next_hit.reflection *= current_hit_result.reflection
            return self.__recProcessing(current_hit_result=next_hit)
        else :
            return current_hit_result.color
        
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
