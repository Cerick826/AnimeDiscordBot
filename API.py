from ast import alias
import datetime
from pydoc import synopsis
from unittest import result
import discord
import asyncio
import aiohttp
import random
import mysql.connector
import mal
from animec  import *
from discord import Embed
from operator import truediv
from discord_components import *
from discord.ext import commands
from click import CommandCollection
from utils import sortWatchList, check_format, check_ep_format

bot = commands.Bot(command_prefix="!", help_command=None)
bot.remove_command("help")
conn = mysql.connector.connect(
    host="sql3.freesqldatabase.com",
    port=3306,
    user="sql3474170",
    passwd="jmkGZaymNS",
    database="sql3474170",
)
cur = conn.cursor()


@bot.event
async def on_ready():
    print("Bot is ready and Online")
    global botON
    botON = True


@bot.event
async def on_message(message):
    global botON

    if message.author.bot:
        return
    if botON:
        if message.content.startswith("!hi"):
            await message.channel.send("hello!")

        if message.content.startswith("!leave"):
            await message.channel.send("I am leaving!")
            await bot.change_presence(status=discord.Status.invisible)

            botON = False

    if not (botON):
        if message.content.startswith("!join"):
            await message.channel.send("I am back!")
            await bot.change_presence(status=discord.Status.online)
            botON = True
    await bot.process_commands(message)


@bot.command(
    name="animeSearch",
    aliases=["AnimeSearch", "animesearch", "Animesearch"],
    pass_context=True,
)
async def animeSearch(ctx, *, arg):
    image = mal.AnimeSearch(arg)
    embed = discord.Embed(
        title="Anime Search Result",
        description=image.results[0].title,
        color=0xF2D026,
    )
    embed.add_field(name="Synopsis", value=image.results[0].synopsis)
    embed.add_field(name="Episodes", value=image.results[0].episodes, inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=image.results[0].image_url)
    await ctx.send(embed=embed)

@bot.command(
    name="relAnime",
    aliases=["RelAnime", "relanime", "Re;anime"],
    pass_context=True,
)
async def relAnime(ctx, *, arg):
    animeTitle = mal.AnimeSearch(arg)
    animeTitleID = animeTitle.results[0].mal_id
    related = mal.Anime(animeTitleID).related_anime

    embed = discord.Embed(
        title="Affiliated Work Relating to this Anime",
        description=animeTitle.results[0].title,
        color=0x87aea6,
    )
    for key, val in related.items():
        val1 = str(val)[1:-1]
        embed.add_field(name=key, value=val1)
        
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=animeTitle.results[0].image_url)
    await ctx.send(embed=embed)


bot.run("OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ")
