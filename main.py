import discord
from discord.ext import commands
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

@bot.command(name="saveList", aliases=["savelist", "Savelist", "SaveList"], pass_context=True)
async def saveList(ctx, *, arg):
    my_id = str(ctx.message.author.id)
    cur.execute(f"SELECT animelist FROM watchlist WHERE user_id = {my_id}")
    result = cur.fetchall()
    mylist = " ".join(map(str, result))
    print(mylist)
    if len(mylist) == 5:
        mylist = str(arg)
    else:
        mylist = mylist[2:-3]
        mylist += ", " + str(arg)
    print(mylist)
    cur.execute("""UPDATE watchlist SET animelist= %s WHERE user_id = %s""", (mylist, my_id))
    conn.commit()
    await ctx.send(arg + " saved to list")

@bot.command(name="showList", aliases=["showlist", "ShowList", "Showlist"], pass_context=True)
async def showList(ctx):
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

@bot.command(name="deleteList", aliases=["Deletelist", "DeleteList", "deletelist"], pass_context=True)
async def deleteList(ctx):
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
            await ctx.send("List deleted!")
    else:
        await ctx.send("You don't have any list saved!")

@bot.command()
async def help(context):
    #await context.send("help command - this is a test")

@bot.command(name="help", aliases=["Help"], pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title = '**Help Menu**',
        description = 'Use any of the following commands:',
        color = discord.Color.blue()
    )
    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url = ctx.author.avatar_url)
    embed.add_field(name='Commands:',value=' `createList`, `saveList`, `showList`, `delAnime`, `deleteList`, `recommend`, `.......`')
    embed.add_field(name='Details:',value='`commandDetails`', inline = False)
    await ctx.send(embed=embed)
    
    
bot.run('OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ')