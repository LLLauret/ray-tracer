from typing import List
import numpy as np
from picture import Picture
from interfaces.IOut import IOut
from output.bmp import Bmp
from interfaces.IScene import IScene
from multi_proc.height_parallelizer import HeightParallelizer
from multi_proc.height_reassembler import HeightReassembler
from multi_proc.cleaner import Cleaner

# cette classe a pour but de configurer le multiprocessing en découpant les éléments
class ManufactureHeightMultiProc :
    def __init__(self,scene: IScene, rays: np.ndarray, nb_process: int = 4) -> None:
        self.__scene = scene
        self.__nb_process = nb_process
        self.__rays = rays
        self.__name_list : List[str] = [ ]

    def createParallelizer(self) -> HeightParallelizer :
        rays_list = self.__createRayTabs()
        pic_list = self.__createPicList()
        out_list = self.__createOutList()
        return HeightParallelizer(rays=rays_list, scene=self.__scene, pics=pic_list, outs=out_list,nb_proc=self.__nb_process)

    # divise un tableau complet en utilisant les rangées    
    def __createRayTabs (self) -> List[np.ndarray] :
        # ne fonctionne que si le tableau peut être divisé sans reste, de manière égale
        # à revoir car la méthode limite les résolutions possibles
        return np.split(self.__rays, self.__nb_process)
    
    def __createPicList (self) -> List[Picture] :
        l : List[Picture] = [ ]
        shape = self.__rays.shape # shape est un tuple
        width = shape[1]
        height = shape[0]//self.__nb_process
        for x in range(self.__nb_process) :
            p = Picture(width=width, height=height)
            l.append(p)
        return l
    
    def __createOutList(self) -> List[IOut] :
        l : List[IOut] = [ ]
        shape = self.__rays.shape
        width = shape[1]
        height = shape[0]//self.__nb_process
        for x in range(self.__nb_process) :
            path = f"part_{x+1}.bmp"
            out = Bmp(path=path, resolution=(width,height))
            self.__name_list.append(path)
            l.append(out)
        return l
    
    def createReassembler (self) -> HeightReassembler :
        return HeightReassembler(filenames=self.__name_list)
    
    def createCleaner (self) -> Cleaner :
        return Cleaner(filenames=self.__name_list)