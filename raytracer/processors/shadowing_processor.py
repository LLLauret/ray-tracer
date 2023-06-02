from processors.base_processor import *
from interfaces.IForm import IForm
from ray.ray_manufacture import *
from Geometry3D.utils import get_eps

class ShadowingProcessor (BaseProcessor) : 
    def __init__(self, light_position: List[Point], geometries: List[IForm], manuf_ray: RayManufacture) -> None:
        super().__init__()
        self.__light_position : List[Point] = light_position
        self.__geometries : List[IForm] = geometries
        self._manuf : RayManufacture = manuf_ray
    
    def setNext(self, handler: IProcessor) -> IProcessor:
        return super().setNext(handler)
    
    def handle(self, hit_result: HitResult) -> Color:
        # test d'ombrage
        hit_result.shadowed = self.__isShadowedFromAllLights(hit_result=hit_result)
        # délègue le traitement au calcul de l'illumination
        if self._next_handler is not None :
            return self._next_handler.handle(hit_result=hit_result)
        
        # retourne une valeur si il n'y a pas de noeud suivant
        return self.__fakeShadowingProcessing(hit_result=hit_result, ratio=0.3)

    # verifie si le point est illuminé ou dans l'ombre
    def __isShadowed(self, ray: Ray) -> bool :
        light_to_hit_distance = ray.norm()
        for g in self.__geometries :
            # il faut ajouter un epsilon pour éviter l'acnée de l'ombre
            if g.hit(ray).distance + get_eps()  < light_to_hit_distance :
                return True
        return False
    
    # vérifie si le point d'intersection est à l'abris de toute les sources de lumière 
    def __isShadowedFromAllLights(self, hit_result: HitResult) -> bool :
        result : bool = False
        for l in self.__light_position :
            raylight = self._manuf.createRay(l,hit_result.hit_point)
            result = self.__isShadowed(ray=raylight)
            # on ajoute les sources qui illuminent l'objet
            if result is False :
                hit_result.light_point.append(l)
        return result
    
    # méthode qui calcule la couleur sans éclairage
    def __fakeShadowingProcessing (self, hit_result: HitResult, ratio : float) -> Color :
        new_color: Color = hit_result.color.ratio(ratio)
        return new_color