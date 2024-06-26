from Animal import Animal
from Carnivore import Carnivore

class Leopard(Animal, Carnivore):
    NAME = "Leopard"
    SLEEP_INCREASE = 1.5
    STRENGTH_GAIN = 0.55

    def __init__(self, age = 0, health = 0.0, strength = 0.0):
        super().__init__(age, health, strength)

    def same_species(self, animal):
        if self.NAME == animal.NAME:
            return True
        return False

    def sleep(self):
        self.strength = self.strength * self.SLEEP_INCREASE

    def is_poisonous(self):
        return False
    
    def eat_animal(self, animal):
        new_strength = (animal.strength * self.STRENGTH_GAIN) + self.strength
        self.strength = new_strength

    def to_string(self):
        return super().toString() + "; species: Leopard"