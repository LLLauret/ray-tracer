import copy
from Geometry3D import Vector,Point,ConvexPolygon,distance
from Geometry3D.render.renderer_matplotlib import MatplotlibRenderer
from viewport.iteratorViewport import iteratorViewport

# représentation de l'écran/champs de vision dans l'espace
class Viewport :
    def __init__(self, width:int, height:int, pts: list[Point]) :
        self.__tp_left = pts[0]
        self.__tp_right = pts[1]
        self.__bt_left = pts[2]
        self.__bt_right = pts[3]
        self.__width = width
        self.__height = height
        self.__vec_col = Vector(self.__tp_left, self.__tp_right).normalized()
        self.__vec_row = Vector(self.__tp_left, self.__bt_left).normalized()
        self.__step_col = distance(self.__tp_left, self.__tp_right) / width
        self.__step_row = distance(self.__tp_left, self.__bt_left) / height

    def addToPlotTest(self, r : MatplotlibRenderer, color:str) :
        cvp = ConvexPolygon([self.__tp_left, self.__bt_left, self.__bt_right, self.__tp_right])
        r.add((cvp, color,1), normal_length=0)

    # test : aperçu des mesures du viewport
    def testLongueur(self) :
        print("A - B : {}".format(distance(self.__tp_left,self.__tp_right)))
        print("A - C : {}".format(distance(self.__tp_left,self.__bt_left)))
        print("B - D : {}".format(distance(self.__tp_right,self.__bt_right)))
        print("C - D : {}".format(distance(self.__bt_left,self.__bt_right)))


    def iterator(self) -> iteratorViewport :
        first_point_center = copy.deepcopy(self.__tp_left)
        first_point_center.move(self.__vec_col * (self.__step_col/2))
        first_point_center.move(self.__vec_row * (self.__step_row/2))
        delta_col = (self.__vec_col * self.__step_col)
        delta_row = (self.__vec_row * self.__step_row)
        return iteratorViewport(origin=first_point_center, delta_col = delta_col, delta_row = delta_row, width=self.__width, height=self.__height) 