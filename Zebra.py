import random as rand
from Animal import Animal
from Herbivore import Herbivore

class Zebra(Animal, Herbivore):
    NAME = "Zebra"
    SLEEP_INCREASE = 1.3
    MAX_STRENGTH_GAIN = 40

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
    
    def eat_plant(self):
        random_strength = rand.uniform(0, self.MAX_STRENGTH_GAIN)
        self.strength = self.strength + random_strength

    def to_string(self):
        return super().toString() + "; species: Zebra"