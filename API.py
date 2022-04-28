import discord
import mal
from animec import *
from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)
bot.remove_command("help")


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
        color=0x87aea6,
    )
    for key, val in related.items():
        val1 = str(val)[1:-1]
        embed.add_field(name=key, value=val1)
        
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=animeTitle.results[0].image_url)
    await ctx.send(embed=embed)


bot.run("OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ")
