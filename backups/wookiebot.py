import os
import random
#import nationdistributor.py

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

#client = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='?')
async def q(ctx):
    await quotes.invoke(ctx)
@bot.command(name='quote')
async def quotes(ctx, *args):
    
    relevant_quotes = []
    #players = ['thedarkdeathnz', 'aussie gold', 'geld', 'goat', 'madcowsteak', 'pico', 'whindghost', 'angus', 'succundo', 'fraser', 'simon', 'jamie', 'viruk', 'phate', 'wookie', 'blazier', 'flex']
    infile = ''
    specific_word = ''
    
    for arg in args:
        arg = arg.lower()
        #for player in players:
        #    if arg and arg in player:
        #        specific_player = arg
        #        break        
    
        if 'dnd' in arg:
            infile = open('dnd_quotes.txt')
            #break
    
        elif 'toxic' in arg:
            infile = open('boiz_quotes.txt')
            #break
    
        elif 'deep' in arg:
            infile = open('deep.txt')
            #break
            
        elif 'oracle' in arg:
            infile = open('oracle.txt')
            #break
            
        elif 'aquinas' in arg:
            infile = open('aquinas.txt')
            #break
        
        else:
            if arg:
                specific_word = arg
                #await ctx.send(f"Finding quotes containing '{arg}'") 
                break
        

    if not infile:        
        if ctx.guild.name == "Not so much D&D. Mostly CSGO":
            infile = open('boiz_quotes.txt')
         
        elif ctx.guild.name == "FarscapeCMDR - RPG server":
            infile = open('dnd_quotes.txt')

    relevant_quotes = infile.read().splitlines()    
    infile.close() 
    
    if specific_word:
        #await ctx.send(f"Finding quotes containing '{arg}'") 
        relevant_quotes = [q for q in relevant_quotes if specific_word in q.lower()]
        #print(relevant_quotes)
    
    if relevant_quotes:
        
        maxcount = 10
        count = 0
        response = ''
        while not response and count < maxcount:
            response = random.choice(relevant_quotes).strip('",')
            count += 1        
               
        name = response[response.rfind('-')+1:]
        if not name or len(name) > 32:
            name = 'WookieBot'
        response = response[:response.rfind('-')]
        
        await ctx.guild.get_member(bot.user.id).edit(nick=name)
        await ctx.send(response, tts=True)
    else:
        if specific_word:
            await ctx.send(f"Couldn't find quotes containing '{arg}' in {infile.name}") 
        else:
            await ctx.send(f"Couldn't find any quote in {infile}") 
    
@bot.command(name='addquote')
async def addquote(ctx, * arg):
    if ctx.guild.name == "Not so much D&D. Mostly CSGO":
        infile = open('boiz_quotes.txt', 'a')
        infile.write(' '.join(arg) + '\n')
        infile.close()
        await ctx.send("Successfully added a new quote to " + infile.name)
    elif ctx.guild.name == "FarscapeCMDR - RPG server":
        infile = open('dnd_quotes.txt', 'a')
        infile.write(' '.join(arg) + '\n')
        infile.close()
        await ctx.send("Successfully added a new quote to " + infile.name)
        
#@bot.command(name='randomnations')
#async def randomnations(ctx):
    #if ctx.guild.name == "Not so much D&D. Mostly CSGO":
        #nationdistributor.main()

@bot.command(name='roll')
async def roll_dice(ctx, *args):
    
    await ctx.send("Rolling {}...".format(' '.join(args)))
    
    grand_total = 0
    operators = ['+', '-']
    cur_operator = ''
    coefficient = 0
    num_rolls = 0
    
    for dice_string in args:
        dice_string = dice_string.lower().strip()
        for operator in operators:
            if len(dice_string) > 1 and operator in dice_string:
                cur_operator = operator
                coefficient = int(dice_string[dice_string.find(operator) + 1:])
                dice_string = dice_string[:dice_string.find(operator)]
                break
        num_dice = dice_string[:dice_string.find('d')]
        dice_sides = dice_string[dice_string.find('d') + 1:]
        dice_total = 0
        
        if num_dice.isnumeric() and dice_sides.isnumeric():
            if int(num_dice) > 100000:
                await ctx.send("Too many dice, don't be ridiculous!")
                break
            
            for i in range(int(num_dice)):
                dice_total += random.randint(1, int(dice_sides))
                
            if cur_operator:
                if cur_operator == '+':
                    dice_total += coefficient
                elif cur_operator == '-':
                    dice_total -= coefficient
            num_rolls += 1
            grand_total += dice_total
            await ctx.send(dice_total)
    if num_rolls > 1:
        await ctx.send(f"Total: {grand_total}")

def main():
    bot.run(TOKEN)

main()