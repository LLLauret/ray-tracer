from PIL import Image as Img
from interfaces.IOut import IOut

# Représentation de l'aperçu de l'image produite à l'écran
class Screen (IOut):
    def __init__(self, resolution:tuple[int,int]) :
        self.__width = resolution[0]
        self.__height = resolution[1]
        

    def write(self,datas: list) :
        image = Img.new('RGB',(self.__width,self.__height),"black")
        image.putdata(datas)
        image.show()
    
    def __str__(self) -> str:
        return f"{self.__width} x {self.__height}"