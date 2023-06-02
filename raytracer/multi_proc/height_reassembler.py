from typing import List
from PIL import Image as Img
import numpy as np
from picture import Picture
from interfaces.IReassembler import IReassembler

class HeightReassembler (IReassembler) :
    def __init__(self, filenames: List[str]) -> None:
        self.__names : List[str] = filenames
        self.__chunks : List[np.ndarray] = [ ]

    def make(self) -> Picture:
        for fn in self.__names :
            img = Img.open(fp=fn) #chargement du fichier en mémoire
            # conversion de l'image sous forme de tableau de pixels
            img_data: np.ndarray = np.asarray(img)
            # on conserve les données dans une liste
            self.__chunks.append(img_data)
            img.close()
        
        # on recrée le tableau de pixels entier
        result : np.ndarray = self.__chunks.pop(0)
        for c in self.__chunks :
            result = np.append(result,c,axis=0)
        
        # on crée un Picture à partir du tableau [r,g,b]
        pic : Picture = Picture(width=result.shape[1], height=result.shape[0])
        pic.setPixels(array=result) # set tout les pixels de la Picture
        return pic    

