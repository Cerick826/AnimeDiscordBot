from ast import alias
import asyncio
from click import pass_context
import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import pafy

from random import choice

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


bot = commands.Bot(command_prefix="!")

status = ["music"]
queue = []
loop = False


@bot.event
async def on_ready():
    change_status.start()
    print("Bot is online!")


@bot.command(name="join", aliases=["Join"])
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()


@bot.command(name="leave", aliases=["Leave"])
async def leave(ctx):
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


@bot.command(name="stop", aliases=["Stop"], pass_context=True)
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()


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
                    user.voice.channel.id == ctx.voice_client.channel.id
                    and user.id not in reacted
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
