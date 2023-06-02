from abc import ABC, abstractmethod
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from Geometry3D.geometry import Point
from hit_result import HitResult
from ray.ray import Ray

class IForm (ABC) :
    
    @abstractmethod
    def addToPlotTest (self, r:MatplotlibRenderer) :
        pass
    
    @abstractmethod
    def hit (self, ray:Ray) -> HitResult :
        pass