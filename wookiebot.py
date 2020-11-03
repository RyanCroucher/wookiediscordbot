import os
import random
#import nationdistributor.py

import discord
from dotenv import load_dotenv
from pathlib import Path

from discord.ext import commands

env_path = Path('.') / '.env'
load_dotenv(env_path)
TOKEN = os.getenv('DISCORD_TOKEN')
BOIZ_DISCORD = os.getenv('BOIZ_DISCORD')
RPG_DISCORD = os.getenv('RPG_DISCORD')

bot = commands.Bot(command_prefix='!')
bot.last_author = ''
bot.message_content = ''

#client = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_message(message):
    
    #if '!' not in message.content and message.author.id != bot.user.id:
    if '!' not in message.content and 'That last comment' not in message.content:
        bot.last_author = message.author
        bot.message_content = message.content

    await bot.process_commands(message)

@bot.command(name='?')
async def q(ctx):
    await quotes.invoke(ctx)
@bot.command(name='quote')
async def quotes(ctx, *args):
    
    relevant_quotes = []
    infile = ''
    specific_word = ''
    
    for arg in args:
        arg = arg.lower()   
    
        if 'dnd' in arg:
            infile = open('dnd_quotes.txt')
    
        elif 'toxic' in arg:
            infile = open('boiz_quotes.txt')
    
        elif 'deep' in arg:
            infile = open('deep.txt')
            
        elif 'oracle' in arg:
            infile = open('oracle.txt')
            break
            
        elif 'aquinas' in arg:
            infile = open('aquinas.txt')
        
        else:
            if arg:
                specific_word = arg
                break
        
    if not infile:        
        if ctx.guild.name == BOIZ_DISCORD:
            infile = open('boiz_quotes.txt')
         
        elif ctx.guild.name == RPG_DISCORD:
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
    if ctx.guild.name == BOIZ_DISCORD:
        infile = open('boiz_quotes.txt', 'a')
        infile.write(' '.join(arg) + '\n')
        infile.close()
        await ctx.send("Successfully added a new quote to " + infile.name)
    elif ctx.guild.name == RPG_DISCORD:
        infile = open('dnd_quotes.txt', 'a')
        infile.write(' '.join(arg) + '\n')
        infile.close()
        await ctx.send("Successfully added a new quote to " + infile.name)
        
#@bot.command(name='randomnations')
#async def randomnations(ctx):
    #if ctx.guild.name == "Not so much D&D. Mostly CSGO":
        #nationdistributor.main()

@bot.command(name='npc')
async def npc(ctx, *, arg):
    
    relevant_npcs = []
    specific_word = ''

    arg = arg.lower()   
    if arg == 'all':
        pass
    
    else:
        if arg:
            specific_word = arg  

    infile = open('npcs.txt')
    relevant_npcs = infile.read().splitlines()    
    infile.close() 
    
    if specific_word:
        relevant_npcs = [n for n in relevant_npcs if specific_word in n.lower()]
    
    if relevant_npcs:
        
        await ctx.guild.get_member(bot.user.id).edit(nick='WookieBot')
        if specific_word:

            specific_npc = relevant_npcs
            await ctx.send(f"NPC definitions containing '{arg}' in {infile.name}")

            i = 0
            batch_size = 5
            while i < len(specific_npc):
                response = '\n'.join(npc for npc in sorted(specific_npc)[i:i + batch_size])
                response = response.lower().replace(specific_word.lower(), f'**{specific_word.lower()}**')
                await ctx.send(response)
                i += batch_size            
        else:
            await ctx.send(f"All NPC definitions in {infile.name}")
            i = 0
            batch_size = 5
            while i < len(relevant_npcs):
                response = '\n'.join(npc for npc in sorted(relevant_npcs)[i:min(len(relevant_npcs), i + batch_size)])
                await ctx.send(response)
                i += batch_size
            
    else:
        if specific_word:
            await ctx.send(f"Couldn't find NPC definitions containing '{arg}' in {infile.name}") 
        else:
            await ctx.send(f"Couldn't find any NPC in {infile}") 
        
@bot.command(name='addnpc')
async def addnpc(ctx, *, arg):
    if ctx.guild.name == RPG_DISCORD:
        infile = open('npcs.txt', 'a')
        infile.write(''.join(arg) + '\n')
        infile.close()
        await ctx.send("Successfully added a new NPC to " + infile.name)      
    else:
        await ctx.send("Can't add NPCs from this discord server!")
        
        
@bot.command(name='kills')
async def kills(ctx, *arg):
    if not arg:
        arg = "all"
    else:
        arg = arg[0]
        
    relevant_kills = []
    chars = ["Humphrey D. Cobblebottom", "Kai", "Kairos", "Pasha Singh", "The Sultan"]
    specific_char = None

    arg = arg.lower()   
    if arg != 'all':
        for char in chars:
            if arg.lower() in char.lower():
                specific_char = char
                break
        else:
            await ctx.send("Character not recognised, showing all kills:")
        
    infile = open('kills.txt', 'r', encoding="utf-8")
    relevant_kills = infile.read().splitlines()    
    infile.close()
    
    
    await ctx.guild.get_member(bot.user.id).edit(nick='WookieBot')    
        
    if specific_char:
        await ctx.send(f"Kill records of '{char}' in {infile.name}")
        char_kill_dict, char_kill_list = get_char_kills(char, relevant_kills)
        
        total_unique_kills = len(char_kill_dict)
        total_kills = sum(char_kill_dict.values())
        highest_cr_kill = max(w[1] for w in char_kill_list)
        strongest_kill = set([kill[0] for kill in char_kill_list if kill[1] == highest_cr_kill])
        
        response = f"Total kills: {total_kills}\nStrongest Kill(s): {', '.join(strongest_kill)} (CR: {highest_cr_kill})\n"
        #await ctx.send(stats) 
        
        response += 'All kills: ' + ', '.join(f'{kill}\*{num}' for kill, num in char_kill_dict.items())
        response = response.replace('\*1', '')
        await ctx.send(response)         
    else:
        await ctx.send(f"All kill records (sorted by CR) in {infile.name}")
        response = ''
        for char in chars:
            char_kill_dict, _ = get_char_kills(char, relevant_kills)

            response += char + ': ' + ', '.join(f'{kill}\*{num}' for kill, num in char_kill_dict.items()) + '\n'
        response = response.replace('\*1', '')
        await ctx.send(response)     

def get_char_kills(char, data):
    
    char_kills = {}

    char_kill_list = [(w[1], int(w[2])) for k in data for w in [k.split('|')] if w[0] == char]

    for kill in sorted(char_kill_list, key=lambda x: x[1], reverse=True):
        enemy_name = kill[0]
        char_kills[enemy_name] = char_kills.get(enemy_name, 0) + 1
        
    return char_kills, char_kill_list
        
@bot.command(name='addkill')
async def addkill(ctx, character, enemy, cr='0'):
    if ctx.guild.name == RPG_DISCORD:
        
        enemy = enemy.title()
        
        chars = ["Humphrey D. Cobblebottom", "Kai", "Kairos", "Pasha Singh", "The Sultan"]
        selected_char = None
        for char in chars:
            if character.lower() in char.lower():
                selected_char = char
                break
        if selected_char is None:
            await ctx.send("No such character. Pick from:")
            await ctx.send('\n'.join(char for char in chars))
            return
            
        if cr != 0 and not cr.isnumeric():
            await ctx.send(f"{cr} is not an appropriate CR number.")
            return        
            
        infile = open('kills.txt', 'a')
        infile.write(f"{selected_char}|{enemy}|{cr}\n")
        infile.close()
        await ctx.send(f"Recorded kill: {selected_char} killed a {enemy} (CR {cr})")   
                 
    else:
        await ctx.send("Can't record kills from this discord server!")
        
@bot.command(name='gods')
async def gods(ctx, *, arg):
    relevant_gods = []
    specific_word = ''

    arg = arg.lower()   
    if arg == 'all' or not arg:
        pass
    
    else:
        specific_word = arg
        
    infile = open('gods.txt', 'r', encoding="utf-8")
    relevant_gods = infile.read().splitlines()    
    infile.close()
    
    
    await ctx.guild.get_member(bot.user.id).edit(nick='WookieBot')    
        
    if specific_word:
        relevant_gods = [n for n in relevant_gods if specific_word.lower() in n.lower()]
        await ctx.send(f"Deity definitions containing '{arg}' in {infile.name}")
        i = 0
        batch_size = 2
        while i < len(relevant_gods):
            response = '\n\n'.join(god for god in sorted(relevant_gods)[i:i + batch_size])
            response = response.lower().replace(specific_word.lower(), f'**{specific_word.lower()}**')
            if response:
                await ctx.send(response + '\n\n')
            i += batch_size
    else:
        relevant_gods = [n[:n.find(')')+1] for n in sorted(relevant_gods) if ':' in n and ')' in n]
        await ctx.send(f"All deity definitions in {infile.name}")
        i = 0
        batch_size = 5
        while i < len(relevant_gods):
            response = '\n'.join(god for god in sorted(relevant_gods)[i:i + batch_size])
            await ctx.send(response)
            i += batch_size        
        
@bot.command(name='howtoxic')
async def howtoxic(ctx):
    #toxicity_level = random.randint(0, 100)
    toxic_words = [
    ('meme', 5),('wookie', 5),('angus', 5),('succundo', 5),('grudge', 5), ('attrition', 5),
    ('ryan',10),('farscape', 10),('simon',10),('remove', 10),('gold', 10),('aussie', 10),('geld', 10),('eamon',10), ('goat', 10), ('madcow', 10),('meta', 10),('dying', 10), ('gaslight', 10),
    ('pico', 15),('dick', 15),('stupid', 15),('owned', 15),('pussies',15),('snake',15),('carrion', 15), ('rat', 15),
    ('toxic', 20), ('toxicity', 20), ('kicked', 20), ('unfriending', 20), ('gaslighting', 20), ('fuck', 20), ('fucker', 20), ('shit', 20),('crying', 20),('execute', 20),('execution',20), 
    ('sheckles', 25),('jew', 25),('just you', 25),('retards', 30),('phate', 40),('redacted', 40), ('homolust', 40)
    ]
    
    nick = bot.last_author.name
    if ctx.guild.get_member(bot.last_author.id):
        nick = ctx.guild.get_member(bot.last_author.id).display_name

    total_toxicity = 0
    toxic_word_count = 0
    for toxic_word in toxic_words:
        if toxic_word[0] in bot.message_content.lower() or toxic_word[0] in nick.lower():
            toxic_word_count += bot.message_content.lower().count(toxic_word[0]) + nick.lower().count(toxic_word[0])
            total_toxicity += toxic_word[1]
    total_toxicity *= (1+toxic_word_count)/(len(bot.message_content.split())/3)
    #toxicity_level = sum(ord(c) for c in bot.message_content) % 100
    toxicity_level = total_toxicity + len(bot.message_content.split())/2
    await ctx.guild.get_member(bot.user.id).edit(nick='ToxicityBot')
    await ctx.send(f"That last comment by {nick} was {toxicity_level:.1f}% toxic.")
    #await ctx.send(f"That last comment was {toxicity_level}% toxic.")
    
    
@bot.command(name='meme')
async def meme(ctx, *args):
    
    await ctx.guild.get_member(bot.user.id).edit(nick='ToxicityBot') 
    
    memes = []
    specific_word = ''
 
    for arg in args:
        arg = arg.lower()
        if arg:
            specific_word = arg
            break
        
    infile = open('images.txt', 'r', encoding="utf-8")
    data = infile.read().splitlines()    
    infile.close()
    
    if specific_word:
        memes = [m[m.rfind(',')+1:] for m in data if specific_word in m.lower()]
    else:
        memes = [m[m.rfind(',')+1:] for m in data]
    
    if memes:
        meme = random.choice(memes).strip()
        await ctx.send(meme)
        
@bot.command(name='rat')
async def rat(ctx, *args):
    
    rats = [
    "https://thespinoff.co.nz/wp-content/uploads/2020/08/rat.jpg",
    "https://cdn.discordapp.com/attachments/362888280519213058/764082895907979274/norway-rat-illustration_1855x1218.jpg",
    "https://ichef.bbci.co.uk/news/1024/cpsprodpb/BEE1/production/_110356884_gettyimages-89167609.jpg",
    "https://thisnzlife.co.nz/wp-content/uploads/2017/02/ratsjpg3.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQXSf8544aAQGlSBW6HJPhuXTo82oJHiQKIRA&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQaYlgyFy703KLObpPHqulz5JFDC5szbaJ_bQ&usqp=CAU",
    ]
    
    name = ''
    for arg in args:
        if arg:
            name = arg
            break
    if name:
        await ctx.guild.get_member(bot.user.id).edit(nick=f'{name.capitalize()} The Rat')
    else:
        await ctx.guild.get_member(bot.user.id).edit(nick='Rat')
    rat = random.choice(rats)    
    await ctx.send(rat)
    message = "squeek "*random.randint(1,3)
    await ctx.send(f"{message.strip().capitalize()}.",tts=True)

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
                dice_string = f"{dice_string} {cur_operator} {coefficient}"
                cur_operator = ''
            num_rolls += 1
            grand_total += dice_total
            await ctx.send(f"{dice_string}: {dice_total}")
            #await ctx.send(dice_string + ": " + str(dice_total)
    if num_rolls > 1:
        await ctx.send(f"Total: {grand_total}")

def main():
    bot.run(TOKEN)

main()