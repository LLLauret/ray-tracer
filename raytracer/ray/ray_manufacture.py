from ray.ray import *

class RayManufacture : 
    def __init__(self) -> None:
        pass
    
    # crée un rayon en fonction d'un point de départ et un autre point par lequel le rayon passe
    def createRay(self, origin : Point, through: Point) -> Ray :
        return Ray(origin=origin, point=through)