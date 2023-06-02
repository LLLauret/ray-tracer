from abc import ABC, abstractmethod

class IParallelizer(ABC) :
    
    @abstractmethod
    def runProcess (self) :
        pass
