from click import CommandCollection
import discord
from discord import Embed
from discord.ext import commands
from discord_components import *


class ExceptionHandle:

    def __init__(self: "ExceptionHandle") -> None:

        # Global Embed for error handling format
        self.e_embed = discord.Embed(
            title="**Command Error**", description="", color=discord.Color.red()
        )
        

    async def no_list_error(self: "ExceptionHandle", ctx) -> None:
        self.e_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        self.e_embed.add_field(
            name="You don't have a list created!",
            value="Use `!createList` to start a list",
        )
        await ctx.send(embed=self.e_embed)
        self.e_embed.clear_fields()

    async def empty_list_error(self: "ExceptionHandle", ctx) -> None:
        self.e_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        self.e_embed.add_field(
            name="The list is empty!",
            value="Use `!savelist <anime title>` to save an anime to your list",
        )
        await ctx.send(embed=self.e_embed)
        self.e_embed.clear_fields()

    async def missing_anime_error(self: "ExceptionHandle", ctx) -> None:
        self.e_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        self.e_embed.add_field(
            name="That anime is not in your list!",
            value="Use `!showlist` to view saved animes",
            inline=False,
        )
        await ctx.send(embed=self.e_embed)
        self.e_embed.clear_fields()

    async def existing_list_error(self: "ExceptionHandle", ctx) -> None:
        self.e_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        self.e_embed.add_field(
            name="You already have a list!",
            value="Use `!savelist <anime title>` to start a list",
            inline=False,
        )
        await ctx.send(embed=self.e_embed)
        self.e_embed.clear_fields()
