import discord
from discord.ext import commands, tasks

#client = discord.Client()

bot = commands.Bot(command_prefix= '!', help_command=None)
bot.remove_command('help')

# @client.event
# async def on_ready():
#    print('We have logged in as {0.user}'.format(client))
#     global botON
#     botON = True


# @client.event
# async def on_message(message):
#     global botON

#     # making sure bot does not respond to itself
#     if message.author == client.user:
#             return

#     if (botON):
#         if message.content.startswith('!hi'):
#             await message.channel.send('hello!')
        
#         if message.content.startswith('!leave'):
#             await message.channel.send('I am leaving!')
#             await client.change_presence(status=discord.Status.invisible)
             
#             botON = False

#     if not(botON):
#         if(message.content.startswith('!join')):
#             await message.channel.send('I am back!')
#             await client.change_presence(status=discord.Status.online)
#             botON = True

#Commands

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