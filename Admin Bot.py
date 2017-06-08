import discord
import asyncio
import processControl
from processControl import configureCheck
from processControl import removeCommand
from processControl import retrieveServer
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
        for i in client.servers:
            print(i.id)

        print(client.servers['114691817177481220'])
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!create'):
        components = message.content.split(" ")
        string = ','.join(components)
        if(configureCheck(components)):
            server = retrieveServer(client.servers, message.channel)
            
            await client.send_message(message.channel, '!PINNED %s channel %s' % (components[1], components[2]))
            everyone_perms = discord.PermissionOverwrite(read_messages=False)
            my_perms = discord.PermissionOverwrite(read_messages=True)

            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
            mine = discord.ChannelPermissions(target=message.author, overwrite=my_perms)
            await client.create_channel(server, components[2], everyone, mine) 
        else:
            await client.send_message(message.channel, 'Unknown command')
        
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!PINNED') and str(message.author) == 'Administrator Bot#5712':
        await client.pin_message(message)


client.run('MzIyMzUwMzI1MTYyMDQ5NTM2.DBrhPA.Yaue1LcH8f_Idevh9peUatODqWs')
