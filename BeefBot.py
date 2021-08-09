#!/usr/bin/env python
# coding: utf-8
# help https://discordpy.readthedocs.io/en/stable/index.html
# https://www.youtube.com/watch?v=nW8c7vT6Hl4

import os
import io
import discord
import requests
from discord_slash import SlashCommand
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from github import Github
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

STARDEW_BASE_URL = 'https://stardewvalleywiki.com/'
SVE_WIKI_BASE_URL = 'https://stardew-valley-expanded.fandom.com/wiki/'
guild_ids = [168168226994388992, 707683542238494760]

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)
# github credential setup
github = Github(os.getenv("GITHUB_TOKEN"))
repo = github.get_user().get_repo('beef-bot-discord')
#path in repo
x = repo.get_git_refs()
for y in x:
    print(y)
dataRef = repo.get_git_ref("heads/data")

pieChartName = 'pie.png'
filename = 'messagesLog.csv'
msgAnalysisLimit = 1000


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.listen('on_message')
async def on_message(message):
    if message.author == client.user:  # not recursive
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
async def ping(ctx):  # context = ctx
    await ctx.send('Pong!')


@client.command(pass_context = True)
async def pog(ctx):  # context = ctx
    # pogArr = ['475181449105113098', '475181455354494986', '475181460924661760', '475181470294474762', '475181475851927571', '475181481338077185', '475181486878752768', '475181492163706881', '475181497905577984']
    pogArr = ['<:1_:475181449105113098>',
               '<:2_:475181455354494986>',
               '<:3_:475181460924661760>',
               '<:4_:475181470294474762>',
               '<:5_:475181475851927571>',
               '<:6_:475181481338077185>',
               '<:7_:475181486878752768>',
               '<:8_:475181492163706881>',
               '<:9_:475181497905577984>']
    # emojiArr = []
    # for i in pogArr:
    #     emoji = i
    await ctx.send(f'{pogArr[0]}{pogArr[1]}{pogArr[2]}\n{pogArr[3]}{pogArr[4]}{pogArr[5]}\n{pogArr[6]}{pogArr[7]}{pogArr[8]}\n')
    await ctx.message.delete()


@client.command()
async def beef(ctx, name):  # context = ctx
    await ctx.send(f"""I'm telling you, {name} is as cracked as he is jacked. I saw him at a 7-11 the other day buying Monster and adult diapers. I asked him what the diapers were for and he said "they contain my full power so I don’t completely shit on these kids" then he rode a boar out the door""")


@client.command(aliases=['aidan'])
async def Aidan(ctx):  # context = ctx
    await ctx.send('Aidan is significantly more attractive and more interesting than me, and so is his girlfriend. My girlfriend is very ugly. And so am I. These are facts. Debate me.')


@client.command()  # message analysis
async def msgAnal(ctx):
    messages = await ctx.channel.history(limit=msgAnalysisLimit).flatten()

    # Save contents to get sha every time analysis is done: new file every time!
    csvFile = repo.get_contents(filename, ref="heads/data")

    msgDict = {}
    for msg in messages:
        if msg.author != client.user:
            if msg.author.name in msgDict.keys():
                msgDict.update({msg.author.name: msgDict[msg.author.name] + 1})
            else:
                msgDict[msg.author.name] = 1
    # dataframe for plot visualization
    df = pd.DataFrame(msgDict.items(), columns=["Name", "Messages Sent"])
    df = df.set_index('Name')
    df = df.sort_values(by="Messages Sent", ascending=False)
    pieDf = df.head(15)
    piePlot = (pieDf.plot(x="Name", y="Messages Sent",
               kind="pie", autopct='%1.1f%%', figsize=(13, 10)))
    piePlot.legend(bbox_to_anchor=(0.85, 0.9),
                   bbox_transform=plt.gcf().transFigure)
    piePlot.set_title("Proportion of Messages Sent", fontsize=25)
    plt.ylabel(None)
    plt.tight_layout()
    piePlotFig = piePlot.get_figure()
    piePlotFig.savefig(pieChartName)
    image = discord.File(pieChartName)
    await ctx.send(file=image)
    channelName = str(ctx.channel)

    stringFormat = ''
    arr = []
    for x, y in msgDict.items():
        arr.append([x, y])
    for z in range(2):
        for i in arr:
            stringFormat += str(i[z])
            stringFormat += ','
        stringFormat = stringFormat[:-1]
        stringFormat += '\n'

    # await ctx.send('Anal in progress')
    # creates csv file in github in data branch (not main!)
    repo.update_file(filename, "PyGithub - messages data csv",
                     stringFormat, csvFile.sha, branch="data")
    print('Finished', ctx.channel)
    await ctx.send('Anal Finished :)')

@slash.slash(name = 'stardewGifts', guild_ids = guild_ids,
            description = "Shows Liked/Loved gifts for NPCs in Stardew Valley Expanded",
            options = [
                    create_option(
                        name = "npc",
                        description = "NPC added in Stardew Valley Expanded you want to gift, DOESN'T WORK for original characters",
                        option_type = 3,
                        required = True
                    )
            ])
async def _stardewGifts(ctx, npc: str):
    npc = npc.capitalize()
    #Navigate to npc page
    page = requests.get(SVE_WIKI_BASE_URL + npc)
    pageScraper = BeautifulSoup(page.content, 'html.parser')
    embed = discord.Embed(title = f"{npc}'s Loved/Liked Gifts",
                            url = SVE_WIKI_BASE_URL + npc,
                            color = 0xFF0000)
    npcPic = pageScraper.find(class_ = "image-thumbnail")
    imgTag = npcPic.find('img')
    thumbnailPic = imgTag['src']
    #Set embed thumbnail
    embed.set_thumbnail(url = thumbnailPic)
    lovedGiftTable = pageScraper.find_all("table", class_ = "article-table")[7]
    tableLen = len(lovedGiftTable.find_all('tr'))
    embed.add_field(name = "Loved", value = f"{npc} loves these", inline = False)
    for i in range(2, tableLen):
        gift = lovedGiftTable.select('tr')[i]
        pic = gift.select('td')[0]
        giftImg = pic.find('img')
        giftImg = giftImg['data-src']
        item = gift.select('td')[1]
        name = item.text.strip()
        link = item.find('a')
        link = link['href']
        if 'stardewvalleyexpanded' not in link:
            link = SVE_WIKI_BASE_URL + link
        embed.add_field(name = name, value = link, inline = True)
    embed.add_field(name = "Liked", value = f"{npc} likes these", inline = False)
    likedGiftTable = pageScraper.find_all("table", class_ = "article-table")[8]
    tableLen = len(likedGiftTable.find_all('tr'))
    for i in range(2, tableLen):
        gift = likedGiftTable.select('tr')[i]
        pic = gift.select('td')[0]
        giftImg = pic.find('img')
        giftImg = giftImg['data-src']
        item = gift.select('td')[1]
        name = item.text.strip()
        link = item.find('a')
        link = link['href']
        if 'stardewvalleyexpanded' not in link:
            link = SVE_WIKI_BASE_URL + link
        embed.add_field(name = name, value = link, inline = True)
    await ctx.send(embed = embed)

@slash.slash(name = 'stardewBaseGifts', guild_ids = guild_ids,
            description = "Shows Liked/Loved gifts for base NPCs in Stardew Valley",
            options = [
                    create_option(
                        name = "npc",
                        description = "Original NPC in Stardew Valley you want to gift to",
                        option_type = 3,
                        required = True
                    )
            ])
async def _stardewBaseGifts(ctx, npc: str):
    npc = npc.capitalize()
    #Navigate to npc page
    page = requests.get(STARDEW_BASE_URL + npc)
    pageScraper = BeautifulSoup(page.content, 'html.parser')
    embed = discord.Embed(title = f"{npc}'s Loved/Liked Gifts",
                            url = STARDEW_BASE_URL + npc,
                            color = 0xFF0000)
    npcPic = pageScraper.find_all('ul', class_ = "gallery")[1]
    imgTag = npcPic.find_all('img')[0]
    # imgTag = npcPic.find('img')
    thumbnailPic = STARDEW_BASE_URL + imgTag['src']
    #Set embed thumbnail
    embed.set_thumbnail(url = thumbnailPic)
    lovedGiftTable = pageScraper.find_all(id = "roundedborder")[0]
    tableLen = len(lovedGiftTable.find_all('tr'))
    embed.add_field(name = "Loved", value = f"{npc} loves these", inline = False)
    for i in range(2, tableLen):
        gift = lovedGiftTable.select('tr')[i]
        pic = gift.select('td')[0]
        item = gift.select('td')[1]
        name = item.text.strip()
        link = item.find('a')
        link = link['href']
        if 'stardewvalley' not in link:
            link = STARDEW_BASE_URL + link
        embed.add_field(name = name, value = link, inline = True)
    embed.add_field(name = "Liked", value = f"{npc} likes these", inline = False)
    likedGiftTable = pageScraper.find_all(id = "roundedborder")[1]
    tableLen = len(likedGiftTable.find_all('tr'))
    for i in range(2, tableLen):
        gift = likedGiftTable.select('tr')[i]
        pic = gift.select('td')[0]
        item = gift.select('td')[1]
        name = item.text.strip()
        link = item.find('a')
        link = link['href']
        if 'stardewvalley' not in link:
            link = STARDEW_BASE_URL + link
        embed.add_field(name = name, value = link, inline = True)
    await ctx.send(embed = embed)

client.run(os.getenv('BOT_TOKEN'))
