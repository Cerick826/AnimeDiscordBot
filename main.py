from click import CommandCollection
import discord
import asyncio
from discord import Embed
from discord.ext import commands
from discord_components import *
from utils import sortWatchList, check_format
from operator import truediv
import mysql.connector
import datetime

bot = commands.Bot(command_prefix='!', help_command=None)
bot.remove_command('help')
conn = mysql.connector.connect(host='sql3.freesqldatabase.com', port=3306, user='sql3474170', passwd='jmkGZaymNS',
                               database='sql3474170')
cur = conn.cursor()


@bot.event
async def on_ready():
    print('Bot is ready and Online')
    global botON
    botON = True


@bot.event
async def on_message(message):
    global botON

    if message.author.bot:
        return
    if (botON):
        if message.content.startswith('!hi'):
            await message.channel.send('hello!')

        if message.content.startswith('!leave'):
            await message.channel.send('I am leaving!')
            await bot.change_presence(status=discord.Status.invisible)

            botON = False

    if not (botON):
        if (message.content.startswith('!join')):
            await message.channel.send('I am back!')
            await bot.change_presence(status=discord.Status.online)
            botON = True
    await bot.process_commands(message)


# COMMANDS
@bot.command(name="menu", aliases=["Menu"])
async def menu(ctx):
    await ctx.send("Menu", components=[
        [Button(label="Help", style="2", emoji="0️⃣", custom_id="button0"),
         Button(label="Create List", style="2", emoji="1️⃣", custom_id="button1"),
         Button(label="Save List", style="2", emoji="2️⃣", custom_id="button2"),
         Button(label="Show List", style="2", emoji="3️⃣", custom_id="button3"),
         Button(label="Delete Anime", style="2", emoji="4️⃣", custom_id="button4")
         # Button(label="Delete List", style="3", emoji = "5️⃣", custom_id="button5")
         ]
    ])
    interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id == "button0")
    await interaction.send(content="Button clicked!", ephemeral=False)


@bot.command(name="saveList", aliases=["savelist", "Savelist", "SaveList"], pass_context=True)
async def saveList(ctx, *, arg):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    embed = discord.Embed(color=0x14ebc0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    print(mylist)
    # if user is present in database...enters if block to save to database
    if len(result) != 0:
        if await check_format(mylist):
            mylist = str(arg)
        else:
            mylist = mylist[2:-3]
            mylist += ", " + str(arg)
        print(mylist)
        cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", (mylist, my_id))
        conn.commit()
        embed.add_field(name="Success!", value=f"{arg} -- saved to list", inline=False)
        await ctx.send(embed=embed)
    else:
        e_embed.add_field(name="You don't have a list created!", value="Use `!createList` to start a list")
        await ctx.send(embed=e_embed)
        e_embed.clear_fields()

    
    


@bot.command(name="showList", aliases=["showlist", "ShowList", "Showlist"], pass_context=True)
async def showList(ctx):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    embed = discord.Embed(title="Anime list", description="My saved animes: ", color=0x14ebc0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    
    # if user is not present in database
    # e_embed is global error embed
    if len(result) == 0:
        e_embed.add_field(name="You don't have a list created!", value="Use `!createList` to create a list")
        await ctx.send(embed=e_embed)
        e_embed.clear_fields()
    elif await check_format(mylist):
        #print(mylist)
        await on_command_error(ctx, commands.CommandInvokeError)
        # embed.add_field(name="Error", value="The list is empty!", inline=False)
        #await ctx.send(embed=embed)
    elif len(mylist) > 5:
        mylist = mylist[2:-3]
        mylist = await sortWatchList(mylist)
        counter = 1
        for anime in mylist.split(","):
            embed.add_field(name=f'{counter}', value=f"{anime}", inline=True)
            counter += 1
        print(mylist)
        await ctx.send(embed=embed)
    
    

@bot.command(name="delAnime", aliases=["Delanime", "DelAnime", "delanime"], pass_context=True)
async def delAnime(ctx, *, arg):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    embed = discord.Embed(color=0x14ebc0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if len(result) == 0:
        e_embed.add_field(name="You don't have a list created!", value="Use `!createList` to start a list")
        await ctx.send(embed=e_embed)
        e_embed.clear_fields()
    elif await check_format(mylist):
        #print(mylist)
        e_embed.add_field(name="Your list is empty!", value="Use `!savelist <anime title>` to start a list", inline=False)
        await ctx.send(embed=e_embed)
        e_embed.clear_fields()
    elif arg not in mylist:
        e_embed.add_field(name="That anime is not in your list!", value="Use `!showlist` to view saved animes", inline=False)
        await ctx.send(embed=e_embed)
        e_embed.clear_fields()
    else:
        mylist = mylist[2:-3]
        print(mylist)
        mylist = mylist.replace(arg, "")
        print(mylist[-2:-2])
        if mylist[-2:-1] == ",":
            mylist = mylist[:-2]
        if mylist[0:1] == ",":
            mylist = mylist[2:]
        mylist = mylist.replace(", ,", ",")
        cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", (mylist, my_id))
        conn.commit()
        embed.add_field(name="Success!", value=f"{arg} deleted from anime list!", inline=False)
        await ctx.send(embed=embed)


@bot.command(name="createList", aliases=["Createlist", "CreateList", "createlist"], pass_context=True)
async def createList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    embed = discord.Embed(color=0x14ebc0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if len(find_id) != 0:
        e_embed.add_field(name="You already have a list!", value="Use `!savelist <anime title>` to start a list", inline=False)
        await ctx.send(embed=e_embed)
        e_embed.clear_fields()
    else:
        sqladd = "INSERT INTO watchlist (user_id, animelist) VALUES (%s, %s)"
        valadd = (author_id, " ")
        cur.execute(sqladd, valadd)
        embed.add_field(name="Success!", value=f"New watchlist created!", inline=False)
        await ctx.send(embed=embed)
        conn.commit()


# Exception Handling

@bot.check
def check_command(ctx):
    return ctx.command.qualified_name

# Global Embed for error handling format
e_embed = discord.Embed(
            title='**Command Error**',
            description='',
            color=discord.Color.red()
        )

@bot.event
async def on_command_error(ctx, error):
    e_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if isinstance(error, commands.CommandInvokeError):
        if check_command(ctx) == "showList":
            e_embed.add_field(name="Your list is empty!", value="Use `!savelist <anime title>` to start a list")
        
    elif isinstance(error, commands.MissingRequiredArgument):
        if check_command(ctx) == "saveList":
            e_embed.add_field(name="Incorrect Usage!", value="Use `!savelist <anime title>` to save an anime to your list")
        if check_command(ctx) == "delAnime":
            e_embed.add_field(name="Incorrect Usage!", value="Use `!delanime <anime title>` to delete an anime from your list")
    elif isinstance(error, commands.CommandNotFound):
        e_embed.add_field(name="Command not found!", value="Use `!help` for list of commands\n" +
                                                            "Use `!help <command name>` for specific command details")
    else:
        raise error

    await ctx.send(embed=e_embed)
    e_embed.clear_fields()

    


@bot.command(name="clearList", aliases=["Clearlist", "ClearList", "clearlist"], pass_context=True)
async def clearList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    embed = discord.Embed(color=0x14ebc0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    find_id = cur.fetchall()
    if len(find_id) != 0:
        cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {author_id}")
        result = cur.fetchall()
        mylist = " ".join(map(str, result))
        if await check_format(mylist):
            embed.add_field(name="Error", value=f"Your list is currently empty", inline=False)
            await ctx.send(embed=embed)
        else:
            #Adding reaction double check to confirm user really wanna clearlist
            embed.add_field(name="Hmm", value=f"This will clear your entire watchlist, you sure?", inline=False)
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user
            # Check if user confirm or not. Cancel if it takes too long
            try:
                reaction, user = await bot.wait_for("reaction_add", check=check, timeout=30)
            except asyncio.TimeoutError:
                await message.edit(content="Interaction timed out!.")
                return
            # if user chooses ✅
            if str(reaction.emoji) == "✅":
                cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", ("", author_id))
                conn.commit()
                embed.add_field(name="Success", value=f"Anime list cleared", inline=False)
                await ctx.send(embed=embed)
            # if user chooses ❌
            if str(reaction.emoji) == "❌":
                embed.add_field(name="Hmm", value=f"Interaction canceled", inline=False)
                await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have any list saved!")


@bot.command(name="deleteList", aliases=["Deletelist", "DeleteList", "deletelist"], pass_context=True)
async def deleteList(ctx):
    author_id = str(ctx.message.author.id)
    embed = discord.Embed(color=0x14ebc0)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    # Check if user_id is in the database
    # case user_id is found
    if len(find_id) != 0:
        # Adding reaction double check to confirm user really wanna delete the entire list
        embed.add_field(name="Hmm", value=f"This will delete your entire watchlist from this server, you sure?", inline=False)
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user
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
        embed.add_field(name="Success", value=f"You don't have a list baka!", inline=False)
        await ctx.send(embed=embed)


@bot.command(name="help", aliases=["Help"], pass_context=True)
async def help(ctx, *, arg=None):
    if (arg == "createList" or arg == "createlist" or arg == "Createlist" or arg == "CreateList"):
        # await ctx.send("createList Usage: !createList")
        embedcreateList = discord.Embed(
            title='**Help Menu**',
            description='',
            color=discord.Color.blue()
        )
        embedcreateList.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        embedcreateList.add_field(name='Command: createList', value='Alias:  `createlist`, `Createlist`, `CreateList`')
        embedcreateList.add_field(name='Details:', value='`Creates a list in the database`', inline=False)
        embedcreateList.add_field(name='Usage:', value='`!createList`', inline=False)
        await ctx.send(embed=embedcreateList)
        return

    elif (arg == "saveList" or arg == "savelist" or arg == "Savelist" or arg == "SaveList"):
        # await ctx.send("saveList Usage: !saveList <anime name>")
        embedsaveList = discord.Embed(
            title='**Help Menu**',
            description='',
            color=discord.Color.blue()
        )
        embedsaveList.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        embedsaveList.add_field(name='Command: saveList', value='Alias:  `savelist`, `Savelist`, `SaveList`')
        embedsaveList.add_field(name='Details:', value='`Saves anime to list`', inline=False)
        embedsaveList.add_field(name='Usage:', value='`!saveList <anime name>`', inline=False)
        await ctx.send(embed=embedsaveList)
        return

    elif (arg == "showList" or arg == "showlist" or arg == "Showlist" or arg == "ShowList"):
        # await ctx.send("showList Usage: !showList")
        embedshowList = discord.Embed(
            title='**Help Menu**',
            description='',
            color=discord.Color.blue()
        )
        embedshowList.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        embedshowList.add_field(name='Command: showList', value='Alias:  `showlist`, `Showlist`, `ShowList`')
        embedshowList.add_field(name='Details:', value='`Shows your list`', inline=False)
        embedshowList.add_field(name='Usage:', value='`!showList`', inline=False)
        await ctx.send(embed=embedshowList)
        return

    elif (arg == "delAnime" or arg == "delanime" or arg == "Delanime" or arg == "DelAnime"):
        # await ctx.send("delAnime Usage: !delAnime <anime name>")
        embeddelAnime = discord.Embed(
            title='**Help Menu**',
            description='',
            color=discord.Color.blue()
        )
        embeddelAnime.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        embeddelAnime.add_field(name='Command: delAnime', value='Alias:  `delanime`, `Delanime`, `DelAnime`')
        embeddelAnime.add_field(name='Details:', value='`Deletes an anime from list`', inline=False)
        embeddelAnime.add_field(name='Usage:', value='`!delAnime <anime name>`', inline=False)
        await ctx.send(embed=embeddelAnime)
        return

    elif (arg == "deleteList" or arg == "deletelist" or arg == "Deletelist" or arg == "DeleteList"):
        # await ctx.send("deleteList Usage: !deleteList")
        embeddeleteList = discord.Embed(
            title='**Help Menu**',
            description='',
            color=discord.Color.blue()
        )
        embeddeleteList.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        embeddeleteList.add_field(name='Command: deleteList', value='Alias:  `deletelist`, `Deletelist`, `DeleteList`')
        embeddeleteList.add_field(name='Details:', value='`Deletes list from database`', inline=False)
        embeddeleteList.add_field(name='Usage:', value='`!deleteList`', inline=False)
        await ctx.send(embed=embeddeleteList)
        return
      
    elif (arg == "poll" or arg == "Poll"):
        embedpoll = discord.Embed(
            title='**Help Menu**',
            description='',
            color=discord.Color.blue()
        )
        embedpoll.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        embedpoll.add_field(name='Command: poll', value='Alias:  `Poll`')
        embedpoll.add_field(name='Details:', value='`Creates a poll for users to vote on`', inline=False)
        embedpoll.add_field(name='Usage:', value='`!poll <choice1> <choice2> <question>`', inline=False)
        await ctx.send(embed=embedpoll)
        return

    embed = discord.Embed(
        title='**Help Menu**',
        description='Use any of the following commands:',
        color=discord.Color.blue()
    )
    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='Commands:',
                    value=' `createList`, `saveList`, `showList`, `delAnime`, `deleteList`, `recommend`, `clearList`')
    embed.add_field(name='Details:', value='`!help <command>`', inline=False)
    await ctx.send(embed=embed)
    
@bot.command(name="poll", aliases=["Poll"], pass_context=True)
async def poll(ctx, choice1, choice2, *, question):
    embed = discord.Embed(
        title=question,
        description=f":one: {choice1}\n\n:two: {choice2}",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
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
        timestamp=datetime.datetime.utcnow()
    )
    embed2.set_footer(text=f"{choice1} || {choice2} ")
    await newmessage.edit(embed=embed2)
    
@bot.command(name="animePic", aliases=["animepic"], pass_context=True)
async def animePic(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://aws.random.cat/meow") as r:
                data = await r.json()

                embed = discord.Embed(title= "Picture")
                embed.set_image(url=data['file'])
                
                await ctx.send(embed=embed)


bot.run('OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ')
