from interfaces.IForm import IForm
from interfaces.IProcessor import IProcessor
from Geometry3D import Point
from interfaces.IScene import IScene
from color import Color
from ray.ray import Ray
from hit_result import HitResult
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from typing import List

class Scene(IScene) : 
    def __init__(self, geometries: List[IForm], lights: List[Point], processing_chain:IProcessor) -> None:
        self.__geometries : List[IForm] = geometries
        self.__lights : List[Point] = lights
        self.__processors : IProcessor = processing_chain
        
    # détermine la couleur rendu pour un rayon donné    
    def processRay(self, ray: Ray, row: int, col: int) -> tuple[Color, int, int]:
        nearest_hit : HitResult = self.__getNearestHit(ray)
        nearest_hit.camera_position = ray.origin()
        color = self.__processors.handle(nearest_hit)
        return color, row, col

    # détermine le point d'intersection le plus proche dans la scène
    def __getNearestHit (self, ray: Ray) -> HitResult :
        # valeur initiale, miss avec une distance infinie
        nearest_hit : HitResult = HitResult(hit=False)
        for g in self.__geometries :
            hit = g.hit(ray=ray)
            # le hit le plus proche est déterminé ici
            if hit.hit is True and hit.distance < nearest_hit.distance :
                nearest_hit = hit
        return nearest_hit
    
    # méthode de rendu dans matPlotLib    
    def addToTestPlot(self, r: MatplotlibRenderer) :
        for g in self.__geometries :
            g.addToPlotTest(r)        
            # les sources lumineuse sont considérés comme des points.    
        for p in self.__lights :
            r.add((p, 'purple', 20))
            pass