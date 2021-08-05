#!/usr/bin/env python
# coding: utf-8

# In[4]:


#help https://discordpy.readthedocs.io/en/stable/index.html
#https://www.youtube.com/watch?v=nW8c7vT6Hl4

import os
import discord
from discord.ext import commands
from github import Github
import pandas as pd

client = commands.Bot(command_prefix = '!')
#github credential setup
github = Github(os.getenv("GITHUB_TOKEN"))
repo = github.get_user().get_repo('beef-bot-discord')
#path in repo
x = repo.get_git_refs()
for y in x:
    print(y)
dataRef = repo.get_git_ref("heads/data")

filename = 'messagesLog.csv'
msgAnalysisLimit = 25000

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




@client.listen('on_message')
async def on_message(message):
    if message.author == client.user: #not recursive
        return

    if '<@&867166985136504862>' in message.content:
        await message.channel.send('https://www.twitch.tv/notjiho')
    else:
        print(message.content)
    
    if 'booba' in message.content.lower():
        await message.channel.send('(.)(.)')
    if 'mommy' in message.content.lower():
        await message.channel.send('milky')



@client.command()
async def ping(ctx): #context = ctx
    await ctx.send('Pong!')

@client.command(aliases=['aidan'])
async def Aidan(ctx): #context = ctx
    await ctx.send('Aidan is significantly more attractive and more interesting than me, and so is his girlfriend. My girlfriend is very ugly. And so am I. These are facts. Debate me.')

@client.command() #message analysis
async def msgAnal(ctx):
    df = pd.DataFrame([[0]], index=[0], columns=['Filler'])
    massages = await ctx.channel.history(limit= msgAnalysisLimit).flatten()

    #Save contents to get sha every time analysis is done: new file every time!
    csvFile = repo.get_contents(filename, ref="heads/data")

    msgDict = {}
    for msg in massages:
        if msg.author != client.user:
            if msg.author.name in msgDict.keys():
                msgDict.update({msg.author.name: msgDict[msg.author.name] + 1})
            else:
                msgDict[msg.author.name] = 1
    channelName = str(ctx.channel)

    stringFormat = ''
    arr = []
    for x, y in msgDict.items():
        arr.append([x,y])
    for z in range(2):
        for i in arr:
            stringFormat += str(i[z])
            stringFormat += ','
        stringFormat = stringFormat[:-1]
        stringFormat += '\n'

    # await ctx.send('Anal in progress')
    #creates csv file in github in data branch (not main!)
    repo.update_file(filename, "PyGithub - messages data csv", stringFormat, csvFile.sha, branch = "data")
    print('Finished',ctx.channel)
    await ctx.send('Anal Finished :)')    

client.run(os.getenv('BOT_TOKEN'))
