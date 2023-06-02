from interfaces.IForm import IForm,abstractmethod, HitResult, Ray
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from color import Color

class BaseForm (IForm) :
    def __init__(self, color_name: str, shininess: float = 0, reflection: float = 0, transparency: bool = False, refraction = 0) -> None:
        self._shininess : float = shininess
        self._reflection : float = reflection
        self._transparency : bool = transparency
        self._color_name : str = color_name
        self._color : Color = Color.fromName(color_name)
        self._refraction : float = refraction

    @abstractmethod
    def hit(self, ray: Ray) -> HitResult:
        pass

