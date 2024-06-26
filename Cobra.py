import random as rand
from Animal import Animal
from Carnivore import Carnivore

class Cobra(Animal, Carnivore):
    NAME = "Cobra"
    SLEEP_INCREASE = 1.7
    STRENGTH_GAIN = 0.9
    POISON_CHANCE = 0.8

    def __init__(self, age = 0, health = 0.0, strength = 0.0):
        super().__init__(age, health, strength)

    def same_species(self, animal):
        if self.NAME == animal.NAME:
            return True
        return False

    def sleep(self):
        self.strength = self.strength * self.SLEEP_INCREASE

    def is_poisonous(self):
        return True
    
    def eat_animal(self, animal):
        new_strength = animal.strength * self.STRENGTH_GAIN + self.strength
        self.strength = new_strength
    
    def poison_animal(self):
        random_number = rand.uniform(0, 1)
        if random_number <= self.POISON_CHANCE:
            return True
        return False

    def to_string(self):
        return super().toString() + "; species: Cobra"