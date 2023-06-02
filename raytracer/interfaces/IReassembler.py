from abc import ABC, abstractmethod
from picture import Picture

class IReassembler (ABC) :
    
    @abstractmethod
    def make (self) -> Picture :
        pass
