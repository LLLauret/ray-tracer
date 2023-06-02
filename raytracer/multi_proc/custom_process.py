import multiprocessing as mp
import numpy as np
from picture import Picture
from interfaces.IOut import IOut
from interfaces.IScene import IScene

# class dérivée de multiprocessing.Process, qui permet de se départir de la sérialisation
# la fonction du processing se retrouve à être la méthode run(),
# et les arguments de la méthodes se retrouvent à être attributs du process

class CustomProcess(mp.Process) :
    def __init__(self, ray_tab: np.ndarray, out: IOut, pic: Picture, scene: IScene) -> None:
        super().__init__()
        self.__rays = ray_tab
        self.__out = out
        self.__pic = pic
        self.__scene = scene

    # run() execute scene.processRay pour tout les rays du processus    
    def run(self) :
        j = 0
        for y in self.__rays :
            i=0
            for x in y :
                result = self.__scene.processRay(ray=x,row=j,col=i)
                self.__pic.setPixel(color=result[0],y=j,x=i)
                i = i+1
            j = j+1
        
        # affichage/débuggage
        proc = mp.current_process()
        # on crée un fichier bmp (chunk)
        self.__pic.export(self.__out)
        print (f"{proc.name} a terminé")