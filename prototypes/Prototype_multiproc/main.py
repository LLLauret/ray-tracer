from multithreader import *
import os

def getColorForRange (y, total) -> tuple[int,int,int]:
    rg = y//(total//4)
    if  rg < 1 :
        return tuple((255,0,0))
    elif rg < 2 :
        return tuple((0,255,0))
    elif rg < 3 :
        return tuple((0,0,255))
    else:
        return tuple((128,128,128))

def createColoredArray(width, height) -> any :
    pixels : np.ndarray = np.ndarray(shape=(height,width),dtype=tuple)
    for y in range(height) :
        for x in range(width) :
            color = getColorForRange(y,height)
            pixels[y][x] = color
    return pixels    
        
def main() :
    WIDTH, HEIGHT = 800,600
    tableau = createColoredArray(WIDTH,HEIGHT)
    proc_man = ProcessManager(pixels=tableau, nbWorkers=4)
    os.system('cls')

    print("bonjour, ceci est un prototype pour le multiprocessing \n")
    print("le programme construit un tableau, et le multiprocessing le découpe pour en faire plusieurs images")
    
    print("lancement des processus... \n ")
    proc_man.runMultiproc()
    
    print("les pocessus enfants ont terminé leur tâches")

# contrôle nécessaire pour Windows
if __name__ == '__main__' :
    main()