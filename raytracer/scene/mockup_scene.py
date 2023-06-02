from typing import List
from interfaces.IScene import *
from interfaces.IForm import *
from geometries.form_cube import FormCube
from geometries.form_sphere import FormSphere
from geometries.surface import Surface
from hit_result import HitResult
from interfaces.IProcessor import *
from processors.miss_processor import MissProcessor
from processors.direct_light_processor import DirectLightProcessor
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer


class MockupScene (IScene) :
    def __init__(self) : 
        self.__geometries : List[IForm] = list()
        self.__lights : List[Point] = list()

        # self.__geometries.append(FormCube(4, Point(8,18,0),color_name='aqua',x_angle=0, y_angle=45, z_angle=45))
        # self.__geometries.append(FormSphere(center=Point(-4,30,0),color_name='red',radius=7))
        # self.__geometries.append(Surface(base_p=Point(-250,-15,-100),length=800,width=500,color_name='grey', shininess=0.5))
        self.__geometries.append(FormSphere(center=Point(10,60,0),color_name='orange', radius=20))
        self.__lights.append(Point(0,15,30))
        self.__background_color = Color(value=(0,0,0))

        self.__miss_handler : IProcessor = MissProcessor(bg_color=self.__background_color)
        self.__dle_handler : IProcessor =  DirectLightProcessor(self.__lights[0], geometries=self.__geometries)
        self.__miss_handler.setNext(self.__dle_handler)

    
    # méthode de rendu dans matPlotLib    
    def addToTestPlot(self,r: MatplotlibRenderer) :
        for g in self.__geometries :
            g.addToPlotTest(r)        
            # les sources lumineuse sont considérés comme des points.    
        for p in self.__lights :
            r.add((p, 'red', 10))
            

    # lance le processus de calcul du ray tracing -> Color, x, y
    def processRay(self, ray: Ray, row: int, col: int) -> tuple[Color, int, int]:
        nearest_hit : HitResult = self.__getNearestHit(ray)
        color = self.__miss_handler.handle(nearest_hit)
        return color, row, col

    def __getNearestHit (self, ray: Ray) -> HitResult :
        # valeur initiale, miss avec une distance infinie
        nearest_hit : HitResult = HitResult(hit=False)
        for g in self.__geometries :
            hit = g.hit(ray=ray)
            # le hit le plus proche est déterminé ici
            if hit.hit is True and hit.distance < nearest_hit.distance :
                nearest_hit = hit
        return nearest_hit