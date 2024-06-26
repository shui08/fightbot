from abc import ABC, abstractmethod

class Carnivore(ABC):
    
    @abstractmethod
    def eat_animal(self, animal):
        pass
