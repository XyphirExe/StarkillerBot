import discord
from discord.ext import commands
import asyncio
from mutagen.mp3 import MP3
from discord import opus


TOKEN = 'NTU2OTMyMjgzMTM1OTUwODQ5.D3A_Uw.pr3hw_8BQFRWvYIMHpUxVgo0nnE'

client = commands.Bot(command_prefix='star')


global ChannelAlpha
global ChannelBeta
global setChannels
global vc
global listConnectedChannels


listConnectedChannels = []
vc = None
ChannelAlpha = str("0")
ChannelBeta = str("0")
setChannels = int(0)


OPUS_LIBRARIES = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
                  'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libraries=OPUS_LIBRARIES):
    if opus.is_loaded():
        return True
    for opus_lib in opus_libraries:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass


async def stopMusic():
    await client.wait_until_ready()

    while not client.is_closed():
        if vc is None:
            None
        elif vc.is_connected() is True and vc.is_playing() is False:
            vc.stop()
            await vc.disconnect()
        await asyncio.sleep(120)


async def loop():
    await asyncio.sleep(10)
    await client.wait_until_ready()
    channel = client.get_channel(577970026468999178)

    while not client.is_closed():
        await asyncio.sleep(1700)
        loopTime = 1
        print("Looped!")
        await channel.send("Looped!" + str(loopTime))
        loopTime += 1
        await asyncio.sleep(1700)


@client.event
async def on_ready():
    global vc
    print('Bot is ready.')
    print('As : ' + str(client.user.name))
    print('ID : ' + str(client.user.id))
    fromchannel = client.get_channel(408716218829373460)
    if vc is None:
        vc = await fromchannel.connect()
    audiofile = 'my_body_is_ready2.mp3'
    vc.play(discord.FFmpegPCMAudio(audiofile))
    sound = MP3(str(audiofile))
    time = int(sound.info.length)
    await asyncio.sleep(int(time) + int(5))
    await vc.disconnect()


@client.command()
async def ping(ctx):
    await ctx.send("Pong!\nPfiouu..." +
                   f"ça m'a pris {round(client.latency * 1000)} ms" +
                   "à renvoyer la balle!")


@client.command()
async def echo(ctx):
    echoText = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):]
    if echoText == '':
        await ctx.send("Khey t'as rien dis wesh...")
    else:
        await ctx.send(f"**{echoText}**")


@client.command()
async def setstatus(ctx, type, url, *, newStatus=None):
    if type == str("Playing"):
        newStatus = url + " " + newStatus
        await client.change_presence(
            activity=discord.Game(name=newStatus))
    elif type == str("Listening"):
        newStatus = url + " " + newStatus
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name=newStatus))
    elif type == str("Watching"):
        newStatus = url + " " + newStatus
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=newStatus))
    elif type == str("Streaming"):
        await client.change_presence(
            activity=discord.Streaming(name=newStatus, url=url))


@client.event
async def on_voice_state_update(member, before, after):
    await client.wait_until_ready()
    fromchannel = client.get_channel(408716218829373460)
    if member.id != client.user.id:
        if after.channel == fromchannel:
            vc = await fromchannel.connect()
            rhinochill = 'rhinochill.mp3'
            vc.play(discord.FFmpegPCMAudio(rhinochill))
            sound = MP3(str(rhinochill))
            time = int(sound.info.length)
            await asyncio.sleep(time + 5)
            await vc.disconnect()
    else:
        None


@client.command()
async def play(ctx, *, audioFileName):
    global vc
    author = ctx.author
    fromchannel = author.voice.channel
    if vc.is_connected() is False:
        vc = await fromchannel.connect()
    audioFileName = audioFileName + ".mp3"
    vc.play(discord.FFmpegPCMAudio(audioFileName))
    sound = MP3(str(audioFileName))
    time = int(sound.info.length)
    await asyncio.sleep(int(time) + int(5))
    await vc.disconnect()


@client.command()
async def stop(ctx):
    global vc
    await ctx.send("Stopped")
    vc.stop()


@client.command()
async def disconnect(ctx):
    global vc
    await ctx.send("Disconnected")
    await vc.disconnect()


@client.command()
async def addCChannel(ctx, *, id):
    global setChannels
    global listConnectedChannels
    if len(id) == 18 and id.isdigit():
        addChannel = client.get_channel(int(id))
        fromGuild = addChannel.guild
        listConnectedChannels.append(id)
        setChannels = setChannels + int(1)
        await ctx.send("Le salon textuel {} (ID: {}) du serveur {}"
                       .format(addChannel, id, fromGuild) +
                       " à été ajouté! ID des salons textuels connectés:")
        await ctx.send(listConnectedChannels)
    else:
        await ctx.send("Erreur, il faut un ID de salon textuel." +
                       " (nombre à 18 digits)")


@client.command()
async def removeCChannel(ctx, *, id):
    global setChannels
    global listConnectedChannels
    if len(id) == 18 and id.isdigit():
        removeChannel = client.get_channel(int(id))
        fromGuild = removeChannel.guild
        listConnectedChannels.remove(id)
        setChannels = setChannels - int(1)
        await ctx.send("Le salon textuel {} (ID: {}) du serveur {}"
                       .format(removeChannel, id, fromGuild) +
                       " à été enlevé. ID des salons textuels connectés:")
        await ctx.send(listConnectedChannels)
    else:
        await ctx.send("Erreur, il faut un ID de salon textuel." +
                       " (nombre à 18 digits)")


@client.event
async def on_message(message):
    global setChannels
    global listConnectedChannels
    channelsTest = int(2)
    if setChannels >= channelsTest:
        guild = message.guild
        author = message.author
        content = message.content
        channel = message.channel
        if message.author != client.user \
           and str(channel.id) in listConnectedChannels:
            print('|| In {} / Channel= {} | < {} >: {}'.format(
                  guild, channel, author, content))
            if str(channel.id) in listConnectedChannels:
                for connectedChannel in listConnectedChannels:
                    getListChannel = client.get_channel(int(connectedChannel))
                    try:
                        if getListChannel == channel:
                            continue
                        else:
                            await getListChannel.send(
                                "{} a dit dans {}/{}: {}".format(
                                    author, guild, channel, content))
                    except AssertionError:
                        continue
                await client.process_commands(message)
        await client.process_commands(message)
    else:
        await client.process_commands(message)


@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await channel.send(
        "``` {} a dit: {} ... Il n'a pas assumé. ```".format(author, content))
    await client.process_commands(message)


client.loop.create_task(stopMusic())
client.loop.create_task(loop())
client.run(TOKEN)
