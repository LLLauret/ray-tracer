from typing import List
from interfaces.IBuilder import IBuilder
from interfaces.IProcessor import IProcessor
from interfaces.IScene import IScene
from interfaces.IForm import IForm
from geometries.manufacture_form import ManufactureForm
from processors.manufacture_process_chain import ManufactureProcessChain
from color import Color
from Geometry3D import Point
from scene.scene import Scene

# Configurateur pour la scène
class BuilderScene (IBuilder) :
    def __init__(self, jsonScene: object, form_manufacture: ManufactureForm, process_manufacture: ManufactureProcessChain) -> None :
        self.__scene = jsonScene
        self.__manuf_form: ManufactureForm = form_manufacture
        self.__geometries : List[IForm] = []
        self.__lights : List[Point] = []
        self.__manufacture_process : ManufactureProcessChain = process_manufacture
        self.__bg_color : Color = Color.fromName(self.__scene['background'])
        self.__processChain : IProcessor = None #type: ignore
    
    # fait appel à la manufacture de géométrie
    def addForms(self):
        for form_obj in self.__scene['geometries'] :
            self.__geometries.append(self.__manuf_form.createForm(form_obj))

    # crée une liste de sources lumineuses    
    def addLights(self):
        for light_obj in self.__scene['sources'] :
            light : Point = Point(light_obj['x'], light_obj['y'], light_obj['z'])
            self.__lights.append(light)
    
    # fait appel à la manufacture de processeur pour créer la chaine de traitement des rayons
    def addProcessors(self):
        self.__processChain = self.__manufacture_process.createChain(form_list=self.__geometries, light_list=self.__lights, bg_color=self.__bg_color, features=self.__scene['rendering'], max_rebounds=self.__scene['max_rebounds'])

    def reset(self):
        self.__geometries.clear()
        self.__lights.clear()
        self.__processChain = None

    # retoune une IScene configurée
    def getResult(self) -> IScene :
        return Scene(geometries=self.__geometries,lights=self.__lights, processing_chain=self.__processChain)