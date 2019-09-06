#On import les modules et tout le nécessaire
import discord
from discord.ext import commands
import asyncio
from mutagen.mp3 import MP3
from discord import opus

#Token spécifique à notre bot créé sur le Discord Developer Portal

TOKEN = 'NTU2OTMyMjgzMTM1OTUwODQ5.XXLKRg.NrzZhTv6tLDfoKmK8l5rLP30BB4'

#Dénomination du bot par "client" et dénomination de son préfixe par "SK" et "sk"
client = commands.Bot(command_prefix=['SK', 'sk'])

#On déclare que ces variables suivantes sont globales et peuvent être utilisées dans certaines fonctions du code
global setChannels
global vc
global listConnectedChannels
global bienvenue
global channelBienvenue
global channelReady
global alreadyLaunched

#Dans cette version ce variables sont autmatiquements choisies
bienvenue = str('rhinochill')
bienvenue += '.mp3'

channelBienvenue = int(408716218829373460)

channelReady = int(408716218829373460)

'''

#On demande une musique qui sera utilisée comme musique de bienvenue sur un salon vocal précis
bienvenue = str(input('> Sélectionnez une musique en format .mp3 dans le dossier "Music"\nElle sera utilisée comme musique de bienvenue sur un salon vocal précis :\n'))
bienvenue += '.mp3'

#On demande l'ID du salon vocal sur lequel nous voulons que le bot lise la musique de bienvenue
testBienvenue = int(0)
while testBienvenue == 0:
    channelBienvenue = str(input('> Sélectionnez le salon vocal de bienvenue (ID à 18 digits sur votre serveur Discord) :\n'))
    if len(channelBienvenue) == 18 and channelBienvenue.isdigit():
        print("> Salon vocal utilisé : (ID: {})\n".format(channelBienvenue))
        testBienvenue = int(1)
    else:
        print("> Erreur, il faut un ID de salon textuel. (nombre à 18 digits)\n")
        testBienvenue = int(0)

#On demande l'ID d'un salon vocal sur lequel le bot annoncera vocalement qu'il est en ligne et est opérationnel
testReady = int(0)
while testReady == 0:
    channelReady = str(input('> Sélectionnez le salon vocal pour annoncer que le bot est prêt (ID à 18 digits sur votre serveur Discord) :\n'))
    if len(channelReady) == 18 and channelReady.isdigit():
        print("> Salon vocal utilisé : (ID: {})\n".format(channelReady))
        testReady = int(1)
    else:
        print("> Erreur, il faut un ID de salon textuel. (nombre à 18 digits)\n")
        testReady = int(0)
'''

#On déclare les variables et on leur attribue une valeur de base
listConnectedChannels = []
vc = None
ChannelAlpha = str("0")
ChannelBeta = str("0")
setChannels = int(0)
alreadyLaunched = int(0)

#On charge les opus pour les OS différents de Windows
OPUS_LIBRARIES = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libraries=OPUS_LIBRARIES):
    if opus.is_loaded() is False:
        for opus_lib in opus_libraries:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                print("<<!>> Erreur, je n'ai pas pu chargé l'opus {}".format(opus_lib))
                pass

#Cette fonction permet d'éviter que le bot soit vue comme inactif et soit éteint par un serveur hébergeur (il envoie un message toutes les ~28-29minutes dans un salon  textuel précis)
async def loop():
    await client.wait_until_ready()
    channel = client.get_channel(582344339225837579)
    loopTime = 1

    while not client.is_closed():
        await asyncio.sleep(1700)
        print("Looped!")
        await channel.send("Looped!" + str(loopTime))
        loopTime += 1

#Actions qu'effectue le bot un fois opérationnel: il affiche dans la console qu'il est prêt, il affiche aussi son nom et son ID et annonce qu'il est prêt dans le salon vocal demandé auparavant à l'utilisateur du bot
@client.event
async def on_ready():
    global vc
    global channelReady
    print('Bot is ready.')
    print('As : ' + str(client.user.name))
    print('ID : ' + str(client.user.id))
    readyChannel = client.get_channel(int(channelReady))
    if vc is None:
        vc = await readyChannel.connect()
    audiofile = 'my_body_is_ready.mp3'
    vc.play(discord.FFmpegPCMAudio('./Music/' + audiofile))
    sound = MP3(str('./Music/' + audiofile))
    time = int(sound.info.length)
    await asyncio.sleep(int(time) + int(5))
    if vc.is_playing() is False:
        await vc.disconnect()

#Commande permettant de connaitre la latence du bot
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong!\nPfiouu... ça m'a pris {round(client.latency * 1000)} ms à renvoyer la balle!")

#Commande qui demande au bot de répéter un mot ou un ensemble de mots
@client.command()
async def echo(ctx):
    echoText = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with) + len(" "):]
    if echoText == '':
        await ctx.send("Il semblerait que rien n'est sorti de votre clavier! :)")
    else:
        await ctx.send(f"**{echoText}**")

#Commande permettant de définir le statut du bot sur Discord
@client.command()
async def setstatus(ctx, type=str("Nothing"), url=str(""), *, newStatus=str("")):
    if type == str("Playing"):
        newStatus = url + " " + newStatus
        await client.change_presence(activity=discord.Game(name=newStatus))
    elif type == str("Listening"):
        newStatus = url + " " + newStatus
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=newStatus))
    elif type == str("Watching"):
        newStatus = url + " " + newStatus
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=newStatus))
    elif type == str("Streaming"):
        await client.change_presence(activity=discord.Streaming(name=newStatus, url=url))
    else:
        await ctx.send("La commande a été mal utilisée.\nPréciser le type d'activité, l'url du stream si c'en est un et/ou la phrase de status. ")

#Lorsque le statut vocal d'un utilisateur change le bot se connecte à un salon vocal pour lire un fichier audio
@client.event
async def on_voice_state_update(member, before, after):
    global vc
    global bienvenue
    global channelBienvenue
    bienvenueChannel = client.get_channel(int(channelBienvenue))
    if member.id != client.user.id and after.channel is None and before.channel is not None:
        goneFrom = before.channel
        if vc.is_connected() is False:
            vc = await goneFrom.connect()
        if vc.is_playing() is False:
            audioFileName = str('gone.mp3')
            vc.play(discord.FFmpegPCMAudio('./Music/' + audioFileName))
            sound = MP3(str('./Music/' + audioFileName))
            time = int(sound.info.length)
            await asyncio.sleep(time + 5)
            if vc.is_playing() is False:
                await vc.disconnect()
    elif member.id != client.user.id and after.channel == bienvenueChannel:
        if vc.is_connected() is False:
            vc = await bienvenueChannel.connect()
        if vc.is_playing() is False:
            await asyncio.sleep(2)
            vc.play(discord.FFmpegPCMAudio('./Music/' + bienvenue))
            sound = MP3(str('./Music/' + bienvenue))
            time = int(sound.info.length)
            await asyncio.sleep(time + 5)
            if vc.is_playing() is False:
                await vc.disconnect()

#Commande affichant la liste des musiques pouvant être écoutées
@client.command()
async def musiques(ctx):
    musics1 = open("./Music/playlist1.txt", "r")
    if musics1.mode == "r":
        list = musics1.read()
        await ctx.author.send("```" + list + "```")
    musics2 = open("./Music/playlist2.txt", "r")
    if musics2.mode == "r":
        list = musics2.read()
        await ctx.author.send("```" + list + "```")
    await ctx.send("<@{}> je vous ai envoyé un message privé contenant la liste des musiques disponibles!".format(ctx.author.id))

#Commande permettant de jouer de la musique dans le salon vocal de celui l'ayant effectuée
@client.command()
async def play(ctx, *, audioFileName=str("Nothing")):
    global vc
    global musicPlaylist
    author = ctx.author
    if author.voice.channel is None:
        await ctx.send("Vous n'êtes même pas connecté à un salon vocal. >:(")
    else:
        fromchannel = author.voice.channel
        if vc.is_connected() is False:
            vc = await fromchannel.connect()
        audioFileName = "./Music/" + audioFileName + ".mp3"
        try:
            exist = open(audioFileName)
        except:
            await ctx.send("Cette musique n'existe pas dans le répertoir.\nTapez **SKmusiques** pour connaître le répertoire de musique.")
        else:
            if vc.is_playing() is True:
                await ctx.send("Je ne peux gérer qu'une seule musique à la fois pour le moment, désolé! ;(")
            else:
                vc.play(discord.FFmpegPCMAudio(audioFileName))
                sound = MP3(str(audioFileName))
                time = int(sound.info.length)
                await asyncio.sleep(int(time) + int(5))
        if vc.is_playing() is False:
            await vc.disconnect()

#Commande mettant en pause la lecture audio du client vocal du bot
@client.command()
async def pause(ctx):
    global vc
    vc.pause()
    await ctx.send("Paused")

#Commande reprenantla lecture audio du client vocal du bot
@client.command()
async def resume(ctx):
    global vc
    vc.resume()
    await ctx.send("Resumed")

#Commande stoppant la lecture audio du client vocal du bot
@client.command()
async def stop(ctx):
    global vc
    vc.stop()
    await ctx.send("Stopped")

#Commande déconnectant la lecture audio du client vocal du bot
@client.command()
async def disconnect(ctx):
    global vc
    await vc.disconnect()
    await ctx.send("Disconnected")

#Commande qui lance un quiz dans le salon textuel de et pour l'utilisateur Discord ayant effectuée cette commande
@client.command()
async def quiz(ctx):
    global alreadyLaunched
    if alreadyLaunched == int(1):
        pass
    else:
        alreadyLaunched = int(1)
        await ctx.send("**QUIZ: L'HISTOIRE DES JEUX VIDÉO**\n**Et c'est parti pour le quiz !\nLe quiz ne se termine que lorsque toutes les questions auront une réponse.**")
        score = 0
        await ctx.send("**QUESTION 1:** Quel est le tout premier jeu-vidéo sur écran de l'histoire ?\nA: **Space Invaders**\nB: **Pong**\nC: **OXO**\nD: **Programme de dames de C. Strachey**")
        message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
        answer = message.content
        while answer != str('A') and answer != str('B') and answer != str('C') and answer != str('D'):
            await ctx.send('Il faut répondre avec seulement une des lettres!')
            message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
            answer = message.content
        if answer.startswith('C'):
            await ctx.send("**En effet**, il s'agit d'un jeu de morpion sorti en 1952.\n ")
            score += 1
        else:
            await ctx.send('**Et non**, le tout premier jeu sur écran est OXO, un jeu de morpion sorti en 1952.\n ')
        await ctx.send("\n**QUESTION 2:** Quelle est la toute première réelle console de l'histoire ?\nA: **Magnavox Odyssey**\nB: **Color TV-Game 6**\nC: **Ping-O-Tronic**\nD: **VideoSport MK2**")
        message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
        answer = message.content
        while answer != str('A') and answer != str('B') and answer != str('C') and answer != str('D'):
            await ctx.send('Il faut répondre avec seulement une des lettres!')
            message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
            answer = message.content
        if answer.startswith('A'):
            await ctx.send("Commercialisée en 1972, il s'agit **en effet** de la toute première console.")
            score += 1
        else:
            await ctx.send('**Et non**, la toute première réelle console est la Magnavox Odyssey, sortie en 1972.')
        await ctx.send("**QUESTION 3:** Parmis les entreprises suivantes laquelle a traversée toutes les générations de consoles de jeu ?\nA: **Microsoft**\nB: **Sega**\nC: **Sony**\nD: **Nintendo**")
        message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
        answer = message.content
        while answer != str('A') and answer != str('B') and answer != str('C') and answer != str('D'):
            await ctx.send('Il faut répondre avec seulement une des lettres!')
            message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
            answer = message.content
        if answer.startswith('D'):
            await ctx.send("**Et oui**, c'est depuis 1977 avec la Color TV-Game 6 jusqu'à aujourd'hui avec la Nintendo Switch que Nintendo a parcouru absolument toutes les générations de consoles de l'histoire.\n ")
            score += 1
        else:
            await ctx.send("**Et non**, seul Nintendo a traversé toutes les générations de consoles, de 1977 à aujourd'hui.")
        await ctx.send("**QUESTION 4:** Quel est le jeu le plus vendu de tous les temps ?\nA: **Minecraft**\nB: **Grand Theft Auto V**\nC: **Wii Sports**\nD: **Tetris**")
        message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
        answer = message.content
        while answer != str('A') and answer != str('B') and answer != str('C') and answer != str('D'):
            await ctx.send('Il faut répondre avec seulement une des lettres!')
            message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
            answer = message.content
        if answer.startswith('A'):
            await ctx.send("**C'est exact !** Ce jeu s'est écoulé à plus de 176 M de ventes !\n ")
            score += 1
        else:
            await ctx.send("**Malheureusement**, aucun jeu vidéo n'a réussi à détroner Minecraft et ses 176 M de ventes.\n ")
        await ctx.send("**QUESTION 5 FINALE:** Quelle est la console de jeu la plus vendue de tous les temps ?\nA: **PlayStation**\nB: **Game Boy / Game Boy Color**\nC: **PlayStation 2**\nD: **Nintendo DS**")
        message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
        answer = message.content
        while answer != str('A') and answer != str('B') and answer != str('C') and answer != str('D'):
            await ctx.send('Il faut répondre avec seulement une des lettres!')
            message = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1)
            answer = message.content
        if answer.startswith('C'):
            await ctx.send("**Et oui**, malgré le fait que la Nintendo DS tende à se rapprocher des ventes de la PS2 ( seulement 2 M d'écart ), c'est la console de Sony qui détient le reccord de 157 M de ventes.\n ")
            score += 1
        else:
            await ctx.send("**Non...** C'est la PS2 qui détient le reccord avec 157 M de ventes.\n ")
        await ctx.send(f'Le quiz est terminé, vous avez un score de {score} point(s) !\n ')
        alreadyLaunched = int(0)

#Commande rajoutant une ID à la liste "listConnectedChannels"
@client.command()
async def addCChannel(ctx, *, id=str("Rien")):
    global setChannels
    global listConnectedChannels
    if len(id) == 18 and id.isdigit() and str(id) not in listConnectedChannels:
        addChannel = client.get_channel(int(id))
        fromGuild = addChannel.guild
        listConnectedChannels.append(id)
        setChannels = setChannels + int(1)
        await ctx.send("Le salon textuel {} (ID: {}) du serveur {} à été ajouté\nID des salons textuels connectés : ".format(addChannel, id, fromGuild))
        await ctx.send(listConnectedChannels)
    else:
        await ctx.send("Erreur, il faut un ID de salon textuel existant n'étant pas dans la liste d'ID. (nombre à 18 digits)")

#Commande enlevant une ID à la liste "listConnectedChannels"
@client.command()
async def removeCChannel(ctx, *, id=str("Rien")):
    global setChannels
    global listConnectedChannels
    if len(id) == 18 and id.isdigit() and str(id) in listConnectedChannels:
        removeChannel = client.get_channel(int(id))
        fromGuild = removeChannel.guild
        listConnectedChannels.remove(id)
        setChannels = setChannels - int(1)
        await ctx.send("Le salon textuel {} (ID: {}) du serveur {} à été enlevé.\nID des salons textuels connectés : ".format(removeChannel, id, fromGuild))
        await ctx.send(listConnectedChannels)
    else:
        await ctx.send("Erreur, il faut un ID de salon textuel existant dans la liste d'ID. (nombre à 18 digits)")

#Lorsqu'un message d'un salon textuel dont l'ID est présent dans la liste "listConnectedChannels" est envoyé il est renvoyé aux autres salons textuels dont leur ID ets présent dans cette liste
@client.event
async def on_message(message):
    global setChannels
    global listConnectedChannels
    guild = message.guild
    author = message.author
    content = message.content
    channel = message.channel
    print('|| In {} / Channel= {} | < {} >:\n     {}'.format(guild, channel, author, content))
    channelsTest = int(2)
    if setChannels >= channelsTest and message.author != client.user and str(channel.id) in listConnectedChannels:
        for connectedChannel in listConnectedChannels:
            getListChannel = client.get_channel(int(connectedChannel))
            try:
                if getListChannel == channel:
                    continue
                else:
                    await getListChannel.send("{} a dit dans {} / {}: {}".format(author, guild, channel, content))
            except AssertionError:
                print("|<!>| Message de {} non envoyé dans {} / {} :\n       {}".format(guild, channel, author, content))
                continue
        await client.process_commands(message)
    else:
        await client.process_commands(message)

#Lorsqu'un utilisateur supprime un message, ce message est affiché dans la console
@client.event
async def on_message_delete(message):
    author = message.author
    guild = message.guild
    content = message.content
    channel = message.channel
    print("|<!>| Ce message de {} dans {} / {} à été supprimé :\n     {}".format(author, guild, channel, content))
    await client.process_commands(message)


#Permet la répétition de la fonction "loop()"
client.loop.create_task(loop())
#Permet de mettre en ligne le bot avec le "TOKEN"
client.run(TOKEN)
