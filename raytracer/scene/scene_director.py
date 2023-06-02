from interfaces.IBuilder import IBuilder
from interfaces.IScene import IScene

# Directeur qui sert d'interface pour le montage de la scène
class SceneDirector :
    def __init__(self, builder: IBuilder) -> None:
        self.__builder : IBuilder = builder

    def make(self) -> IScene:
        self.__builder.addForms()
        self.__builder.addLights()
        self.__builder.addProcessors()
        return self.__builder.getResult()

    def changeBuilder(self, builder: IBuilder) :
        self.__builder = builder
        pass
    
