from color import Color
from interfaces.IOut import IOut
import numpy as np

# Représente un conteneur de couleurs
class Picture : 
    def __init__(self, width : int, height: int) -> None:
        # self.__pixels = [[0 for i in range(width)] for j in range(height)]
        self.__pixels = np.ndarray(shape=(height, width), dtype=Color)
        self.__width = width
        self.__height = height
    
    # Sérialise les tuple RGB pour les envoyer vers la sortie IOut 
    def export (self, output:IOut) :
        pixels : tuple[int,int,int] = []
        for y in range(self.__height) :
            for x in range(self.__width) :
                value = self.__pixels[y][x].getRGB()
                pixels.append(value)
        output.write(datas=pixels)
    
    
    def setPixel(self, color:Color, y: int, x:int) :
        self.__pixels[y][x] = color
    
    def setPixels(self, array: np.ndarray) :
        for y in range(self.__height) :
            for x in range(self.__width) :
                self.__pixels[y][x] = Color.fromNpArray(array[y][x])

    def add(self, other: 'Picture') -> 'Picture' :
        new_array = np.append(self.__pixels, other.__pixels, axis=0)
        new_pic = Picture(width=new_array.shape[1],height=new_array.shape[0])
        new_pic.__pixels = new_array
        return new_pic