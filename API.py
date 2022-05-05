import datetime
import discord
import mal
import animec

from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)

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
    async with ctx.channel.typing():
        image = mal.AnimeSearch(arg)
        mal_id = image.results[0].mal_id
        anime = mal.Anime(mal_id)
        otherTitle = str(anime.title_synonyms)[1:-1]
        otherTitle = otherTitle.replace('\'', '')
        licensors = str(anime.licensors)[1:-1]
        licensors = licensors.replace('\'', '')
        studios = str(anime.studios)[1:-1]
        studios = studios.replace('\'', '')
        genres = str(anime.genres)[1:-1]
        genres = genres.replace('\'', '')
        themes = str(anime.themes)[1:-1]
        themes = themes.replace('\'', '')
        producers = str(anime.producers)[1:-1]
        producers = producers.replace('\'', '')
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
        for i in range(len(characters)):
            nameList += characters[count].name + "\n"
            roleList += characters[count].role + "\n"
            voiceActorList += characters[count].voice_actor + "\n"
            count += 1
        for i in range(len(staff)):
            staffList += staff[countStaff].name + "\n"
            staffRoleList += staff[countStaff].role + "\n"
            countStaff += 1
        embed = discord.Embed(
            title=image.results[0].title,
            url=anime.url,
            color=0xF2D026,
        )
        embed.add_field(name="***Titles***",
                        value=f"**🇺🇸English title: ** {anime.title_english}\n"
                            f"**🇯🇵Japanese title: ** {anime.title_japanese}\n"
                            f"**➤Synonyms: ** {otherTitle}", inline=True)
        embed.add_field(name="***Statistics***",
                        value=f"**💯Score: ** `{anime.score}`\n"
                            f"**✌️Scored by: ** `{anime.scored_by}` users\n"
                            f"**♚Ranked: ** `{anime.rank}`\n"
                            f"**✨Popularity: ** `{anime.popularity}`\n"
                            f"**🕴️Members: ** `{anime.members}`\n"
                            f"**💖Favorites: ** `{anime.favorites}`\t", inline=True)
        embed.add_field(name="***Information***",
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
                            f"**➤Rating: ** {anime.rating}\t", inline=False)
        embed.add_field(name="Synopsis", value=f"```{synopsis}...```", inline=False)
        embed.add_field(name="***Characters & Voice Actors***", value="List of major characters and their voice actors:", inline=False)
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
                name=f"{i+1}) {titles[i]}",
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
        url= image.results[0].url,
        description=image.results[0].title,
        color=0x5d7faf,
    )
    embed.add_field(name="Japanese title",value=f"{japanese}",inline=False)
    embed.add_field(name="Synopsis",value=image.results[0].synopsis,inline=False)
    embed.add_field(name="Volumes", value=image.results[0].volumes, inline=False)
    embed.add_field(name="Genres",value=f"{genre}",inline=False)
    embed.add_field(name="Themes",value=f"{themes}")
    embed.add_field(name="Type", value=image.results[0].type)
    embed.add_field(name="Score", value=image.results[0].score)
    embed.add_field(name="URL", value=image.results[0].url)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=image.results[0].image_url)
    await ctx.send(embed=embed)


bot.run("OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ")
