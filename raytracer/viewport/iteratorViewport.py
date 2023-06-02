import copy
from Geometry3D import *

# Itérateur qui permet de parcourir les points du viewport
class iteratorViewport() :
    def __init__(self, origin : Point, delta_col : Vector, delta_row : Vector, width: int, height: int) :
        self.__origin = origin
        self.__col = 0
        self.__row = 0
        self.__width = width
        self.__height = height
        self.__delta_col = delta_col
        self.__delta_row = delta_row
        self.__moving_point = copy.deepcopy(origin)
        self.__pixel_count = width * height
        self.__index = 0
    
    # semble fonctionner avec l'incrémentation dans next()
    def hasMore(self) -> bool :
        #return (self.col * self.row < self.pixel_count) is True
        return (self.__index < self.__pixel_count) is True
    # semble correct !
    def next(self) -> tuple[Point,int,int] :
        if self.__col == 0 and self.__row == 0 :
            self.__col += 1
            self.__row += 1

        elif self.__col < self.__width :
            self.__moving_point.move(self.__delta_col)
            self.__col += 1
        
        elif self.__row < self.__height :
            self.__row += 1
            self.__col = 1
            self.__lineReturn()    
        
        self.__index += 1
        return self.__moving_point, self.__row-1, self.__col-1
    
    # permet de repartir au début de la ligne suivante
    def __lineReturn(self) :
        self.__origin.move(self.__delta_row)
        self.__moving_point = copy.deepcopy(self.__origin)
