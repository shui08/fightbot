import os
from dotenv import load_dotenv, dotenv_values
from discord.ext import commands
import discord
import random as rand
import HelperFunctions as HF
from Animal import Animal
from Carnivore import Carnivore
from Herbivore import Herbivore
from Wolf import Wolf
from Leopard import Leopard
from Toad import Toad
from Cobra import Cobra
from Panda import Panda
from Zebra import Zebra

load_dotenv()
BOT_TOKEN = f"{os.getenv('FIGHTBOT_TOKEN')}"
CHANNEL_ID = int(os.getenv('CHANNEL'))
MIN_ASCII_CHAR = 33
MAX_ASCII_CHAR = 126
LEFT = "Left"
RIGHT = "Right"
START = "fightbot start!"
WOLF = "https://media.tenor.com/Tw8FiJa_KWsAAAAe/alpha-wolf.png"
LEOPARD = "https://images.vexels.com/media/users/3/128143/isolated/preview/702d2ee4054db44b5e4e9e5dc996dfe1-leopard-funny-cartoon.png?w=360"
TOAD = "https://www.alfoart.com/images/toad-tutorial/1-022.jpg"
COBRA = "https://thumbs.dreamstime.com/b/funny-cobra-wearing-sunglasses-studio-colorful-bright-background-created-generative-ai-277723926.jpg"
PANDA = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSS4YqkaiHiJ29r0xJSiaPmlAbvlHdSKMoV-A&s"
ZEBRA = "https://t4.ftcdn.net/jpg/06/01/35/87/360_F_601358710_FrekunRVshbs0LewSFg5KyxBtuT3K5Ur.jpg"
ANIMAL_DICT = {}

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# sends a message on startup
@bot.event
async def on_ready():
    print(START)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(START)

# makes 2 random animals fight each other
@bot.command()
async def fightrandom(ctx):

    animal1 = HF.random_animal()
    animal2 = HF.random_animal()
    
    animal1_poison = False
    animal2_poison = False
    poison = False
        
    if (animal1.is_poisonous()):
         animal2_poison = animal1.poison_animal()
            
    if (animal2.is_poisonous()):
        animal1_poison = animal2.poison_animal()
            
    if (animal1_poison or animal2_poison):
        poison = True
            
    round_num = 0
    while (animal1.health > 0 and animal2.health > 0):
        await HF.print_round(ctx, round_num)
        await HF.print_both_animals(ctx, animal1, animal2)
        await HF.print_attack(ctx, LEFT, animal1.attack(animal2))
        await HF.print_attack(ctx, RIGHT, animal2.attack(animal1))
        round_num += 1
        
    await HF.print_final_stats(ctx, animal1, animal2, poison)
        
    if (animal1.health <= 0 and animal2.health <= 0):
        await HF.print_tie_game(ctx)
        return
        
    if (animal1.health > 0):
        if (animal1_poison):
            await HF.print_tie_game(ctx)
            return
        if (isinstance(animal1, Carnivore)):
            animal1.eat_animal(animal2)
        elif (isinstance(animal1, Herbivore)):
            animal1.eat_plant()
            
        await HF.print_winner(ctx, LEFT)
    else:
        if (animal2_poison):
            await HF.print_tie_game(ctx)
            return
        if (isinstance(animal2, Carnivore)):
            animal2.eat_animal(animal1)
        elif (isinstance(animal2, Herbivore)):
            animal2.eat_plant()
            
        await HF.print_winner(ctx, RIGHT)

# makes 2 existing animals fight each other - accepts 2 arguments
@bot.command()
async def fight(ctx, animal1_name: str, animal2_name: str):
    if (animal1_name not in ANIMAL_DICT or animal2_name not in ANIMAL_DICT):
        await HF.send_to_channel(ctx, 
                                 "One or both of your animals don't exist!")
        return
    
    animal1 = ANIMAL_DICT[animal1_name]
    animal2 = ANIMAL_DICT[animal2_name]
    
    animal1_poison = False
    animal2_poison = False
    poison = False
        
    if (animal1.is_poisonous()):
         animal2_poison = animal1.poison_animal()
            
    if (animal2.is_poisonous()):
        animal1_poison = animal2.poison_animal()
            
    if (animal1_poison or animal2_poison):
        poison = True
            
    round_num = 0
    while (animal1.health > 0 and animal2.health > 0):
        await HF.print_round(ctx, round_num)
        await HF.print_both_animals(ctx, animal1, animal2)
        await HF.print_attack(ctx, animal1_name, animal1.attack(animal2))
        await HF.print_attack(ctx, animal2_name, animal2.attack(animal1))
        round_num += 1
        
    await HF.print_final_stats(ctx, animal1, animal2, poison)
        
    if (animal1.health <= 0 and animal2.health <= 0):
        await HF.print_tie_game(ctx)
        return
        
    if (animal1.health > 0):
        if (animal1_poison):
            await HF.print_tie_game(ctx)
            return
        if (isinstance(animal1, Carnivore)):
            animal1.eat_animal(animal2)
            await HF.send_to_channel(ctx, f"{animal1_name} ate {animal2_name}! {animal1_name}'s new strength is {animal1.strength}!")
        elif (isinstance(animal1, Herbivore)):
            animal1.eat_plant()
            await HF.send_to_channel(ctx, f"{animal1_name} ate a plant! {animal1_name}'s new strength is {animal1.strength}!")
            
        await HF.print_winner(ctx, animal1_name)
    else:
        if (animal2_poison):
            await HF.print_tie_game(ctx)
            return
        if (isinstance(animal2, Carnivore)):
            animal2.eat_animal(animal1)
            await HF.send_to_channel(ctx, f"{animal2_name} ate {animal1_name}! {animal2_name}'s new strength is {animal2.strength}!")
        elif (isinstance(animal2, Herbivore)):
            animal2.eat_plant()
            await HF.send_to_channel(ctx, f"{animal2_name} ate a plant! {animal2_name}'s new strength is {animal2.strength}!")
        await HF.print_winner(ctx, animal2_name)

# creates a wolf with either customized or random stats
@bot.command()
async def wolf(ctx, age: int = 0, health: float = 0, strength: float = 0, 
               name: str = ""):
    if (name in ANIMAL_DICT):
        await HF.send_to_channel(ctx, "This name is already in use!")
        return
    if (age == 0):
        age = HF.random_age(HF.MAX_AGE)
    if (health == 0):
        health = HF.MAX_HP
    if (strength == 0):
        strength = HF.random_strength(HF.MAX_STRENGTH)
    if (name == ""):
        name = chr(rand.randint(MIN_ASCII_CHAR, MAX_ASCII_CHAR))
    new_wolf = Wolf(age, health, strength)
    ANIMAL_DICT[name] = new_wolf
    await HF.send_to_channel(ctx, "You created a new Wolf!")
    await HF.send_to_channel(ctx, WOLF)
    await HF.send_to_channel(ctx, f"Age: {age}  Health: {health:.2f}\
  Strength: {strength:.2f}  Name: {name}")

# creates a leopard with either customized or random stats
@bot.command()
async def leopard(ctx, age: int = 0, health: float = 0, strength: float = 0, 
                  name: str = ""):
    if (name in ANIMAL_DICT):
        await HF.send_to_channel(ctx, "This name is already in use!")
        return
    if (age == 0):
        age = HF.random_age(HF.MAX_AGE)
    if (health == 0):
        health = HF.MAX_HP
    if (strength == 0):
        strength = HF.random_strength(HF.MAX_STRENGTH)
    if (name == ""):
        name = chr(rand.randint(MIN_ASCII_CHAR, MAX_ASCII_CHAR))
    new_leopard = Leopard(age, health, strength)
    ANIMAL_DICT[name] = new_leopard
    await HF.send_to_channel(ctx, "You created a new Leopard!")
    await HF.send_to_channel(ctx, LEOPARD)
    await HF.send_to_channel(ctx, f"Age: {age}  Health: {health:.2f}\
  Strength: {strength:.2f}  Name: {name}")
   
# creates a toad with either customized or random stats 
@bot.command()
async def toad(ctx, age: int = 0, health: float = 0, strength: float = 0, 
               name: str = ""):
    if (name in ANIMAL_DICT):
        await HF.send_to_channel(ctx, "This name is already in use!")
        return
    if (age == 0):
        age = HF.random_age(HF.MAX_AGE)
    if (health == 0):
        health = HF.MAX_HP
    if (strength == 0):
        strength = HF.random_strength(HF.MAX_STRENGTH)
    if (name == ""):
        name = chr(rand.randint(MIN_ASCII_CHAR, MAX_ASCII_CHAR))
    new_toad = Toad(age, health, strength)
    ANIMAL_DICT[name] = new_toad
    await HF.send_to_channel(ctx, "You created a new Toad!")
    await HF.send_to_channel(ctx, TOAD)
    await HF.send_to_channel(ctx, f"Age: {age}  Health: {health:.2f}\
  Strength: {strength:.2f}  Name: {name}")

# creates a cobra with either customized or random stats
@bot.command()
async def cobra(ctx, age: int = 0, health: float = 0, strength: float = 0, 
                name: str = ""):
    if (name in ANIMAL_DICT):
        await HF.send_to_channel(ctx, "This name is already in use!")
        return
    if (age == 0):
        age = HF.random_age(HF.MAX_AGE)
    if (health == 0):
        health = HF.MAX_HP
    if (strength == 0):
        strength = HF.random_strength(HF.MAX_STRENGTH)
    if (name == ""):
        name = chr(rand.randint(MIN_ASCII_CHAR, MAX_ASCII_CHAR))
    new_cobra = Cobra(age, health, strength)
    ANIMAL_DICT[name] = new_cobra
    await HF.send_to_channel(ctx, "You created a new Cobra!")
    await HF.send_to_channel(ctx, COBRA)
    await HF.send_to_channel(ctx, f"Age: {age}  Health: {health:.2f}\
  Strength: {strength:.2f}  Name: {name}")

# creates a panda with either customized or random stats
@bot.command()
async def panda(ctx, age: int = 0, health: float = 0, strength: float = 0, 
                name: str = ""):
    if (name in ANIMAL_DICT):
        await HF.send_to_channel(ctx, "This name is already in use!")
        return
    if (age == 0):
        age = HF.random_age(HF.MAX_AGE)
    if (health == 0):
        health = HF.MAX_HP
    if (strength == 0):
        strength = HF.random_strength(HF.MAX_STRENGTH)
    if (name == ""):
        name = chr(rand.randint(MIN_ASCII_CHAR, MAX_ASCII_CHAR))
    new_panda = Panda(age, health, strength)
    ANIMAL_DICT[name] = new_panda
    await HF.send_to_channel(ctx, "You created a new Panda!")
    await HF.send_to_channel(ctx, PANDA)
    await HF.send_to_channel(ctx, f"Age: {age}  Health: {health:.2f}\
  Strength: {strength:.2f}  Name: {name}")

# creates a zebra with either customized or random stats
@bot.command()
async def zebra(ctx, age: int = 0, health: float = 0, strength: float = 0, 
                name: str = ""):
    if (name in ANIMAL_DICT):
        await HF.send_to_channel(ctx, "This name is already in use!")
        return
    if (age == 0):
        age = HF.random_age(HF.MAX_AGE)
    if (health == 0):
        health = HF.MAX_HP
    if (strength == 0):
        strength = HF.random_strength(HF.MAX_STRENGTH)
    if (name == ""):
        name = chr(rand.randint(MIN_ASCII_CHAR, MAX_ASCII_CHAR))
    new_zebra = Zebra(age, health, strength)
    ANIMAL_DICT[name] = new_zebra
    await HF.send_to_channel(ctx, "You created a new Zebra!")
    await HF.send_to_channel(ctx, ZEBRA)
    await HF.send_to_channel(ctx, f"Age: {age}  Health: {health:.2f}\
  Strength: {strength:.2f}  Name: {name}")
    
bot.run(BOT_TOKEN)