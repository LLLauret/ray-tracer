import numpy as np
from ray.ray_manufacture import *
from viewport.iteratorViewport import iteratorViewport
from copy import deepcopy
from interfaces.IMultiProc_manufacture import IMultiProcManufacture
from multi_proc.height_multiproc_manufacture import ManufactureHeightMultiProc
from interfaces.IScene import IScene

# retourne la résolution sous forme de tuple [largeur, hauteur]
def resolution(json_resolution:object) -> tuple[int, int] :
    width = json_resolution['width']
    height = json_resolution['height']
    return width,height

def createRays(vp_it: iteratorViewport, ray_manuf: RayManufacture, origin: Point, width: int, height: int) -> np.ndarray :
    ray_tab : np.ndarray = np.ndarray(shape=(height, width),dtype=Ray)
    count = 0
    while (vp_it.hasMore()) :
        point, y, x = vp_it.next()
        ray = ray_manuf.createRay(origin=origin, through=point)
        np.put(a=ray_tab,ind=count,v=deepcopy(ray))
        count += 1

    return ray_tab

def multiProcessFactory(scene: IScene, rays: np.ndarray, type: str = "height", nb_process: int = 4 ) -> IMultiProcManufacture :
    defaut : IMultiProcManufacture = ManufactureHeightMultiProc(scene=scene, rays=rays, nb_process=nb_process)
    if (type == "height") :
        return defaut

