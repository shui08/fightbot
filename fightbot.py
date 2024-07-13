# TODO: FIX A, H, S SPACING DURING FIGHT, ADD ABILITY TO CREATE WHATEVER ANIMALS
# YOU WANT, ADD REPRODUCE, REVIEW ALL OF CODE
import os
from dotenv import load_dotenv, dotenv_values
from discord.ext import commands
import discord
import random as rand
import HelperFunctions
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
MAX_STRENGTH = 200
MIN_AGE_REP = 5
BABY_HP = 100

load_dotenv()
BOT_TOKEN = f"{os.getenv('FIGHTBOT_TOKEN')}"
CHANNEL_ID = 1254308135334838272

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# event: sends a message on startup
@bot.event
async def on_ready():
    print("fightbot start!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("fightbot start!")

# command: makes 2 random animals fight each other
@bot.command()
async def fightrandom(ctx):

    animal1 = random_animal()
    animal2 = random_animal()
    
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
        await print_round(ctx, round_num)
        await print_both_animals(ctx, animal1, animal2)
        await print_attack(ctx, LEFT, animal1.attack(animal2))
        await print_attack(ctx, RIGHT, animal2.attack(animal1))
        round_num += 1
        
    await print_final_stats(ctx, animal1, animal2, poison)
        
    if (animal1.health <= 0 and animal2.health <= 0):
        await print_tie_game(ctx)
        return
        
    if (animal1.health > 0):
        if (animal1_poison):
            await print_tie_game(ctx)
            return
        if (isinstance(animal1, Carnivore)):
            animal1.eat_animal(animal2)
        elif (isinstance(animal1, Herbivore)):
            animal1.eat_plant()
            
        await print_winner(ctx, LEFT)
    else:
        if (animal2_poison):
            await print_tie_game(ctx)
            return
        if (isinstance(animal2, Carnivore)):
            animal2.eat_animal(animal1)
        elif (isinstance(animal2, Herbivore)):
            animal2.eat_plant()
            
        await print_winner(ctx, RIGHT)

# sends messages to discord channel
async def send_to_channel(ctx, message):
    await ctx.send(message)

# Functions to format and send specific messages
async def print_round(ctx, round_num):
    message = f"Round {round_num}:"
    await send_to_channel(ctx, message)

async def print_both_animals(ctx, animal1, animal2):
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
    await send_to_channel(ctx, "```" + str_result + "```")

async def print_attack(ctx, side, damage):
    message = f"{side} does {damage:.2f} damage!"
    await send_to_channel(ctx, message)

async def print_final_stats(ctx, animal1, animal2, poisoned):
    await print_both_animals(ctx, animal1, animal2)
    if (poisoned):
        await send_to_channel(ctx, "An animal was poisoned.")

async def print_tie_game(ctx):
    await send_to_channel(ctx, "-------GAME OVER-------")
    await send_to_channel(ctx, "TIE: Both animals died!")

async def print_winner(ctx, side):
    await send_to_channel(ctx, "-------GAME OVER-------")
    await send_to_channel(ctx, f"{side} animal wins!")

# Helper function to calculate spacing
def calc_spacing(string):
    total_width = SPACING
    str1_width = len(string)
    spacing = total_width - str1_width
    if (spacing < 0):
        return 0
    return spacing

# Function to generate a random animal
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

# Function to generate a random age
def random_age(max):
    rand_age = rand.randint(0, max)
    return rand_age

# Function to generate a random strength
def random_strength(max):
    rand_strength = rand.uniform(0, max)
    return rand_strength
    
bot.run(BOT_TOKEN)