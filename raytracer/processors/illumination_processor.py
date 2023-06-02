from processors.base_processor import *
from ray.ray_manufacture import *
from Geometry3D import Vector
import numpy as np

# traite l'illumination à un point 
class IlluminationProcessor (BaseProcessor) :
    def __init__(self, manuf_ray: RayManufacture) -> None:
        super().__init__()
        self._manuf : RayManufacture = manuf_ray
        
    def setNext(self, handler: IProcessor) -> IProcessor:
        return super().setNext(handler)
    
    def handle(self, hit_result: HitResult) -> Color:
        # condition permet de s'assurer que le calcul d'illumination 
        # ne se fait qu'une fois par hit_result
        if not hit_result.illumination_processed :
            hit_result.color = self.__IlluminationProcessingAllLights(hit_result=hit_result)
            hit_result.illumination_processed = True

        # if (hit_result.reflection != 0 or hit_result.transparency != 0) and self._next_handler is not None:
        if  self._next_handler is not None:
            return self._next_handler.handle(hit_result=hit_result)
        
        return hit_result.color
    
    
    # détermine la couleur du pixel au point d'intersection
    def __IlluminationProcessingAllLights(self, hit_result: HitResult) -> Color :
        
        # Composantes
        ka = hit_result.color.toUnitNpArray(ratio=0.25) if hit_result.shadowed else hit_result.color.toUnitNpArray(ratio=0.3)# ambiant
        kd = hit_result.color.toUnitNpArray(ratio=0.7)# diffuse    
        ks = np.ones(3) # speculaire
        
        if hit_result.transparency : # les caractéristiques pour un objet transparent ne sont pas les mêmes
            ka = hit_result.color.toUnitNpArray(ratio = 0.1)
            kd = hit_result.color.toUnitNpArray(ratio = 0.2)
            pass
        # calcul : ka + Somme de 1 à n [kd(Ln . N) + ks(R . V)^shininess
        illumination = ka
        hit_to_camera = Vector(hit_result.camera_position, hit_result.hit_point).normalized()
        
        
        for l in hit_result.light_point :
            # vecteurs 
            hit_to_light : Vector = Vector(hit_result.hit_point, l).normalized()
            reflected : Vector = 2*np.dot(hit_to_light,hit_result.normal)*hit_result.normal - hit_to_light
            diffuse : np.ndarray = np.dot(hit_to_light, hit_result.normal)
            
            # couleurs / calcul
            ratio_d: np.ndarray = kd*diffuse
            ratio_s: np.ndarray = ks*(np.dot(reflected.normalized(),hit_to_camera)**(hit_result.shininess * 100))
            
            illumination += ratio_d
            
            # la formule précise qu'on ne doit ajouter de spéculaire, uniquement lorsque
            # la quantité diffuse est positive
            if diffuse > 0 :  
                illumination += ratio_s
            
        return Color.fromUnitNpArray(illumination)
        