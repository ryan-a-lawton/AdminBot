import discord
import asyncio
import processControl
from processControl import configureCheck
from processControl import removeCommand

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!create'):
        components = message.content.split(" ")
        string = ','.join(components)
        if(configureCheck(components)):
            print()
        await client.send_message(message.channel, 'Created %s channel %s' % (components[1], components[2]))
        await client.send_message(message.channel, '!PINNED %s channel %s' % (components[1], components[2]))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!PINNED') and str(message.author) == 'Administrator Bot#5712':
        await client.pin_message(message)


client.run('MzIyMzUwMzI1MTYyMDQ5NTM2.DBrhPA.Yaue1LcH8f_Idevh9peUatODqWs')
