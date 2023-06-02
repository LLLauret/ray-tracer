from interfaces.IForm import IForm
from Geometry3D import Point
from geometries.form_cube import FormCube
from geometries.form_sphere import FormSphere
from geometries.surface import Surface
from geometries.checkerboard_ground import CheckerBoardGround

class ManufactureForm :
    def __init__(self) -> None :
        pass
    
    def createForm (self, json_form: object) -> IForm :
        geometry_type : str = json_form['type']
        geometry_form : object = json_form['form']
        form : IForm = self.__switch(geometry_type, geometry_form)
        return form

    def __switch(self, type: str, form: object) -> IForm :
        if type == 'cube' :
            return self.__createCube(form)
        elif type == 'sphere' :
            return self.__createSphere(form)
        elif type == 'surface' :
            return self.__createSurface(form)
        elif type == 'damier' :
            return self.__createDamier(form)
        return None

    def __createCube(self, json_form: object) -> FormCube :
        json_center : object = json_form['center']
        json_orientation: object = json_form['orientation']
        l : float = json_form['length']
        c: str = json_form['color']
        s: float =  json_form['shininess']
        r: float = json_form['reflection']
        t: bool = json_form['transparency']
        center: Point = Point(json_center['x'], json_center['y'], json_center['z'])
        x: int = json_orientation['x']
        y: int = json_orientation['y']
        z: int = json_orientation['z']
        refraction : float = json_form['refraction']

        return FormCube(center=center,length=l, color_name=c, shininess=s, reflection=r, x_angle=x, y_angle=y, z_angle=z, transparency=t, refraction=refraction)

    def __createSphere(self, json_form: object) -> FormSphere :
        json_center : object = json_form['center']
        json_orientation: object = json_form['orientation']
        rad : float = json_form['radius']
        c: str = json_form['color']
        s: float =  json_form['shininess']
        r: float = json_form['reflection']
        t: bool = json_form['transparency']
        center: Point = Point(json_center['x'], json_center['y'], json_center['z'])
        x: int = json_orientation['x']
        y: int = json_orientation['y']
        z: int = json_orientation['z']
        refraction : float = json_form['refraction']
        
        return FormSphere(center=center, radius=rad, color_name=c,shininess=s, reflection=r,transparency=t, refraction=refraction, x_angle=x, y_angle=y, z_angle=z)

    def __createSurface(self, json_form: object) -> Surface : 
        json_base_p = json_form['base']
        p: Point = Point(json_base_p['x'], json_base_p['y'], json_base_p['z'])
        l : float = json_form['length']
        w : float = json_form['width']
        c : str = json_form['color']
        s : float = json_form['shininess']
        r : float = json_form['reflection']
        o : str = json_form['orientation']

        return Surface(base_p=p, length=l, width=w, color_name=c, shininess=s, reflection=r, orientation=o)
    
    def __createDamier(self, json_form: object) -> CheckerBoardGround : 
        json_base_p = json_form['base']
        p: Point = Point(json_base_p['x'], json_base_p['y'], json_base_p['z'])
        l : float = json_form['length']
        w : float = json_form['width']
        c : str = json_form['color']
        s : float = json_form['shininess']
        r : float = json_form['reflection']

        return CheckerBoardGround(base_p=p, length=l, width=w, color_name=c, shininess=s, reflection=r)
    