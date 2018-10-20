import discord
from discord.ext import commands

#If you haven't downloaded discord or python
#Type in google search python.org
#Search in python.org 3.6 and download the 64 bit version
#After all the downloads do:
#pip3 install discord
#or
#python install discord.py

client = commands.Bot(command_prefix="prefix here")

@client.event
async def on_ready():
    print("Ready to show you guys basic stuff!")
    
@client.command()
async def hey():
    await client.say("Hi dude!")
    
client.run("token")
