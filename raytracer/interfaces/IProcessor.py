from abc import ABC, abstractmethod
from hit_result import HitResult

from color import Color


class IProcessor (ABC) :
    
    @abstractmethod
    def setNext(self) -> None :
        pass

    @abstractmethod
    def handle(self, hit_result:HitResult) -> Color :
        pass