from PIL import Image as Img
#from pathlib import Path

from interfaces.IOut import IOut

# représente un fichier BMP
class Bmp (IOut) :
    def __init__(self, path: str, resolution: tuple[int,int]) :
        self.__width = resolution[0]
        self.__height = resolution[1]
        self.__name = path

    def write(self, datas: list) :
        image = Img.new('RGB',(self.__width,self.__height),"black")
        image.putdata(datas)
        file_name = self.__name
        # if (Path.exists(file_name)) :
        #     pass
        image.save(fp=file_name, bitmap_format='bmp') 
        
        