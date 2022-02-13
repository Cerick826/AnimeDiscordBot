import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global botON
    botON = True


@client.event
async def on_message(message):
    global botON

    if message.author == client.user:
            return
    if (botON):
        if message.content.startswith('!hi'):
            await message.channel.send('hello!')
        
        if message.content.startswith('!leave'):
            await message.channel.send('I am leaving!')
            await client.change_presence(status=discord.Status.invisible)
             
            botON = False

    if not(botON):
        if(message.content.startswith('!join')):
            await message.channel.send('I am back!')
            await client.change_presence(status=discord.Status.online)
            botON = True

    
    
    
        
        

        


    

    

client.run('OTQyMjgwNzE5NjU1Mzk1MzY5.YgiNTg.e1knou32SWUBoL7iY4p6PcKHETQ')