#!/usr/bin/env python
# coding: utf-8

# In[4]:


#help https://discordpy.readthedocs.io/en/stable/index.html
#https://www.youtube.com/watch?v=nW8c7vT6Hl4

import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '!')


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

    

client.run('process.env.BOT_TOKEN')

