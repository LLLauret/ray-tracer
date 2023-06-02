from Geometry3D import Point, Vector
from color import Color
from interfaces import IForm
from typing import List
## Classe de donnée, remplie de propriétés, qui montre ses parties publiques à tout le monde !
# TODO : ajouter la propriété shininess de la géométrie concernée
class HitResult :
    def __init__(self, hit: bool, camera_pos: Point = None, hit_point: Point = None, ray_origin: Point = None, distance: float = float('inf'), normal: Vector = None, color: Color = None, geometry_ref:IForm = None, shininess: float = 0, transparency: bool = False, reflection: float = 0, refraction = 0) : # type: ignore
        # touché : hit or miss : boolean
        self.hit : bool = hit
        self.ray_origin = ray_origin
        self.hit_point : Point = hit_point
        # distance à partir de l'origine du rayon du point d'intersection (pour sélectionner le plus proche)
        self.distance : float = distance
        self.normal : Vector = normal
        self.color : Color = color
        self.shininess : float = shininess
        self.reflection : float = reflection
        self.transparency : bool = transparency
        self.refraction : float = refraction
        # référence vers la géométrie pour simplifier la tâche du ShadowingProcessor
        self.geometry : IForm.IForm = geometry_ref #type: ignore
        self.shadowed : bool = False
        self.camera_position : Point = camera_pos
        self.rebounds : int = 0
        self.light_point : List[Point] = []
        self.illumination_processed : bool = False
    