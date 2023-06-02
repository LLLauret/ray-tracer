import numpy as np
from multi_proc.custom_process import CustomProcess
from interfaces.IParallelizer import IParallelizer
from typing import List
from interfaces.IOut import IOut
from interfaces.IScene import IScene
from picture import Picture

# cette classe s'occupe de créer les processus distincts ainsi que de les lancer
class HeightParallelizer (IParallelizer):
    def __init__(self, rays: List[np.ndarray], outs: List[IOut], pics: List[Picture], scene: IScene, nb_proc: int = 4) -> None:
        self.__ray_tabs = rays
        self.__process_list : List[CustomProcess] = []
        self.__pics = pics
        self.__scene = scene
        self.__outputs = outs
        self.__nb_proc = nb_proc 

    def runProcess (self) :
        for n in range(self.__nb_proc) :
            p = CustomProcess(self.__ray_tabs[n], self.__outputs[n], self.__pics[n], scene=self.__scene)  
            self.__process_list.append(p)
        # les processus crées précedemment sont lancés
        for task in self.__process_list :
            task.start()
        # la méthode join nous permet d'attendre que les processus enfants soit terminés avant de retourner au Main
        for task in self.__process_list :
            task.join()
    