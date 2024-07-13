# TODO: FIX A, H, S SPACING DURING FIGHT, ADD ABILITY TO CREATE WHATEVER ANIMALS
# YOU WANT, ADD REPRODUCE, REVIEW ALL OF CODE
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
CHANNEL_ID = 1254308135334838272

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# sends a message on startup
@bot.event
async def on_ready():
    print("fightbot start!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("fightbot start!")

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
        await HF.print_attack(ctx, "Left", animal1.attack(animal2))
        await HF.print_attack(ctx, "Right", animal2.attack(animal1))
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
            
        await HF.print_winner(ctx, "Left")
    else:
        if (animal2_poison):
            await HF.print_tie_game(ctx)
            return
        if (isinstance(animal2, Carnivore)):
            animal2.eat_animal(animal1)
        elif (isinstance(animal2, Herbivore)):
            animal2.eat_plant()
            
        await HF.print_winner(ctx, "Right")
    
bot.run(BOT_TOKEN)