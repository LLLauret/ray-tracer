from abc import *

class IOut (ABC) :

    @abstractmethod
    def write(self,datas: list) :
        pass