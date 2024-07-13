import random as rand
from Animal import Animal
from Carnivore import Carnivore
from Herbivore import Herbivore
from Wolf import Wolf
from Leopard import Leopard
from Toad import Toad
from Cobra import Cobra
from Panda import Panda
from Zebra import Zebra

NUM_ANIMALS = 6
SPACING = 17
LEFT = "Left"
RIGHT = "Right"
AVG_STRENGTH_DIV = 2
ANIMAL2_WIN = 2
MAX_AGE = 100
MAX_HP = 500
MAX_STRENGTH = 250
MIN_AGE_REP = 5
BABY_HP = 100
    
def reproduce(animal1, animal2):
    if (animal1.age > MIN_AGE_REP and animal2.age > MIN_AGE_REP and
        animal1.same_species(animal2)):
        age = 0
        health = BABY_HP
        strength = (((animal1.strength + animal2.strength) / AVG_STRENGTH_DIV) / 
                    AVG_STRENGTH_DIV)
        
        if (isinstance(animal1, Wolf)):
            return Wolf(age, health, strength)
        
        if (isinstance(animal1, Leopard)):
            return Leopard(age, health, strength)
        
        if (isinstance(animal1, Toad)):
            return Toad(age, health, strength)
        
        if (isinstance(animal1, Cobra)):
            return Cobra(age, health, strength)
        
        if (isinstance(animal1, Panda)):
            return Panda(age, health, strength)
        
        if (isinstance(animal1, Zebra)):
            return Zebra(age, health, strength)
        
    return None

def print_both_animals(animal1, animal2):
    age_spacing = calc_spacing(str(animal1.age))
    health_spacing = calc_spacing(f"{animal1.health:.2f}")
    str_spacing = calc_spacing(f"{animal1.strength:.2f}")
    animal_spacing = calc_spacing(animal1.NAME)
    
    str_result = (
        f"({animal1.NAME}) {' ' * animal_spacing} ({animal2.NAME})\n"
        "---------- ----------\n"
        f"A: {animal1.age} {' ' * age_spacing} A: {animal2.age}\n"
        f"H: {animal1.health:.2f} {' ' * health_spacing} H: {animal2.health:.2f}\n"
        f"S: {animal1.strength:.2f} {' ' * str_spacing} S: {animal2.strength:.2f}\n"
    )
    print(str_result)

def calc_spacing(string):
    total_width = SPACING
    str1_width = len(string)
    spacing = total_width - str1_width
    if (spacing < 0):
        return 0
    return spacing

def print_round(round):
    print()
    print(f"Round {round}:")

def print_attack(side, damage):
    print(f"{side} does {damage:.2f} damage!")
    
def print_final_stats(animal1, animal2, poisoned):
    print()
    print_both_animals(animal1, animal2)
    if (poisoned):
        print("An animal was poisoned.")
        
def print_tie_game():
    print("-------GAME OVER-------")
    print("TIE: Both animals died!")

def print_winner(side):
    print("-------GAME OVER-------")
    print(side + " animal wins!")

def random_animal():
    rand_age = random_age(MAX_AGE)
    rand_strength = random_strength(MAX_STRENGTH)
    rand_class = rand.randint(0, NUM_ANIMALS - 1)
    
    if rand_class == 0:
        return Wolf(rand_age, MAX_HP, rand_strength)
    elif rand_class == 1:
        return Leopard(rand_age, MAX_HP, rand_strength)
    elif rand_class == 2:
        return Panda(rand_age, MAX_HP, rand_strength)
    elif rand_class == 3:
        return Zebra(rand_age, MAX_HP, rand_strength)
    elif rand_class == 4:
        return Toad(rand_age, MAX_HP, rand_strength)
    elif rand_class == 5:
        return Cobra(rand_age, MAX_HP, rand_strength)
    else:
        return None
    
def random_age(max):
    rand_age = rand.randint(0, max)
    return rand_age

def random_strength(max):
    rand_strength = rand.uniform(0, max)
    return rand_strength


