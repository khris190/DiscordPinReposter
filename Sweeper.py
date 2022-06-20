# bot.py
from cgi import print_arguments
from dis import disco
from genericpath import exists
from importlib.metadata import files
import os
from queue import Empty
from ssl import CHANNEL_BINDING_TYPES
import string
from typing import List
import json

import discord
from matplotlib.cbook import print_cycles


class Object(object):
    pass

def readJson(file: string): 
    if exists(file):
        return json.loads(open(file, 'r').read())
    return None

def saveJson(file: string, val):
    open(file,"w").write(json.dumps(val))
     
async def printMessagesInChannel(outChannel, guild):
    print(guild)
    for channel in guild.channels:
        if(isinstance(channel, discord.TextChannel)):
            print('test')
            try:
                pins = await channel.pins()
                print(channel)
                for pin in pins:
                    msg = await createMessage(pin)
                    await outChannel.send(content = msg.content, files = msg.files)
                    deletePin(pin)
            except:
                print('error: ' + channel)

async def createMessage(pin):
    msg = Object()
    msg.content = ''
    if client.settings['visible']['do_show_from']:
        msg.content += "From: " + pin.jump_url + '\n'
    if client.settings['visible']['do_show_credit']:
        msg.content += "Credit: " + pin.author.mention + '\n'
    if client.settings['visible']['do_show_date']:
        msg.content += "Date: " + pin.created_at.strftime("%m/%d/%Y, %H:%M:%S") + '\n'
    msg.content += pin.content
    msg.files = []
    for attachment in pin.attachments:
        msg.files.append(await attachment.to_file())
    return msg

async def deletePin(pin):
    if client.settings['visible']['do_delete_pins']:
        await pin.unpin()

client = discord.Client()
client.settings = readJson('settings.json')
#saveJson('settings.json', client.settings)
TOKEN = client.settings['hidden']['TOKEN']

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    guild = message.guild
    if message.content == '*SetChannel':
        print('setChannel' + message.channel.name)
        client.PinChannel = message.channel
        await client.PinChannel.send("channel set")

    elif message.content == '*SweepAll':
        await printMessagesInChannel(client.PinChannel, guild)

    elif message.content == '*SweepToHere':
        tmpChannel = message.channel
        await printMessagesInChannel(tmpChannel, guild)

    elif message.content == '*help':
         await message.channel.send('*SetChannel \n*SweepToHere \n*SweepAll')


client.run(TOKEN)