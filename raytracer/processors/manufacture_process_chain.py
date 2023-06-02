from typing import List
from interfaces.IProcessor import IProcessor
from interfaces.IForm import IForm
from Geometry3D import Point
from color import Color
from ray.ray_manufacture import RayManufacture
from processors.miss_processor import MissProcessor
from processors.reflection_processor import ReflectionProcessor
from processors.illumination_processor import IlluminationProcessor
from processors.shadowing_processor import ShadowingProcessor
from processors.advanced_refraction_processor import AdvancedRefractionProcessor
from processors.simple_refraction_processor import SimpleRefractionProcessor
from processors.occlusion_processor import OcclusionProcessor
from processors.adaptive_occlusion_processor import AdaptiveOcclusionProcessor


# cette classe instancie la chaine de traitement des HitResult
class ManufactureProcessChain :
    def __init__(self, ray_manuf:RayManufacture) -> None:
        self.__ray_manuf = ray_manuf
    
    def createChain(self, form_list:List[IForm], light_list:List[Point], bg_color:Color, features:str='phong', max_rebounds: int = 1) -> IProcessor :
        # mode 'phong' par défaut
        process_chain = MissProcessor(bg_color=bg_color)
        shadowing_processor = ShadowingProcessor(light_position=light_list, geometries=form_list, manuf_ray=self.__ray_manuf)
        illumination_processor = IlluminationProcessor(manuf_ray=self.__ray_manuf)
        
        process_chain.setNext(shadowing_processor)
        shadowing_processor.setNext(illumination_processor)    
        # référence vers le dernier élément de la chaine de base, permet d'enchainer plus facilement les autres.
        last : IProcessor = illumination_processor

        if 'occlusion' in features :
            last = self.__addOcclusion(
                current=last, 
                form_list=form_list, 
                ray_manuf=self.__ray_manuf)
        
        if 'transparency' in features :
            last = self.__addRefraction(
                current=last, 
                form_list=form_list, 
                light_list=light_list, 
                bg_color=bg_color,ray_manuf=self.__ray_manuf)
        
        if 'reflection' in features :
            last = self.__addReflection(
                current=last, 
                form_list=form_list, 
                light_list=light_list, 
                max_rebounds=max_rebounds, 
                ray_manuf=self.__ray_manuf)
        
        return process_chain
     
    
    def __addOcclusion (self, current: IProcessor, form_list: List[IForm], ray_manuf: RayManufacture) -> IProcessor :
        occlusion_processor = AdaptiveOcclusionProcessor(geometries=form_list, ray_manuf=ray_manuf, min_distance=0.5)
        current.setNext(occlusion_processor)
        return occlusion_processor

    def __addReflection(self, current: IProcessor,form_list: List[IForm], ray_manuf: RayManufacture, light_list: List[Point], max_rebounds: int ) -> IProcessor :
        reflect_processor = ReflectionProcessor(geometries=form_list, manuf_ray=ray_manuf, depth=max_rebounds)
        shadowing_processor = ShadowingProcessor(light_position=light_list, geometries=form_list,manuf_ray=ray_manuf)
        illumination_processor = IlluminationProcessor(manuf_ray=ray_manuf)
        reflect_processor.setNext(shadowing_processor)
        shadowing_processor.setNext(illumination_processor)
        current.setNext(reflect_processor)
        return illumination_processor

    def __addRefraction(self, current: IProcessor, form_list: List[IForm], ray_manuf: RayManufacture, light_list: List[Point], bg_color: Color) -> IProcessor :
        refraction_processor = AdvancedRefractionProcessor(geometries=form_list, ray_manuf=self.__ray_manuf)
        miss_processor = MissProcessor(bg_color=bg_color)
        shadowing_processor = ShadowingProcessor(light_position=light_list,geometries=form_list, manuf_ray=self.__ray_manuf)
        illumination_processor = IlluminationProcessor(manuf_ray=ray_manuf)
        refraction_processor.setNext(miss_processor)
        miss_processor.setNext(shadowing_processor)
        shadowing_processor.setNext(illumination_processor)
        current.setNext(refraction_processor)
        return illumination_processor
    

    # chain : Miss -> Shadowing -> Illumination -> Occlusion -> Transparency -> Miss -> Shadowing -> Illumination -> Reflection -> shadowing -> illumination
      