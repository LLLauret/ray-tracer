import json as js
from utils import resolution,createRays, multiProcessFactory
from viewport.iteratorViewport import iteratorViewport
from viewport.viewport import Viewport
from output.screen import Screen
from output.bmp import Bmp
from picture import *
from datetime import datetime
from interfaces.IScene import IScene
from interfaces.IBuilder import IBuilder
from interfaces.IMultiProc_manufacture import IMultiProcManufacture
from geometries.manufacture_form import ManufactureForm
from processors.manufacture_process_chain import ManufactureProcessChain
from scene.builder_scene import BuilderScene
from scene.scene_director import SceneDirector
from camera.manufacture_camera import ManufactureCamera, Camera
from ray.ray_manufacture import RayManufacture,Ray


# le nom du fichier de description de scène sera passé en argument plus tard

def main () :
    
    arg_1 = "./scenes_json/refraction_sphere_1.005.json"
    json_file = open(file=arg_1)
    json_data = js.loads(json_file.read())
    
    # Constantes
    WIDTH, HEIGHT = resolution(json_data['resolution'])
    MULTIPROC = True
    
    # manufactures et monteurs
    manuf_cam : ManufactureCamera = ManufactureCamera(json_data['camera'])
    ray_manufacture = RayManufacture()
    manuf_form : ManufactureForm = ManufactureForm()
    manuf_process : ManufactureProcessChain = ManufactureProcessChain(ray_manuf=ray_manufacture)
    scene_builder : IBuilder = BuilderScene(json_data['scene'], form_manufacture=manuf_form, process_manufacture=manuf_process)
    scene_director : SceneDirector = SceneDirector(builder=scene_builder)


    camera : Camera = manuf_cam.createCamera()
    # champs de vision (plan sur lequel se situe les pixels de l'écran)
    vp : Viewport = camera.createViewPort(width=WIDTH, height=HEIGHT)
    # itérateur pour les points du viewport
    it : iteratorViewport  = vp.iterator()
    # sortie à l'écran (aperçu de l'image)
    out = Screen(resolution=(WIDTH,HEIGHT))
    fichier = Bmp(path=f'apercu_{arg_1}_.bmp',resolution=((WIDTH,HEIGHT)))
    scene : IScene = scene_director.make()
    image = Picture(width=WIDTH, height=HEIGHT)
    print(out)

    #chronometrage :
    debut = datetime.now()

    # lancer de rayon
    cam_pos = camera.position()

    if not MULTIPROC :
        print("starting single-core")
        while it.hasMore() :
            point, y, x = it.next()
            ray : Ray = ray_manufacture.createRay(origin=cam_pos,through=point)
            color, row, col =  scene.processRay(ray,row=y,col=x)
            image.setPixel(color=color, y=row, x=col)

    # le multiprocessing tel qu'implémenté dans l'application me contraint à changer un peu le main()
    else :
        print("starting multi-core")
        # rays est un tableau contenant tout les rayons à traiter
        rays = createRays(vp_it=it,ray_manuf=ray_manufacture, origin=cam_pos, width=WIDTH, height=HEIGHT)
        
        # penser à adapter le nb_process selon la machine sur laquelle s'exécute le programme (utiliser mp.cpu_count() pour avoir le nombre maximal de coeurs)
        # méthode qui détermine quelle factory utiliser pour le multiprocessing
        multiprocess_manuf : IMultiProcManufacture = multiProcessFactory(scene=scene, rays=rays, nb_process=8, type="height")
        parallelizer = multiprocess_manuf.createParallelizer()
        cleaner = multiprocess_manuf.createCleaner()

        # lancement du traitement parallèle
        parallelizer.runProcess()
        print("résultats prêts") # les processus sont terminés
        
        reassembler = multiprocess_manuf.createReassembler()
        # on reconstitue la Picture originale
        image = reassembler.make()
        cleaner.clean()

    # affichage de la durée du traitement 
    print(datetime.now() - debut)

    # affichage de la sortie
    print ("exporting")
    image.export(out)
    image.export(fichier)

# directive nécessaire au multiprocessing pour éviter la récursion dans la création des processus enfants
if __name__ == '__main__' :
    main()