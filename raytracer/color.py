from PIL import ImageColor as Ic
import numpy as np

class Color :
    def __init__(self, value:tuple[int,int,int]) -> None:
        self.__r = value[0]
        self.__g = value[1]
        self.__b = value[2] 
    
    @staticmethod
    def fromName (name: str) -> 'Color' :
        return Color(Ic.getrgb(color=name))

    # retourne les valeurs RGB sous forme de tuple
    def getRGB(self) -> tuple[int,int,int] :
        return self.__r, self.__g, self.__b
    
    # renvoie une fraction de la couleur
    def ratio (self, ratio: float) -> 'Color':
        _r = np.clip((int)(self.__r * ratio),0,255)
        _g = np.clip((int)(self.__g * ratio),0,255)
        _b = np.clip((int)(self.__b * ratio),0,255)
        return Color((_r,_g,_b))
    
    
    def add (self, other:'Color') -> 'Color':
        other_r,other_g, other_b = other.getRGB()
        r = np.clip(self.__r + other_r , 0, 255)
        g = np.clip(self.__g + other_g , 0, 255)
        b = np.clip(self.__b + other_b , 0, 255)
        return Color((r,g,b))

    # retourne une couleur sous forme d'un array dont les valeurs sont comprises entre 0 et 1
    def toUnitNpArray(self, ratio: float = 1) -> np.ndarray :
        return np.array([self.__r, self.__g, self.__b])/255*ratio
    
    # retourne une couleur à partir de valeurs RGB entre 0 et 1
    @staticmethod
    def fromUnitNpArray(array:np.ndarray) -> 'Color' :
        array = array*255
        array = np.clip(array, 0, 255).astype(int)
        return Color(tuple(array))
    
    @staticmethod
    def fromNpArray(array:np.ndarray) -> 'Color' :
        array = np.clip(array, 0, 255).astype(int)
        return Color(tuple(array))
    
    # def sub (self, other:'Color') -> 'Color':
    #     # trouver la couleur complémentaire :
    #     # complement : Color = self.add(other)
    #     other_r, other_g, other_b = other.getRGB()
    #     compl_r = 255 - other_r
    #     compl_g = 255 - other_g
    #     compl_b = 255 - other_b
    #     # compl_r, compl_g, compl_b = complement.getRGB()
    #     r = np.clip(self.__r - compl_r , 0, 255)
    #     g = np.clip(self.__g - compl_g , 0, 255)
    #     b = np.clip(self.__b - compl_b , 0, 255)
    #     return Color((r,g,b))
    