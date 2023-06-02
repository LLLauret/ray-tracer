from abc import *
from color import Color
#from picture import Picture
from ray.ray import Ray 

class IScene (ABC) :

    @abstractmethod
    def processRay(self,ray: Ray, row: int, col: int) -> tuple[Color, int, int]:
        pass
        