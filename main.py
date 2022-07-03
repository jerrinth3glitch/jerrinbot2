
import discord
import os
from discord.ext import commands
import threading
import math
import random as r
import json

import openai


"""
for i in dir(openai):
    print(i)
print()
print("DEBUG                : ", openai.debug)
print("API_KEY            : ", openai.api_key)
print("API_KEY_PATH : ", openai.api_key_path)
print("API_TYPE         : ", openai.api_type)
print("API_VERSION    : ", openai.api_version)
print("APP_INFO         : ", openai.app_info)
print()
print(openai.log)
#print(openai.Search("test"))
input("waiting")
"""

clear = lambda: os.system('cls')
client = discord.Client()
bot = commands.Bot(command_prefix="?")
openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_TOKENS = 150


# List of channel IDs
startUp = 970213219945820160
botcomm = 972566324679147521
openAi    = 970214072052240424
openAiNSFW = 993244692718293013

red = "\u001b[31m"
reset = "\u001b[0m"

# Compiles bad words list for ai usage
badwords = open("badwords.txt", "r+")
badwords = badwords.readlines()
badwords = [i.replace("\n","") for i in badwords]
while "" in badwords:
    badwords.remove("")



lastmessages = []


# Load User dictionary file
def loadUserDict():
    with open("users.txt", "r") as f:
        data = f.read()
    return json.loads(data)


# Save User Dictionary file
def saveUserDict(userDict):
    try:
        with open("users.txt", "w") as f:
            json.dump(userDict, f)
    except:
        return False
    return True


try:
    users = loadUserDict()
except:
    users = {}
    



def checkBadWord(string):
    count = 0
    if string == "":
        return "I have no response."
    for i in badwords:
        if i in string:
            count += string.count(i)
            string = string.replace(i, "#"*len(i))
    return string, count
    

def formatBotMessage(text, rating = 0):
    if rating == 0: # is SFW
        text, count = checkBadWord(text).strip("\n")
        
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n","\n\n\n")
    text = text.replace("@everyone", "@every one")
    text = text.replace("@", "\@")
    
    for i in ">_|*":
        text = text.replace(i, "\\" + i)
    return text


def helpFunction():
    1
    

# BOT STARTUP CODE
bot.event
async def on_ready():
    channel = bot.get_channel(startUp)
    text = "Start up successful!"
    print(text)
    await channel.send(text)



# ON MESSAGE CODE
@bot.event
async def on_message(message):
    global lastmessages, users

        
    botChannel = bot.get_channel(botcomm)

    if message.author.bot: return



            
    # BOT COMMANDS CHANNEL
    if message.channel.id == botcomm:
        userID = str(message.author.id)
        if userID not in users:
            users[str(message.author.id)] = {}
        print(users)
        text = message.content
        if text.lower().startswith(",roll"):
            text = message.content
            try:
                args = int(text.split(" ")[1])
                num = random.randint(0, args)
                await botChannel.send(f"You rolled a {num}")
            except:
                print("error rolling number.")

        if text.lower().startswith(",blaze"):
            text = message.content
            try:
                num = random.randint(0, 2)
                if num == 2:
                    await botChannel.send("You got a blaze rod!")
                else:
                    await botChannel.send("You got icky glowstone.")
            except:
                print("blaze error?")
    saveUserDict(users)





    
        
    # AI CHANNEL
    aiChannels = [openAi, openAiNSFW, 993256836822224926]
    if message.channel.id in aiChannels:
        
        isNSFW = aiChannels.index(message.channel.id)
        CopenAi = bot.get_channel(aiChannels[isNSFW])
        optionEmbed = True

        msg = message.content
        if not msg.lower().startswith("ai"): 
            return
            
        if msg.lower().startswith("ai.e "):
            optionEmbed = False
            msg = "ai" + msg[4:]
            
        # prevents repeated messages lol
        if msg in lastmessages and "random" not in msg:
            return
        else:
            lastmessages.append(msg)
                    
        if len(lastmessages) >= 10:
            lastmessages = [lastmessages[len(lastmessages)-10:]]


        async with message.channel.typing():

            # DEALING WITH ARGUMENTS
            if msg.lower().startswith("ai giant"):
                maxTokens = 2000
                msg = msg[9:]
                randomness = 0.0
            elif msg.lower().startswith("ai long"):
                maxTokens = 500
                msg = msg[8:]
                randomness = 0.0
            elif msg.lower().startswith("ai random"):
                randomness = 0.5
                maxTokens = MAX_TOKENS
                msg = msg[10:]
            elif msg.lower().startswith("ai help"):
                helpFunction()
            else:
                randomness = 0.0
                maxTokens = MAX_TOKENS
                msg = msg[3:]

    
    
            #try:
            if True:
                print(red + "isNSFW:", ["False","True"][isNSFW ** 0] + reset)
                print(red + msg + reset)
                engines = ["text-davinci-002", "text-ada-001"]
                response = openai.Completion.create(
                engine=engines[0],
                prompt=msg,
                temperature=randomness,
                max_tokens=maxTokens,
                top_p=1.0,
                frequency_penalty=1.0,
                presence_penalty=0.0)
                    
                print(response)

                finish_reason = response['choices'][0]['finish_reason']
                text = response['choices'][0]['text']

                # Format response
         
                if len(text) > 1900: text = text[:1900]
                    
                text = formatBotMessage(text, isNSFW)

                # Try using \"long\" or \"giant\" after the ai keyword for a bigger response!
                if finish_reason == "length":
                    description = f"**Showing first {MAX_TOKENS} tokens of response.\n**" + text + "..."
                else:
                    description = text

                # Creates title for embed
                if optionEmbed == False:
                    await CopenAi.send(text, reference=message)
                    
                else:
                    if len(text) < 50:
                        title = msg
                        title = formatBotMessage(msg, isNSFW)
                        embed = discord.Embed(title=title, description=description, color=discord.Color.purple())
                        await CopenAi.send(embed=embed, reference=message)
                        print(openai.log)
                    else:
                        embed = discord.Embed(description=description, color=discord.Color.purple())
                        await CopenAi.send(embed=embed, reference=message)
                        print(openai.log)
      
            #except:
            #    await CopenAi.send("<@611427346099994641> There has been an error of some sort.", reference=message)
                    
            
            

            

    


bot.run(os.getenv("TOKEN"))
