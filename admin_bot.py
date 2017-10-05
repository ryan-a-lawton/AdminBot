import discord
import asyncio
import process_control
from process_control import configureCheck
from process_control import removeCommand
from process_control import retrieveServer
from process_control import cleanID
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
            if components[1] == 'voice': components[2] = components[2] + '_voice'
            '''retrieve Server by matching channel id's between bots servers'''
            server = retrieveServer(client.servers, message.channel)

            await client.send_message(message.channel, 'Created a %s channel called %s, owner is %s' % (components[1], components[2], message.author.mention))


            '''Create permisson fields'''
            everyone_perms_text = discord.PermissionOverwrite(read_messages=False, send_messages=False)
            everyone_perms_voice = discord.PermissionOverwrite(connect=False,speak=False)
            master_perms_text = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_roles=True, manage_channels=True)
            master_perms_voice = discord.PermissionOverwrite(connect=True, speak=True, manage_roles=True, manage_channels=True)
            servant_perms_text = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_roles=True)
            servant_perms_voice = discord.PermissionOverwrite(connect=True, speak=True)
			
            role_admin_name = components[2] + "_ADMIN"
			
            await client.create_role(server, name=role_admin_name, connect=True, speak=True, manage_roles=True, manage_channels=True)
            await client.create_role(server, name=components[2], connect=True, speak=True, manage_roles=True, manage_channels=True)
            role_admin = discord.utils.get(server.roles, name=role_admin_name)
            role = discord.utils.get(server.roles, name=components[2])
            await client.add_roles(message.author, role_admin)
			
            '''Assign users with permission fields'''
            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms_text if components[1] == 'text' else everyone_perms_voice)
            master = discord.ChannelPermissions(target=role_admin, overwrite=master_perms_text if components[1] == 'text' else master_perms_voice)
            servant = discord.ChannelPermissions(target=role, overwrite=servant_perms_text if components[1] == 'text' else servant_perms_voice)

            '''Construct Server'''
            await client.create_channel(server, components[2], everyone, master, servant, type=None if components[1] == 'text' else discord.ChannelType.voice)

        else:
            await client.send_message(message.channel, 'Unknown command')

    elif message.content.startswith('!delete'):
        components = message.content.split(" ")
        string = ','.join(components)
        if(configureCheck(components)):
            '''Create server definition'''
            server = retrieveServer(client.servers, message.channel)
            deleted = False

            '''check to see if we are deleting current channel or a specific channel'''
            if(len(components)==1):
                for i in message.author.permissions_in(message.channel):
                    if i[0] == 'manage_roles' and i[1] == True:
                        await client.send_message(message.channel, 'I will delete this channel in 30 seconds %s! type !cancel to abort.' % (message.author.mention))
                        delete.append([message.channel])
                        await asyncio.sleep(20)
                        await client.send_message(message.channel, '10 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, '5 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '4 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '3 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '2 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '1 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        deleted = True
                        for j in delete:
                            if j[0].id == message.channel.id:
                                role_admin_name = message.channel.name + "_ADMIN"
                                await client.delete_role(server, discord.utils.get(server.roles, name=role_admin_name))
                                await client.delete_role(server, discord.utils.get(server.roles, name=message.channel.name))
                                await client.delete_channel(message.channel)
            elif(len(components)==3):
                channel = discord.utils.get(server.channels, name=components[2])
                for i in message.author.permissions_in(channel):
                    if i[0] == 'manage_roles' and i[1] == True:
                        await client.send_message(message.channel, 'I will delete this channel in 30 seconds %s! type !cancel to abort.' % (message.author.mention))
                        delete.append([channel])
                        print(channel.name+'3')
                        await asyncio.sleep(20)
                        await client.send_message(message.channel, '10 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, '5 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '4 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '3 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '2 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, '1 seconds remaining. %s' % (message.author.mention))
                        await asyncio.sleep(1)
                        deleted = True
                        for j in delete:
                            if j[0].id == channel.id:
                                role_admin_name = channel.name + "_ADMIN"
                                await client.delete_role(server, discord.utils.get(server.roles, name=role_admin_name))
                                await client.delete_role(server, discord.utils.get(server.roles, name=channel.name))
                                await client.delete_channel(channel)

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

    elif message.content.startswith('!add'):
        components = message.content.split(" ")
        string = ','.join(components)
        server = retrieveServer(client.servers, message.channel)
        channel_name = components[1]
        comp = components[::-1]
        comp.pop()
        comp.pop()
        comp = comp[::-1]
        for i in message.author.permissions_in(message.channel):
            if i[0] == 'manage_roles' and i[1] == True:
                for j in comp:
                    ID = cleanID(j);
                    roleName = discord.utils.get(server.roles, name=channel_name)
                    await client.add_roles(server.get_member(ID), roleName)
                    


    elif message.content.startswith('!PINNED') and str(message.author) == 'Administrator Bot#5712':
        '''await client.pin_message(message)'''

def run():
    client.run('MzIyMzUwMzI1MTYyMDQ5NTM2.DHfj_Q.XFgvVyTuKrLqOAHlM66no83olWc')
