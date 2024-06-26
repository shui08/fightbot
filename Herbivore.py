from abc import ABC, abstractmethod

class Herbivore(ABC):
    
    @abstractmethod
    def eat_plant(self):
        pass