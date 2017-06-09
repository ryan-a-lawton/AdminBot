import discord
import asyncio
import processControl
from processControl import configureCheck
from processControl import removeCommand
from processControl import retrieveServer
client = discord.Client()

delete = []

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
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!create'):
        components = message.content.split(" ")
        string = ','.join(components)
        if(configureCheck(components)):
            '''retrieve Server by matching channel id's between bots servers'''
            server = retrieveServer(client.servers, message.channel)

            await client.send_message(message.channel, 'Created a %s channel called %s, owner is %s' % (components[1], components[2], message.author.mention))


            '''Create permisson fields'''
            everyone_perms_text = discord.PermissionOverwrite(read_messages=False, send_messages=False)
            everyone_perms_voice = discord.PermissionOverwrite(connect=False,speak=False)
            my_perms_text = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_roles=True, manage_channels=True)
            my_perms_voice = discord.PermissionOverwrite(connect=True, speak=True, manage_roles=True, manage_channels=True)

            '''Assign users with permission fields'''
            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms_text if components[1] == 'text' else everyone_perms_voice)
            mine = discord.ChannelPermissions(target=message.author, overwrite=my_perms_text if components[1] == 'text' else my_perms_voice)

            '''Construct Server'''
            await client.create_channel(server, components[2], everyone, mine, type=None if components[1] == 'text' else discord.ChannelType.voice)

        else:
            await client.send_message(message.channel, 'Unknown command')

    elif message.content.startswith('!delete'):
        components = message.content.split(" ")
        string = ','.join(components)
        if(configureCheck(components)):
            server = retrieveServer(client.servers, message.channel)
            deleted = False
            for i in message.author.permissions_in(message.channel):
                if i[0] == 'manage_roles' and i[1] == True:
                    await client.send_message(message.channel, 'We will delete this channel in 30 seconds! type !cancel to abort.')
                    delete.append([message.channel])
                    await asyncio.sleep(30)
                    deleted = True
                    for j in delete:
                        if j[0].id == message.channel.id:
                            await client.delete_channel(message.channel)

            if(deleted):
                try:
                    await client.send_message(message.channel, 'You have successfully aborted the deletion process!')
                except:
                    print()
            else:
                await client.send_message(message.channel, 'You do not have permission to delete this channel')
        else:
            await client.send_message(message.channel, 'No such channel type exists')

    elif message.content.startswith('!cancel'):
        components = message.content.split(" ")
        string = ','.join(components)
        if(configureCheck(components)):
            server = retrieveServer(client.servers, message.channel)
            for i in message.author.permissions_in(message.channel):
                if i[0] == 'manage_roles' and i[1] == True:
                    for j in delete:
                        if j[0].id == message.channel.id:
                            delete.remove(j)


    elif message.content.startswith('!PINNED') and str(message.author) == 'Administrator Bot#5712':
        '''await client.pin_message(message)'''


client.run('MzIyMzUwMzI1MTYyMDQ5NTM2.DBrhPA.Yaue1LcH8f_Idevh9peUatODqWs')
