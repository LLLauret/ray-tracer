from interfaces.IProcessor import *
from hit_result import HitResult
from typing import List

class BaseProcessor(IProcessor) :

    _next_handler : IProcessor = None # type: ignore
    
    def setNext(self, handler:IProcessor) -> IProcessor:
        self._next_handler : IProcessor = handler
        return handler

    @abstractmethod
    def handle(self, hit_result : HitResult) -> Color :
        pass