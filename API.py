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
# global exception handling embed
e_embed = discord.Embed(
    title="**Command Error**", description="", color=discord.Color.red()
)

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

@bot.check
def check_command(ctx):
    return ctx.command.qualified_name


@bot.event
async def on_command_error(ctx, error):
    e_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if isinstance(error, commands.MissingRequiredArgument):
        if check_command(ctx) == "saveList":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!savelist <anime title>` to save an anime to your list",
            )
        if check_command(ctx) == "delAnime":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!delanime <anime title>` to delete an anime from your list",
            )
        if check_command(ctx) == "poll":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!poll <anime 1> <anime 2> <question>` to create a poll between two animes",
            )
        if check_command(ctx) == "setEp":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!setEp <anime from list> <episode number>`",
            )
        if check_command(ctx) == "animeSearch":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!animesearch <anime title>`",
            )
        if check_command(ctx) == "relAnime":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!relanime <anime title>`",
            )
    elif isinstance(error, commands.CommandNotFound):
        e_embed.add_field(
            name="Command not found!",
            value="Use `!help` for list of commands\n"
            + "Use `!help <command name>` for specific command details",
        )
    else:
        raise error

    await ctx.send(embed=e_embed)
    e_embed.clear_fields()



bot.run("OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ")
