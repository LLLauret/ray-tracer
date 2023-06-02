from abc import ABC, abstractmethod
from interfaces.IParallelizer import IParallelizer
from interfaces.ICleaner import ICleaner
from interfaces.IReassembler import IReassembler

# manufacture abstraite de multiprocessing, crée une famille d'objet
class IMultiProcManufacture(ABC) :
   
   @abstractmethod
   def createParallelizer(self) -> IParallelizer :
      pass
   
   @abstractmethod
   def createReassembler(self) -> IReassembler :
      pass
   
   @abstractmethod
   def createCleaner(self) -> ICleaner :
      pass
   