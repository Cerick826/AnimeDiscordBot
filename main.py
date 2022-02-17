import discord
from discord.ext import commands
import mysql.connector


bot = commands.Bot(command_prefix='!', help_command=None)
bot.remove_command('help')
conn = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='root', database='animebot')
cur = conn.cursor()

@bot.event
async def on_ready():
    print('Bot is ready and Online')
    global botON
    botON = True


@bot.event
async def on_message(message):
    global botON
    author_id = str(message.author.id)

    if message.author.bot:
            return
    if (botON):
        if message.content.startswith('!hi'):
            await message.channel.send('hello!')

        if message.content.startswith('!createList'):
            cur.execute(f"select user_id from watchlist where user_id = {author_id}")
            find_id = cur.fetchall()

            if find_id == author_id:
                pass
            else:
                sqladd = "INSERT INTO watchlist (user_id, animelist) VALUES (%s, %s)"
                valadd = (author_id, " ")
                cur.execute(sqladd, valadd)
                conn.commit()


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

@bot.command()
async def help(context):
    #await context.send("help command - this is a test")
    embed = discord.Embed(
        title = '**Help Menu**',
        description = 'Use any of the following commands:',
        color = discord.Color.blue()
    )
    embed.add_field(name='Commands:',value=' `createList`, `showList`, `topAnime`, `recommend`, `.......`')
    embed.add_field(name='Settings:',value='`.......`', inline = False)
    await context.send(embed=embed)
    
bot.run('OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ')