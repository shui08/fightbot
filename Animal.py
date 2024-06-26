import random as rand
from abc import ABC, abstractmethod

class Animal(ABC):
    NAME = "Animal"

    def __init__(self, age = 0, health = 0.0, strength = 0.0):
        self._age = age
        self._health = health
        self._strength = strength
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
    
    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = value

    def attack(self, animal):
        damage = rand.uniform(1, self._strength)
        animal.health = animal.health - damage
        return damage
    
    @abstractmethod
    def same_species(self):
        pass

    @abstractmethod
    def sleep(self):
        pass

    @abstractmethod
    def is_poisonous(self):
        pass

    def poison_animal(self):
        return False
    
    def toString(self):
        return ("Animal age: " + self._age + "; health: " + self._health + 
                "; strength: " + self._strength)