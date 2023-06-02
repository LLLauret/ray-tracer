from abc import ABC, abstractmethod
from interfaces.IScene import IScene
class IBuilder (ABC) :
    
    @abstractmethod
    def reset() :
        pass
    @abstractmethod
    def addForms() :
        pass
    @abstractmethod
    def addLights() :
        pass
    @abstractmethod
    def addProcessors() :
        pass

    @abstractmethod
    def getResult() -> IScene :
        pass
