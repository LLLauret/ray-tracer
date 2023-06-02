import os
from typing import List
from interfaces.ICleaner import ICleaner


class Cleaner (ICleaner):
    def __init__(self, filenames: List[str]) -> None:
        self.__names = filenames
    
    def clean (self) :
        for f in self.__names :
            os.remove(f)