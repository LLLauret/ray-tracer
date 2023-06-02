from processors.base_processor import *

# vérifie l'intersection du lancer de rayon
class MissProcessor(BaseProcessor) : 
    
    def __init__(self, bg_color : Color) -> None:
        super().__init__()
        self.__bg_color : Color = bg_color
    
    def handle(self, hit_result: HitResult) -> Color:
        if hit_result.hit and self._next_handler is not None:
            return self._next_handler.handle(hit_result)
        return self.__bg_color

    def setNext(self, handler: IProcessor) -> IProcessor:
        return super().setNext(handler)