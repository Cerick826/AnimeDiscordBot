import datetime
from pydoc import describe
import discord
import asyncio
import aiohttp
import mysql.connector
from discord import Embed
from click import CommandCollection
from operator import truediv
from discord.ext import commands
from discord_components import *

class EmbedHelp:
    
    def __init__(self: "EmbedHelp") -> None:

        self.embedHelp = discord.Embed(
            title="**Help Menu**", description="", color=discord.Color.blue()
        )        

    async def embedCreateList(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(
            name="Command: createList",
            value="Alias:  `createlist`, `Createlist`, `CreateList`",
        )
        self.embedHelp.add_field(
            name="Details:", value="`Creates a list in the database`", inline=False
        )
        self.embedHelp.add_field(name="Usage:", value="`!createList`", inline=False)
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()


    async def embedSaveList(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(
            name="Command: saveList", value="Alias:  `savelist`, `Savelist`, `SaveList`"
        )
        self.embedHelp.add_field(
            name="Details:", value="`Saves anime to list`", inline=False
        )
        self.embedHelp.add_field(
            name="Usage:", value="`!saveList <anime name>`", inline=False
        )
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()



    async def embedShowList(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(
            name="Command: showList", value="Alias:  `showlist`, `Showlist`, `ShowList`"
        )
        self.embedHelp.add_field(
            name="Details:", value="`Shows your list`", inline=False
        )
        self.embedHelp.add_field(name="Usage:", value="`!showList`", inline=False)
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()


    async def embedDelAnime(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(
            name="Command: delAnime", value="Alias:  `delanime`, `Delanime`, `DelAnime`"
        )
        self.embedHelp.add_field(
            name="Details:", value="`Deletes an anime from list`", inline=False
        )
        self.embedHelp.add_field(
            name="Usage:", value="`!delAnime <anime name>`", inline=False
        )
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()

    async def embedDeleteList(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(
            name="Command: deleteList",
            value="Alias:  `deletelist`, `Deletelist`, `DeleteList`",
        )
        self.embedHelp.add_field(
            name="Details:", value="`Deletes list from database`", inline=False
        )
        self.embedHelp.add_field(name="Usage:", value="`!deleteList`", inline=False)
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()

    async def embedPoll(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(name="Command: poll", value="Alias:  `Poll`")
        self.embedHelp.add_field(
            name="Details:", value="`Creates a poll for users to vote on`", inline=False
        )
        self.embedHelp.add_field(
            name="Usage:", value="`!poll <choice1> <choice2> <question>`", inline=False
        )
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()

    async def embedOverall(self: "EmbedHelp", ctx) -> None:
        self.embedHelp.set_footer(
            text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url
        )
        self.embedHelp.add_field(
            name="Commands:",
            value="> `createList` `saveList`    `showList`     `deleteList` `delAnime`\n > \n" + 
                  "> `allRanking` `mostPopular` `animeSearch`  `relAnime` \n > \n" + 
                  "> `recommend`  `poll`        `animePic`     `setEp`"
                  
        )
        self.embedHelp.add_field(name="View Command Details:", value="> `!help <command>`", inline=False)
        await ctx.send(embed=self.embedHelp)
        self.embedHelp.clear_fields()

