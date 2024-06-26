import random as rand
from Animal import Animal
from Carnivore import Carnivore

class Toad(Animal, Carnivore):
    NAME = "Toad"
    SLEEP_INCREASE = 1.2
    STRENGTH_GAIN = 0.3
    MAX_BUGS = 10
    POISON_CHANCE = 0.3

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
        num_bugs = rand.randint(0, 10)
        new_strength = (num_bugs * animal.strength * self.STRENGTH_GAIN +
            self.strength)
        self.strength = new_strength
    
    def poison_animal(self):
        random_number = rand.uniform(0, 1)
        if random_number <= self.POISON_CHANCE:
            return True
        return False

    def to_string(self):
        return super().toString() + "; species: Toad"
