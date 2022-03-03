import discord
from discord import Embed
from discord.ext import commands
from discord_components import *
from operator import truediv
import mysql.connector

bot = commands.Bot(command_prefix='!', help_command=None)
bot.remove_command('help')
conn = mysql.connector.connect(host='sql3.freesqldatabase.com', port=3306, user='sql3474170', passwd='jmkGZaymNS', database='sql3474170')
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

    if not(botON):
        if(message.content.startswith('!join')):
            await message.channel.send('I am back!')
            await bot.change_presence(status=discord.Status.online)
            botON = True
    await bot.process_commands(message)
    
# COMMANDS
@bot.command(name = "menu", aliases=["Menu"])
async def menu(ctx):
    await ctx.send("Menu", components = [
        [Button(label="Help", style="2", emoji = "0️⃣", custom_id="button0"), 
         Button(label="Create List", style="2", emoji = "1️⃣", custom_id="button1"),
         Button(label="Save List", style="2", emoji = "2️⃣", custom_id="button2"),
         Button(label="Show List", style="2", emoji = "3️⃣", custom_id="button3"),
         Button(label="Delete Anime", style="2", emoji = "4️⃣", custom_id="button4")
        # Button(label="Delete List", style="3", emoji = "5️⃣", custom_id="button5")
        ]
            ])
    interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "button0")
    await interaction.send(content = "Button clicked!", ephemeral=False)
    
@bot.command(name="saveList", aliases=["savelist", "Savelist", "SaveList"], pass_context=True)
async def saveList(ctx, *, arg):
    
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    print(mylist)
    if len(mylist) == 5 or len(mylist) == 6:
        mylist = str(arg)
    else:
        mylist = mylist[2:-3]
        mylist += ", " + str(arg)
    print(mylist)
    cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", (mylist, my_id))
    conn.commit()
    await ctx.send(arg + " saved to list")

async def sortWatchList(wString):
    delim = ", "
    result = delim.join(sorted(wString.split(", ")))
    return result

@bot.command(name="showList", aliases=["showlist", "ShowList", "Showlist"], pass_context=True)
async def showList(ctx):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    if len(result) == 0:
        raise Exception()
    if len(mylist) == 5:
        print(mylist)
        raise Exception()
        await ctx.send("The list is empty!")
    else:                                             
        mylist = mylist[2:-3]
        mylist = await sortWatchList(mylist)
        print(mylist)
        await ctx.send(mylist)

@bot.command(name="delAnime", aliases=["Delanime", "DelAnime", "delanime"], pass_context=True)
async def delAnime(ctx, *, arg):
    
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    if len(mylist) == 5:
        print(mylist)
        await ctx.send("The list is empty!")
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
        await ctx.send(arg + " deleted from anime list!")

@bot.command(name="createList", aliases=["Createlist", "CreateList", "createlist"], pass_context=True)
async def createList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()

    if len(find_id) != 0:
        await ctx.send("You already have a list saved!")
        pass
    else:
        sqladd = "INSERT INTO watchlist (user_id, animelist) VALUES (%s, %s)"
        valadd = (author_id, " ")
        cur.execute(sqladd, valadd)
        await ctx.send("New watch list created!")
        conn.commit()

#Exception Handling

@bot.check
def check_command(ctx):
    return ctx.command.qualified_name

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        if check_command(ctx) == "showList":
            await ctx.send("> You don't have a list saved!" + '\n' +
                            "> Use `!createList` to start a list" + '\n')
    elif isinstance(error, commands.MissingRequiredArgument):
        if check_command(ctx) == "saveList":
            await ctx.send("> Incorrect Usage!" + '\n' +
                            "> Use `!savelist <anime title>` to save an anime to your list" + '\n')
        if check_command(ctx) == "delAnime":
            await ctx.send("> Incorrect Usage!" + '\n' +
                            "> Use `!delanime <anime title>` to delete an anime from your list" + '\n')
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("> Command not found!" + '\n' +
                        "> Use `!help` for list of commands" + '\n' +
                        "> Use `!help <command name>` for specific command details")  
    else:
        raise error


@bot.command(name="clearList", aliases=["Clearlist", "ClearList", "clearlist"], pass_context=True)
async def clearList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    if len(find_id) != 0:
        cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {author_id}")
        result = cur.fetchall()
        mylist = " ".join(map(str, result))
        if len(mylist) == 5:
            await ctx.send("List is empty")
            pass
        else:
            cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", ("", author_id))
            conn.commit()
            await ctx.send("List cleared!")
    else:
        await ctx.send("You don't have any list saved!")

@bot.command(name="deleteList", aliases=["Deletelist", "DeleteList", "deletelist"], pass_context=True)
async def deleteList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    if len(find_id) != 0:
        cur.execute(f"DELETE FROM watchlist where user_id = {author_id}")
        await ctx.send("List deleted!")
    else:
        await ctx.send("You don't have a list baka!")


@bot.command(name="help", aliases=["Help"], pass_context=True)
async def help(ctx, *, arg = None):
    if(arg == "createList" or arg == "createlist" or arg == "Createlist" or arg == "CreateList"):
        # await ctx.send("createList Usage: !createList")
        embedcreateList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embedcreateList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embedcreateList.add_field(name='Command: createList',value='Alias:  `createlist`, `Createlist`, `CreateList`')
        embedcreateList.add_field(name='Details:',value='`Creates a list in the database`', inline = False)
        embedcreateList.add_field(name='Usage:',value='`!createList`', inline = False)
        await ctx.send(embed=embedcreateList)
        return

    elif(arg == "saveList" or arg == "savelist" or arg == "Savelist" or arg == "SaveList"):
        # await ctx.send("saveList Usage: !saveList <anime name>")
        embedsaveList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embedsaveList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embedsaveList.add_field(name='Command: saveList',value='Alias:  `savelist`, `Savelist`, `SaveList`')
        embedsaveList.add_field(name='Details:',value='`Saves anime to list`', inline = False)
        embedsaveList.add_field(name='Usage:',value='`!saveList <anime name>`', inline = False)
        await ctx.send(embed=embedsaveList)
        return

    elif(arg == "showList" or arg == "showlist" or arg == "Showlist" or arg == "ShowList"):
        # await ctx.send("showList Usage: !showList")
        embedshowList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embedshowList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embedshowList.add_field(name='Command: showList',value='Alias:  `showlist`, `Showlist`, `ShowList`')
        embedshowList.add_field(name='Details:',value='`Shows your list`', inline = False)
        embedshowList.add_field(name='Usage:',value='`!showList`', inline = False)
        await ctx.send(embed=embedshowList)
        return

    elif(arg == "delAnime" or arg == "delanime" or arg == "Delanime" or arg == "DelAnime"):
        # await ctx.send("delAnime Usage: !delAnime <anime name>")
        embeddelAnime = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embeddelAnime.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embeddelAnime.add_field(name='Command: delAnime',value='Alias:  `delanime`, `Delanime`, `DelAnime`')
        embeddelAnime.add_field(name='Details:',value='`Deletes an anime from list`', inline = False)
        embeddelAnime.add_field(name='Usage:',value='`!delAnime <anime name>`', inline = False)
        await ctx.send(embed=embeddelAnime)
        return

    elif(arg == "deleteList" or arg == "deletelist" or arg == "Deletelist" or arg == "DeleteList"):
        # await ctx.send("deleteList Usage: !deleteList")
        embeddeleteList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embeddeleteList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embeddeleteList.add_field(name='Command: deleteList',value='Alias:  `deletelist`, `Deletelist`, `DeleteList`')
        embeddeleteList.add_field(name='Details:',value='`Deletes list from database`', inline = False)
        embeddeleteList.add_field(name='Usage:',value='`!deleteList`', inline = False)
        await ctx.send(embed=embeddeleteList)
        return

    embed = discord.Embed(
        title = '**Help Menu**',
        description = 'Use any of the following commands:',
        color = discord.Color.blue()
    )
    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
    embed.add_field(name='Commands:',value=' `createList`, `saveList`, `showList`, `delAnime`, `deleteList`, `recommend`, `clearList`')
    embed.add_field(name='Details:',value='`!help <command>`', inline = False)
    await ctx.send(embed=embed)
    
bot.run('OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ')
    
=======
import discord
from discord import Embed
from discord.ext import commands
from discord_components import *
from operator import truediv
import mysql.connector

bot = commands.Bot(command_prefix='!', help_command=None)
bot.remove_command('help')
conn = mysql.connector.connect(host='sql3.freesqldatabase.com', port=3306, user='sql3474170', passwd='jmkGZaymNS', database='sql3474170')
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

    if not(botON):
        if(message.content.startswith('!join')):
            await message.channel.send('I am back!')
            await bot.change_presence(status=discord.Status.online)
            botON = True
    await bot.process_commands(message)
    
# COMMANDS
@bot.command(name = "menu", aliases=["Menu"])
async def menu(ctx):
    await ctx.send("Menu", components = [
        [Button(label="Help", style="2", emoji = "0️⃣", custom_id="button0"), 
         Button(label="Create List", style="2", emoji = "1️⃣", custom_id="button1"),
         Button(label="Save List", style="2", emoji = "2️⃣", custom_id="button2"),
         Button(label="Show List", style="2", emoji = "3️⃣", custom_id="button3"),
         Button(label="Delete Anime", style="2", emoji = "4️⃣", custom_id="button4")
        # Button(label="Delete List", style="3", emoji = "5️⃣", custom_id="button5")
        ]
            ])
    interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "button0")
    await interaction.send(content = "Button clicked!", ephemeral=False)
    
@bot.command(name="saveList", aliases=["savelist", "Savelist", "SaveList"], pass_context=True)
async def saveList(ctx, *, arg):
    
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    print(mylist)
    if len(mylist) == 5 or len(mylist) == 6:
        mylist = str(arg)
    else:
        mylist = mylist[2:-3]
        mylist += ", " + str(arg)
    print(mylist)
    cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", (mylist, my_id))
    conn.commit()
    await ctx.send(arg + " saved to list")

async def sortWatchList(wString):
    delim = ", "
    result = delim.join(sorted(wString.split(", ")))
    return result

@bot.command(name="showList", aliases=["showlist", "ShowList", "Showlist"], pass_context=True)
async def showList(ctx):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    if len(result) == 0:
        raise Exception()
    if len(mylist) == 5:
        print(mylist)
        raise Exception()
        await ctx.send("The list is empty!")
    else:                                             
        mylist = mylist[2:-3]
        mylist = await sortWatchList(mylist)
        print(mylist)
        await ctx.send(mylist)

@bot.command(name="delAnime", aliases=["Delanime", "DelAnime", "delanime"], pass_context=True)
async def delAnime(ctx, *, arg):
    
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    if len(mylist) == 5:
        print(mylist)
        await ctx.send("The list is empty!")
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
        await ctx.send(arg + " deleted from anime list!")

@bot.command(name="createList", aliases=["Createlist", "CreateList", "createlist"], pass_context=True)
async def createList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()

    if len(find_id) != 0:
        await ctx.send("You already have a list saved!")
        pass
    else:
        sqladd = "INSERT INTO watchlist (user_id, animelist) VALUES (%s, %s)"
        valadd = (author_id, " ")
        cur.execute(sqladd, valadd)
        await ctx.send("New watch list created!")
        conn.commit()

#Exception Handling

@bot.check
def check_command(ctx):
    return ctx.command.qualified_name

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        if check_command(ctx) == "showList":
            await ctx.send("> You don't have a list saved!" + '\n' +
                            "> Use `!createList` to start a list" + '\n')
    elif isinstance(error, commands.MissingRequiredArgument):
        if check_command(ctx) == "saveList":
            await ctx.send("> Incorrect Usage!" + '\n' +
                            "> Use `!savelist <anime title>` to save an anime to your list" + '\n')
        if check_command(ctx) == "delAnime":
            await ctx.send("> Incorrect Usage!" + '\n' +
                            "> Use `!delanime <anime title>` to delete an anime from your list" + '\n')
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("> Command not found!" + '\n' +
                        "> Use `!help` for list of commands" + '\n' +
                        "> Use `!help <command name>` for specific command details")  
    else:
        raise error


@bot.command(name="clearList", aliases=["Clearlist", "ClearList", "clearlist"], pass_context=True)
async def clearList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    if len(find_id) != 0:
        cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {author_id}")
        result = cur.fetchall()
        mylist = " ".join(map(str, result))
        if len(mylist) == 5:
            await ctx.send("List is empty")
            pass
        else:
            cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", ("", author_id))
            conn.commit()
            await ctx.send("List cleared!")
    else:
        await ctx.send("You don't have any list saved!")

@bot.command(name="deleteList", aliases=["Deletelist", "DeleteList", "deletelist"], pass_context=True)
async def deleteList(ctx):
    author_id = str(ctx.message.author.id)
    cur.execute(f"select user_id from watchlist where user_id = {author_id}")
    find_id = cur.fetchall()
    if len(find_id) != 0:
        cur.execute(f"DELETE FROM watchlist where user_id = {author_id}")
        await ctx.send("List deleted!")
    else:
        await ctx.send("You don't have a list baka!")


@bot.command(name="help", aliases=["Help"], pass_context=True)
async def help(ctx, *, arg = None):
    if(arg == "createList" or arg == "createlist" or arg == "Createlist" or arg == "CreateList"):
        # await ctx.send("createList Usage: !createList")
        embedcreateList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embedcreateList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embedcreateList.add_field(name='Command: createList',value='Alias:  `createlist`, `Createlist`, `CreateList`')
        embedcreateList.add_field(name='Details:',value='`Creates a list in the database`', inline = False)
        embedcreateList.add_field(name='Usage:',value='`!createList`', inline = False)
        await ctx.send(embed=embedcreateList)
        return

    elif(arg == "saveList" or arg == "savelist" or arg == "Savelist" or arg == "SaveList"):
        # await ctx.send("saveList Usage: !saveList <anime name>")
        embedsaveList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embedsaveList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embedsaveList.add_field(name='Command: saveList',value='Alias:  `savelist`, `Savelist`, `SaveList`')
        embedsaveList.add_field(name='Details:',value='`Saves anime to list`', inline = False)
        embedsaveList.add_field(name='Usage:',value='`!saveList <anime name>`', inline = False)
        await ctx.send(embed=embedsaveList)
        return

    elif(arg == "showList" or arg == "showlist" or arg == "Showlist" or arg == "ShowList"):
        # await ctx.send("showList Usage: !showList")
        embedshowList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embedshowList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embedshowList.add_field(name='Command: showList',value='Alias:  `showlist`, `Showlist`, `ShowList`')
        embedshowList.add_field(name='Details:',value='`Shows your list`', inline = False)
        embedshowList.add_field(name='Usage:',value='`!showList`', inline = False)
        await ctx.send(embed=embedshowList)
        return

    elif(arg == "delAnime" or arg == "delanime" or arg == "Delanime" or arg == "DelAnime"):
        # await ctx.send("delAnime Usage: !delAnime <anime name>")
        embeddelAnime = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embeddelAnime.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embeddelAnime.add_field(name='Command: delAnime',value='Alias:  `delanime`, `Delanime`, `DelAnime`')
        embeddelAnime.add_field(name='Details:',value='`Deletes an anime from list`', inline = False)
        embeddelAnime.add_field(name='Usage:',value='`!delAnime <anime name>`', inline = False)
        await ctx.send(embed=embeddelAnime)
        return

    elif(arg == "deleteList" or arg == "deletelist" or arg == "Deletelist" or arg == "DeleteList"):
        # await ctx.send("deleteList Usage: !deleteList")
        embeddeleteList = discord.Embed(
        title = '**Help Menu**',
        description = '',
        color = discord.Color.blue()
        )
        embeddeleteList.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
        embeddeleteList.add_field(name='Command: deleteList',value='Alias:  `deletelist`, `Deletelist`, `DeleteList`')
        embeddeleteList.add_field(name='Details:',value='`Deletes list from database`', inline = False)
        embeddeleteList.add_field(name='Usage:',value='`!deleteList`', inline = False)
        await ctx.send(embed=embeddeleteList)
        return

    embed = discord.Embed(
        title = '**Help Menu**',
        description = 'Use any of the following commands:',
        color = discord.Color.blue()
    )
    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
    embed.add_field(name='Commands:',value=' `createList`, `saveList`, `showList`, `delAnime`, `deleteList`, `recommend`, `clearList`')
    embed.add_field(name='Details:',value='`!help <command>`', inline = False)
    await ctx.send(embed=embed)
    
bot.run('OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ')