from abc import ABC, abstractmethod

class ICleaner (ABC) :

    @abstractmethod
    def clean (self) :
        pass