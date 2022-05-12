import datetime
import discord
import asyncio
import aiohttp
import mysql.connector
from discord import Embed
from operator import truediv
from discord_components import *
from discord.ext import commands, tasks
from click import CommandCollection
from utils import sortWatchList, sortWatchListEp, check_format, check_ep_format
from exceptions import ExceptionHandle
from embedhelp import EmbedHelp
import random
from random import choice
import mal
import animec
from discord.voice_client import VoiceClient
import youtube_dl
import pafy
from ast import alias
from click import pass_context


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

# global EmbedHelp object
embed_help = EmbedHelp()
# global ExceptionHandle object
error_obj = ExceptionHandle()
# Global Embed for error handling format
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


# COMMANDS


@bot.command(
    name="saveList", aliases=["savelist", "Savelist", "SaveList"], pass_context=True
)
async def saveList(ctx, *, arg):
    endspace = arg.rfind(" ")
    episode = arg[endspace + 1 :]
    animename = arg[0:endspace]

    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))

    cur.execute(f"SELECT ep FROM watchlist WHERE user_id = {my_id}")
    epresult = cur.fetchall()
    myeplist = " ".join(map(str, epresult))

    embed = discord.Embed(color=0x14EBC0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    # if user is present in database...enters if block to save to database
    if len(result) != 0:
        if not (episode.isnumeric()):
            if await check_format(mylist):
                mylist = str(arg)
            else:
                mylist = mylist[2:-3]
                mylist += ", " + str(arg)

            counter = 0
            for anime in mylist.split(","):
                if counter == 0:
                    if await check_ep_format(myeplist):
                        myeplist = "0"
                    else:
                        if myeplist[-2:] == ", ":
                            myeplist = myeplist[2:-3]
                            myeplist += "0"
                        else:
                            myeplist = myeplist[2:-3]
                            myeplist += ", 0"
                else:
                    myeplist += ", 0"
                counter += 1

            cur.execute(
                """UPDATE watchlist SET animelist= %s WHERE user_id = %s""",
                (mylist, my_id),
            )
            cur.execute(
                """UPDATE watchlist SET ep= %s WHERE user_id = %s""", (myeplist, my_id)
            )
            conn.commit()
            embed.add_field(
                name="Success!", value=f"{arg} -- saved to list", inline=False
            )
            await ctx.send(embed=embed)
        else:
            if await check_format(mylist):
                mylist = animename
            else:
                mylist = mylist[2:-3]
                mylist += ", " + animename

            if await check_ep_format(myeplist):
                myeplist = episode
            else:
                if myeplist[-2:] == ", ":
                    myeplist = myeplist[2:-3]
                    myeplist += episode
                else:
                    myeplist = myeplist[2:-3]
                    myeplist += ", " + episode

            cur.execute(
                """UPDATE watchlist SET animelist= %s WHERE user_id = %s""",
                (mylist, my_id),
            )
            cur.execute(
                """UPDATE watchlist SET ep= %s WHERE user_id = %s""", (myeplist, my_id)
            )
            conn.commit()
            embed.add_field(
                name="Success!",
                value=f"{animename} -- saved to list with episode {episode}",
                inline=False,
            )
            await ctx.send(embed=embed)
    else:
        await error_obj.no_list_error(ctx)


@bot.command(
    name="showList", aliases=["showlist", "ShowList", "Showlist"], pass_context=True
)
async def showList(ctx):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))

    cur.execute(f"SELECT ep FROM watchlist WHERE user_id = {my_id}")
    epresult = cur.fetchall()
    myeplist = " ".join(map(str, epresult))

    embed = discord.Embed(
        title="Anime list",
        description="My saved animes with episodes: ",
        color=0x14EBC0,
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    # if user is not present in database
    # e_embed is global error embed
    if len(result) == 0:
        await error_obj.no_list_error(ctx)

    elif await check_format(mylist):
        await error_obj.empty_list_error(ctx)

    elif len(mylist) > 5:
        mylist = mylist[2:-3]
        sortedmylist = await sortWatchList(mylist)
        myeplist = await sortWatchListEp(mylist, sortedmylist, myeplist)
        counter = 0
        for anime in sortedmylist.split(","):
            counter1 = 0
            for ep in myeplist.split(","):
                if counter == counter1:
                    embed.add_field(name=f"{anime}", value=f"{ep}", inline=True)
                    break
                counter1 += 1
            counter += 1

        await ctx.send(embed=embed)


@bot.command(
    name="delAnime", aliases=["Delanime", "DelAnime", "delanime"], pass_context=True
)
async def delAnime(ctx, *, arg):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))

    cur.execute(f"SELECT ep FROM watchlist WHERE user_id = {my_id}")
    epresult = cur.fetchall()
    myeplist = " ".join(map(str, epresult))

    embed = discord.Embed(color=0x14EBC0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if len(result) == 0:
        await error_obj.no_list_error(ctx)

    elif await check_format(mylist):
        await error_obj.empty_list_error(ctx)

    elif arg not in mylist:
        await error_obj.missing_anime_error(ctx)

    else:
        myeplist = myeplist[2:-3]
        counter = 0
        for anime in mylist.split(","):
            if anime == (" " + str(arg)):
                break
            if anime == ("('" + str(arg)):
                break
            if anime == (" " + str(arg) + "'"):
                break
            if anime == ("('" + str(arg) + "'"):
                counter = -2
                break
            if anime == ")":
                counter = -1
                break
            counter += 1
        if not counter == -1:
            if counter == -2:
                myeplist = ""
            elif counter == 0:
                first = myeplist.find(",")
                aft = myeplist[first + 2 :]
                myeplist = aft
            else:
                counter2 = 0
                for i in range(0, counter):
                    counter2 = myeplist.find(",", counter2 + 1)

                counter3 = 0
                for i in range(0, counter + 1):
                    counter3 = myeplist.find(",", counter3 + 1)

                end = myeplist.rfind(",")
                if counter2 != end:
                    bef = myeplist[:counter2]
                    aft = myeplist[counter3:]

                    myeplist = bef + ", " + aft

                elif counter2 == end:
                    bef = myeplist[:counter2]
                    myeplist = bef

            myeplist = myeplist.replace(", ,", ",")

            mylist = mylist[2:-3]
            if counter == -2:
                mylist = ""
            elif counter == 0:
                first = mylist.find(",")
                aft = mylist[first + 2 :]
                mylist = aft
            else:
                counter2 = 0
                for i in range(0, counter):
                    counter2 = mylist.find(",", counter2 + 1)

                counter3 = 0
                for i in range(0, counter + 1):
                    counter3 = mylist.find(",", counter3 + 1)

                end = mylist.rfind(",")
                if counter2 != end:
                    bef = mylist[:counter2]
                    aft = mylist[counter3:]

                    mylist = bef + ", " + aft

                elif counter2 == end:
                    bef = mylist[:counter2]
                    mylist = bef

            if mylist[-2:-1] == ",":
                mylist = mylist[:-2]
            if mylist[0:1] == ",":
                mylist = mylist[2:]
            mylist = mylist.replace(", ,", ",")

            cur.execute(
                """UPDATE watchlist SET animelist= %s WHERE user_id = %s""",
                (mylist, my_id),
            )
            cur.execute(
                """UPDATE watchlist SET ep= %s WHERE user_id = %s""", (myeplist, my_id)
            )
            conn.commit()
            embed.add_field(
                name="Success!", value=f"{arg} deleted from anime list!", inline=False
            )
            await ctx.send(embed=embed)
        else:
            await error_obj.missing_anime_error(ctx)


@bot.command(
    name="createList",
    aliases=["Createlist", "CreateList", "createlist"],
    pass_context=True,
)
async def createList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    embed = discord.Embed(color=0x14EBC0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if len(find_id) != 0:
        await error_obj.existing_list_error(ctx)

    else:
        sqladd = "INSERT INTO watchlist (user_id, animelist, ep) VALUES (%s, %s, %s)"
        valadd = (author_id, " ", " ")
        cur.execute(sqladd, valadd)
        embed.add_field(name="Success!", value=f"New watchlist created!", inline=False)
        await ctx.send(embed=embed)
        conn.commit()


@bot.command(
    name="clearList", aliases=["Clearlist", "ClearList", "clearlist"], pass_context=True
)
async def clearList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    embed = discord.Embed(color=0x14EBC0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    find_id = cur.fetchall()
    if len(find_id) != 0:
        cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {author_id}")
        result = cur.fetchall()
        mylist = " ".join(map(str, result))
        if await check_format(mylist):
            await error_obj.empty_list_error(ctx)

        else:
            # Adding reaction double check to confirm user really wanna clearlist
            embed.add_field(
                name="Hmm",
                value=f"This will clear your entire watchlist, you sure?",
                inline=False,
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            check = (
                lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"
            )  # r=reaction, u=user
            # Check if user confirm or not. Cancel if it takes too long
            try:
                reaction, user = await bot.wait_for(
                    "reaction_add", check=check, timeout=30
                )
            except asyncio.TimeoutError:
                await message.edit(content="Interaction timed out!.")
                return
            # if user chooses ✅
            if str(reaction.emoji) == "✅":
                cur.execute(
                    """UPDATE watchlist SET animelist= %s WHERE user_id = %s""",
                    ("", author_id),
                )
                cur.execute(
                    """UPDATE watchlist SET ep= %s WHERE user_id = %s""",
                    ("", author_id),
                )
                conn.commit()
                embed.add_field(
                    name="Success", value=f"Anime list cleared", inline=False
                )
                await ctx.send(embed=embed)
            # if user chooses ❌
            if str(reaction.emoji) == "❌":
                embed.add_field(name="Hmm", value=f"Interaction canceled", inline=False)
                await ctx.send(embed=embed)
    else:
        await error_obj.no_list_error(ctx)


@bot.command(
    name="deleteList",
    aliases=["Deletelist", "DeleteList", "deletelist"],
    pass_context=True,
)
async def deleteList(ctx):
    author_id = str(ctx.message.author.id)
    embed = discord.Embed(color=0x14EBC0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    # Check if user_id is in the database
    # case user_id is found
    if len(find_id) != 0:
        # Adding reaction double check to confirm user really wanna delete the entire list
        embed.add_field(
            name="Hmm",
            value=f"This will delete your entire watchlist from this server, you sure?",
            inline=False,
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        check = (
            lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"
        )  # r=reaction, u=user
        # Check if user confirm or not. Cancel if it takes too long
        try:
            reaction, user = await bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.edit(content="Interaction timed out!.")
            return
        # if user choose ✅
        if str(reaction.emoji) == "✅":
            cur.execute(f"DELETE FROM watchlist where user_id = {author_id}")
            conn.commit()
            embed.add_field(name="Success", value=f"List deleted!", inline=False)
            await ctx.send(embed=embed)
        # if user chooses ❌
        if str(reaction.emoji) == "❌":
            embed.add_field(name="Hmm", value=f"Interaction canceled", inline=False)
            await ctx.send(embed=embed)
    # case user_id not existing in database
    else:
        await error_obj.no_list_error(ctx)


@bot.command(name="help", aliases=["Help"], pass_context=True)
async def help(ctx, *, arg=None):
    if (
        arg == "createList"
        or arg == "createlist"
        or arg == "Createlist"
        or arg == "CreateList"
    ):
        await embed_help.embedCreateList(ctx)
        return

    elif (
        arg == "saveList" or arg == "savelist" or arg == "Savelist" or arg == "SaveList"
    ):
        await embed_help.embedSaveList(ctx)
        return

    elif (
        arg == "showList" or arg == "showlist" or arg == "Showlist" or arg == "ShowList"
    ):
        await embed_help.embedShowList(ctx)
        return

    elif (
        arg == "delAnime" or arg == "delanime" or arg == "Delanime" or arg == "DelAnime"
    ):
        await embed_help.embedDelAnime(ctx)
        return

    elif (
        arg == "deleteList"
        or arg == "deletelist"
        or arg == "Deletelist"
        or arg == "DeleteList"
    ):
        await embed_help.embedDeleteList(ctx)
        return

    elif arg == "poll" or arg == "Poll":

        await embed_help.embedPoll(ctx)
        return

    else:
        await embed_help.embedOverall(ctx)
        return


@bot.command(name="poll", aliases=["Poll"], pass_context=True)
async def poll(ctx, choice1, choice2, *, question):
    embed = discord.Embed(
        title=question,
        description=f":one: {choice1}\n\n:two: {choice2}",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_footer(text=f"Poll by {ctx.author.name}")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await asyncio.sleep(10)

    newmessage = await ctx.fetch_message(message.id)
    firstChoice = await newmessage.reactions[0].users().flatten()
    secondChoice = await newmessage.reactions[1].users().flatten()

    result = "TIE"
    if len(firstChoice) > len(secondChoice):
        result = choice1
    elif len(secondChoice) > len(firstChoice):
        result = choice2

    embed2 = discord.Embed(
        title=question,
        description=f"Vote has concluded:\nResult : {result}",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow(),
    )
    embed2.set_footer(text=f"{choice1} || {choice2} ")
    await newmessage.edit(embed=embed2)


@bot.command(name="animeMeme", aliases=["animememe", "Animememe"], pass_context=True)
async def animeMeme(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cd:
            async with cd.get("https://reddit.com/r/animememes.json") as r:
                meme = await r.json()

                embed = discord.Embed(title="Picture", color=discord.Colour.purple())
                embed.set_image(
                    url=meme["data"]["children"][random.randint(0, 30)]["data"]["url"]
                )

                await ctx.send(embed=embed)


@bot.command(name="setEp", aliases=["setep"], pass_context=True)
async def setEp(ctx, *, arg):
    endspace = arg.rfind(" ")
    episode = arg[endspace + 1 :]
    animename = arg[0:endspace]

    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))

    cur.execute(f"SELECT ep FROM watchlist WHERE user_id = {my_id}")
    epresult = cur.fetchall()
    myeplist = " ".join(map(str, epresult))

    embed = discord.Embed(color=0x14EBC0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if len(result) == 0:
        await error_obj.no_list_error(ctx)

    elif await check_format(mylist):
        await error_obj.empty_list_error(ctx)

    elif animename not in mylist:
        await error_obj.missing_anime_error(ctx)

    else:

        myeplist = myeplist[2:-3]
        counter = 0
        for anime in mylist.split(","):
            if anime == (" " + str(animename)):
                break
            if anime == ("('" + str(animename)):
                break
            if anime == (" " + str(animename) + "'"):
                break
            if anime == ")":
                counter = -1
                break
            counter += 1
        if not counter == -1:
            if counter == 0:
                first = myeplist.find(",")
                aft = myeplist[first:]
                myeplist = str(episode) + aft
            else:
                counter2 = 0
                for i in range(0, counter):
                    counter2 = myeplist.find(",", counter2 + 1)

                counter3 = 0
                for i in range(0, counter + 1):
                    counter3 = myeplist.find(",", counter3 + 1)

                end = myeplist.rfind(",")
                if counter2 != end:
                    bef = myeplist[:counter2]
                    aft = myeplist[counter3:]

                    myeplist = bef + ", " + str(episode) + aft

                elif counter2 == end:
                    bef = myeplist[:counter2]
                    myeplist = bef + ", " + str(episode)

            myeplist = myeplist.replace(", ,", ",")

            cur.execute(
                """UPDATE watchlist SET ep= %s WHERE user_id = %s""", (myeplist, my_id)
            )
            conn.commit()
            embed.add_field(
                name="Success!",
                value=f"{animename} updated to episode {episode}!",
                inline=False,
            )
            await ctx.send(embed=embed)

        else:
            await error_obj.missing_anime_error(ctx)


@bot.command(
    name="allRanking",
    aliases=["AllRanking", "allranking", "Allranking"],
    pass_context=True,
)
async def allRanking(ctx):
    embed = discord.Embed(
        title="Top Anime",
        description="All time ranking for every animes",
        color=0xF2D026,
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(
        url="https://cdn.myanimelist.net/r/50x70/images/anime/1223/96541.webp?s=263cff1b768e29f3cc841792b2dded2e"
    )
    cur.execute(f"SELECT * from allanimerating ORDER BY rank ASC")
    data = cur.fetchall()
    if data is None:
        return
    rankList = ""
    titleList = ""
    ratingList = ""
    # episodesList = ""
    # votesList = ""
    for rank, title, rating, episodes, votes in data:
        rankList += str(rank) + "\n"
        titleList += title[:20] + "\n"
        ratingList += str(rating) + "\n"
        # episodesList += str(episodes) + '\n'
        # votesList += str(votes) + '\n'
    embed.add_field(name="Rank", value=rankList, inline=True)
    embed.add_field(name="Title", value=titleList, inline=True)
    embed.add_field(name="Rating", value=ratingList, inline=True)
    # embed.add_field(name="Episodes", value=episodesList, inline=True)
    # embed.add_field(name="Votes", value=votesList, inline=True)
    embed.set_footer(text="Source: MyAnimeList")
    await ctx.send(embed=embed)


@bot.command(
    name="mostPopular",
    aliases=["MostPopular", "mostpopular", "Mostpopular"],
    pass_context=True,
)
async def mostPopular(ctx):
    embed = discord.Embed(
        title="Top Popularity",
        description="Most voted anime of all time",
        color=0xECA383,
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(
        url="https://cdn.myanimelist.net/r/50x70/images/anime/10/47347.webp?s=6b6f0445f6a93276f3cbd98400582612"
    )
    cur.execute(f"SELECT * from mostpopularanime ORDER BY rank ASC")
    data = cur.fetchall()
    if data is None:
        return
    rankList = ""
    titleList = ""
    # ratingList = ""
    # episodesList = ""
    votesList = ""
    for rank, title, votes, rating, episodes in data:
        rankList += str(rank) + "\n"
        titleList += title[:20] + "\n"
        # ratingList += str(rating) + '\n'
        # episodesList += str(episodes) + '\n'
        votesList += str(votes) + "\n"
    embed.add_field(name="Rank", value=rankList, inline=True)
    embed.add_field(name="Title", value=titleList, inline=True)
    # embed.add_field(name="Rating", value=ratingList, inline=True)
    # embed.add_field(name="Episodes", value=episodesList, inline=True)
    embed.add_field(name="Votes", value=votesList, inline=True)
    embed.set_footer(text="Source: MyAnimeList")
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
        if check_command(ctx) == "animesearch":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!animesearch <anime title>`",
            )
        if check_command(ctx) == "relanime":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!relanime <anime title>`",
            )
        if check_command(ctx) == "mangaSearch":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!mangasearch <anime title>` to view anime details",
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


# API Commands
@bot.command(
    name="animeSearch",
    aliases=["AnimeSearch", "animesearch", "Animesearch"],
    pass_context=True,
)
async def animeSearch(ctx, *, arg):
    async with ctx.channel.typing():
        image = mal.AnimeSearch(arg)
        mal_id = image.results[0].mal_id
        anime = mal.Anime(mal_id)
        otherTitle = str(anime.title_synonyms)[1:-1]
        otherTitle = otherTitle.replace("'", "")
        licensors = str(anime.licensors)[1:-1]
        licensors = licensors.replace("'", "")
        studios = str(anime.studios)[1:-1]
        studios = studios.replace("'", "")
        genres = str(anime.genres)[1:-1]
        genres = genres.replace("'", "")
        themes = str(anime.themes)[1:-1]
        themes = themes.replace("'", "")
        producers = str(anime.producers)[1:-1]
        producers = producers.replace("'", "")
        synopsis = anime.synopsis[:1015]
        background = anime.background
        background = background.split("More Videos")
        characters = anime.characters
        nameList = ""
        roleList = ""
        voiceActorList = ""
        count = 0
        staff = anime.staff
        countStaff = 0
        staffList = ""
        staffRoleList = ""
        order = 1
        for i in range(len(characters)):
            nameList += characters[count].name + "\n"
            roleList += characters[count].role + "\n"
            voiceActorList += characters[count].voice_actor + "\n"
            count += 1
        for i in range(len(staff)):
            staffList += str(order) + ". " + staff[countStaff].name + "\n"
            staffRoleList += str(order) + ". " + staff[countStaff].role + "\n"
            countStaff += 1
            order += 1
        embed = discord.Embed(
            title=image.results[0].title,
            url=anime.url,
            color=0xF2D026,
        )
        embed.add_field(
            name="***Titles***",
            value=f"**🇺🇸English title: ** {anime.title_english}\n"
            f"**🇯🇵Japanese title: ** {anime.title_japanese}\n"
            f"**➤Synonyms: ** {otherTitle}",
            inline=True,
        )
        embed.add_field(
            name="***Statistics***",
            value=f"**💯Score: ** `{anime.score}`\n"
            f"**✌️Scored by: ** `{anime.scored_by}` users\n"
            f"**♚Ranked: ** `{anime.rank}`\n"
            f"**✨Popularity: ** `{anime.popularity}`\n"
            f"**🕴️Members: ** `{anime.members}`\n"
            f"**💖Favorites: ** `{anime.favorites}`\t",
            inline=True,
        )
        embed.add_field(
            name="***Information***",
            value=f"**🎥 Type: ** {anime.type}\t\t"
            f"**🎬 Episodes: ** `{anime.episodes}`\t\t"
            f"**💨Status: ** {anime.status}\n"
            f"**➤Aired: ** {anime.aired}\n"
            f"**📺Premiered: ** {anime.premiered}\n"
            f"**📡Broadcast: ** {anime.broadcast}\n"
            f"**➤Producers: ** {producers}\n"
            f"**👜Licensors: ** {licensors}\n"
            f"**➤Studios: ** {studios}\n"
            f"**➤Source: ** {anime.source}\t\t"
            f"**➤Genres: ** {genres}\t\t"
            f"**🕧Duration: ** {anime.duration}\n"
            f"**➤Themes: ** {themes}\n"
            f"**➤Rating: ** {anime.rating}\t",
            inline=False,
        )
        embed.add_field(name="Synopsis", value=f"```{synopsis}...```", inline=False)
        embed.add_field(
            name="***Characters & Voice Actors***",
            value="List of major characters and their voice actors:",
            inline=False,
        )
        embed.add_field(name="⭐Name⭐", value=f"**{nameList}**", inline=True)
        embed.add_field(name="🗣Role🗣", value=roleList, inline=True)
        embed.add_field(name="🕺Voice Actors💃", value=f"_{voiceActorList}_", inline=True)
        embed.add_field(name="***Staff***", value="List of staff", inline=False)
        embed.add_field(name="👥Staff Name👥", value=f"**{staffList}**", inline=True)
        embed.add_field(name="💭Role💭", value=f"_{staffRoleList}_", inline=True)
        embed.add_field(name="Background", value=f"```{background[0]}```", inline=False)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=image.results[0].image_url)
        embed.set_footer(text="Source: MyAnimeList")
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
        color=0x87AEA6,
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
        if check_command(ctx) == "mangaSearch":
            e_embed.add_field(
                name="Incorrect Usage!",
                value="Use `!mangasearch <anime title>` to view anime details",
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


@bot.command(
    name="animeNews", aliases=["animenews", "Animenews", "AnimeNews"], pass_context=True
)
async def animeNews(ctx, amount: int = 3):
    async with ctx.channel.typing():
        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        description = news.description

        animeNews = discord.Embed(
            title="Latest Anime News",
            color=discord.Colour.purple(),
            timestamp=datetime.datetime.utcnow(),
        )
        animeNews.set_thumbnail(url=news.images[0])

        for i in range(amount):
            animeNews.add_field(
                name=f"{i + 1}) {titles[i]}",
                value=f"{description[i][:200]}...\n[Read More]({links[i]})",
                inline=False,
            )
        await ctx.send(embed=animeNews)


@bot.command(
    name="mangaSearch",
    aliases=["MangaSearch", "mangasearch", "Mangasearch"],
    pass_context=True,
)
async def mangaSearch(ctx, *, arg):
    mangaName = mal.MangaSearch(arg)
    mangaNameID = mangaName.results[0].mal_id
    image = mal.MangaSearch(arg)
    japanese = mal.Manga(mangaNameID).title_japanese
    themes = mal.Manga(mangaNameID).themes
    genre = mal.Manga(mangaNameID).genres

    image = mal.MangaSearch(arg)
    embed = discord.Embed(
        title="Manga Search Result",
        url=image.results[0].url,
        description=image.results[0].title,
        color=0x5D7FAF,
    )
    embed.add_field(name="Japanese title", value=f"{japanese}", inline=False)
    embed.add_field(name="Synopsis", value=image.results[0].synopsis, inline=False)
    embed.add_field(name="Volumes", value=image.results[0].volumes, inline=False)
    embed.add_field(name="Genres", value=f"{genre}", inline=False)
    embed.add_field(name="Themes", value=f"{themes}")
    embed.add_field(name="Type", value=image.results[0].type)
    embed.add_field(name="Score", value=image.results[0].score)
    embed.add_field(name="URL", value=image.results[0].url)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=image.results[0].image_url)
    await ctx.send(embed=embed)


## start of song.py
## ================================================================

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()


status = ["music"]
queue = []
loop = False


@bot.command(name="stop", aliases=["Stop"])
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@bot.command(name="loop", aliases=["Loop"])
async def loop_(ctx):
    global loop

    if loop:
        await ctx.send("Loop mode is now `False!`")
        loop = False

    else:
        await ctx.send("Loop mode is now `True!`")
        loop = True


@bot.command(name="play", aliases=["Play"])
async def play(ctx):
    global queue

    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    elif len(queue) == 0:
        await ctx.send("Nothing in your queue! Use `!queue` to add a song!")

    else:
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        except:
            pass

    server = ctx.message.guild
    voice_channel = server.voice_client
    while queue:
        try:
            while voice_channel.is_playing() or voice_channel.is_paused():
                await asyncio.sleep(2)
                pass

        except AttributeError:
            pass

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(queue[0], loop=bot.loop)
                voice_channel.play(
                    player, after=lambda e: print("Player error: %s" % e) if e else None
                )

                if loop:
                    queue.append(queue[0])

                del queue[0]

            await ctx.send("**Now playing:** {}".format(player.title))

        except:
            break


@bot.command(name="volume", aliases=["Volume"])
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel.")

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")


@bot.command(name="pause", aliases=["Pause"])
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()


@bot.command(name="resume", aliases=["Resume"])
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()


@bot.command(name="queue", aliases=["Queue", "add", "Add"], pass_context=True)
async def queue_(ctx, *, url):
    global queue

    queue.append(url)
    await ctx.send(f"`{url}` added to queue!")


@bot.command(name="remove", aliases=["Remove"], pass_context=True)
async def remove(ctx, number):
    global queue

    try:
        del queue[int(number)]
        await ctx.send(f"Your queue is now `{queue}!`")

    except:
        await ctx.send(
            "Your queue is either **empty** or the index is **out of range**"
        )


@bot.command(name="view", aliases=["View"], pass_context=True)
async def view(ctx):
    await ctx.send(f"Your queue is now `{queue}!`")


@bot.command(name="skip", aliases=["Skip"], pass_context=True)
async def skip(ctx):
    if ctx.voice_client is None:
        return await ctx.send("I am not playing any song.")

    if ctx.author.voice is None:
        return await ctx.send("You are not connected to any voice channel.")

    if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
        return await ctx.send("I am not currently playing any songs for you.")

    poll = discord.Embed(
        title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}",
        description="**80% of the voice channel must vote to skip for it to pass.**",
        colour=discord.Colour.blue(),
    )
    poll.add_field(name="Skip", value=":white_check_mark:")
    poll.add_field(name="Stay", value=":no_entry_sign:")
    poll.set_footer(text="Voting ends in 15 seconds.")

    poll_msg = await ctx.send(embed=poll)
    poll_id = poll_msg.id

    await poll_msg.add_reaction("\u2705")  # yes
    await poll_msg.add_reaction("\U0001F6AB")  # no

    await asyncio.sleep(15)  # 15 seconds to vote

    poll_msg = await ctx.channel.fetch_message(poll_id)

    votes = {"\u2705": 0, "\U0001F6AB": 0}
    reacted = []

    for reaction in poll_msg.reactions:
        if reaction.emoji in ["\u2705", "\U0001F6AB"]:
            async for user in reaction.users():
                if (
                    # user.voice.channel.id == ctx.voice_client.channel.id
                    user.id not in reacted
                    and not user.bot
                ):
                    votes[reaction.emoji] += 1

                    reacted.append(user.id)

    skip = False

    if votes["\u2705"] > 0:
        if (
            votes["\U0001F6AB"] == 0
            or votes["\u2705"] / (votes["\u2705"] + votes["\U0001F6AB"]) > 0.79
        ):  # 80% or higher
            skip = True
            embed = discord.Embed(
                title="Skip Successful",
                description="***Voting to skip the current song was succesful, skipping now.***",
                colour=discord.Colour.green(),
            )

    if not skip:
        embed = discord.Embed(
            title="Skip Failed",
            description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**",
            colour=discord.Colour.red(),
        )

    embed.set_footer(text="Voting has ended.")

    await poll_msg.clear_reactions()
    await poll_msg.edit(embed=embed)

    if skip:
        ctx.voice_client.stop()


@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))


bot.run("OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ")
