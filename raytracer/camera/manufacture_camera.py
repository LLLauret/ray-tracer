from Geometry3D import Point
from camera.camera import Camera

class ManufactureCamera :
    def __init__(self, json_camera: object) -> None:
        self.__camera : object = json_camera

    def createCamera(self) :
        pos_json = self.__camera['position']
        dir_json = self.__camera['direction']
        foc : float = self.__camera['focal']
        fov : float = self.__camera['fov']
        pos : Point = Point(pos_json['x'], pos_json['y'], pos_json['z'])
        a : float = dir_json['horizontal']
        e : float = dir_json['vertical']
        return Camera(position=pos, distance=foc, azimuth=a, elevation=e, fov=fov)