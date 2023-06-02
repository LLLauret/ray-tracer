from PIL import Image
from typing import List
import numpy as np
import multiprocessing as mp
from time import sleep
import random

class ProcessManager :
    def __init__(self, pixels: np.ndarray, nbWorkers: int) -> None:
        self.__pixels = pixels
        self.__nbWorkers = nbWorkers
        self.__tabList = self.__decompose() # on découpe le tableau par la hauteur

    # décompose un tableau de m*n en plusieurs tableau de m * n/nb
    def __decompose (self) -> List[np.ndarray] :
        return np.split(self.__pixels, self.__nbWorkers)

    def runMultiproc(self) :
        process = [ ]
        for x in self.__tabList :
            p = mp.Process(target=self.createFile, args=(x,))
            process.append(p)

        [x.start() for x in process]
        # permet d'attendre la fin des processus enfants avant de retourner au parent
        [x.join() for x in process]
        
    def createFile(self, arr: np.ndarray) :
        print(f"{mp.current_process().name} has started")
        sleep(random.randrange(2,4))
        img = Image.new(mode="RGB", size=(arr.shape[1],arr.shape[0]))
        lst = list()
        for y in arr:
            for x in y :
                lst.append(x)
        img.putdata(lst)
        
        img.save(f"{mp.current_process().name}.bmp")
        
        print(f"{mp.current_process().name} s'est terminé")