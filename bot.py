import discord
from discord.ext import commands

TOKEN = 'NTYyNjE0MzIzMDM0MTkzOTIx.XMb6KA.vb6lNQDyFO9neyu9PMBISqUjrPE'
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Le bot est prêt !')


@client.command()
async def ping(ctx):
    await ctx.send('Pong!')


@client.command()
async def play(ctx, *, audioFileName):
    global vc
    voicechannel = client.get_channel(556530761994338320)
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio(r'D:/JOHAN/École/ISN/atom projet/' + f'{audioFileName}'))
    while vc.is_playing() == 0:
        vc.stop()
        await vc.disconnect()


@client.command()
async def creepy(ctx):
    global vc
    voicechannel = client.get_channel(556530761994338320)
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio(r'D:/JOHAN/École/ISN/atom projet/creepy.mp3'))
    while vc.is_playing() == 0:
        vc.stop()
        await vc.disconnect()


@client.command()
async def gone(ctx, *, playerName):
    global vc
    voicechannel = client.get_channel(556530761994338320)
    vc = await voicechannel.connect()
    await ctx.send(f'**{playerName}**' + ' **IS GONE!**')
    vc.play(discord.FFmpegPCMAudio(r'D:/JOHAN/École/ISN/atom projet/gone.mp3'))
    while vc.is_playing() == 0:
        vc.stop()
        await vc.disconnect()


@client.command()
async def pause(ctx):
    global vc
    await ctx.send("Mis en pause, et oui!")
    vc.pause()


@client.command()
async def resume(ctx):
    global vc
    await ctx.send("Pchhit ! Et c'est reparti !")
    vc.resume()


@client.command()
async def stop(ctx):
    global vc
    await ctx.send("Désolé mon frère, je m'arrête...")
    vc.disconnect()


@client.command()
async def quiz(ctx):
    await ctx.send("**QUIZ: L'HISTOIRE DES JEUX VIDÉOS**\n**Et c'est parti pour le quiz !**")
    score = 0
    await ctx.send("**QUESTION 1:** Quel est le tout premier jeu-vidéo sur écran de l'histoire ?\nA: **Space Invaders**\nB: **Pong**\nC: **OXO**\nD: **Programme de dames de C. Strachey**")
    message = await client.wait_for('message')
    answer = message.content
    if "C" == answer:
        await ctx.send("**En effet**, il s'agit d'un jeu de morpion sorti en 1952.")
        score += 1
    else:
        await ctx.send('**Et non**, le tout premier jeu sur écran est OXO, un jeu de morpion sorti en 1952.')
    await ctx.send("\n**QUESTION 2:** Quelle est la toute première réelle console de l'histoire ?\nA: **Magnavox Odyssey**\nB: **Color TV-Game 6**\nC: **Ping-O-Tronic**\nD: **VideoSport MK2**")
    message = await client.wait_for('message')
    answer = message.content
    if "A" == answer:
        await ctx.send("Commercialisée en 1972, il s'agit **en effet** de la toute première console.")
        score += 1
    else:
        await ctx.send('**Et non**, la toute première réelle console est la Magnavox Odyssey, sortie en 1972.')
    await ctx.send("**QUESTION 3:** Parmis les entreprises suivantes laquelle a traversée toutes les générations de consoles de jeu ?\nA: **Microsoft**\nB: **Sega**\nC: **Sony**\nD: **Nintendo**")
    message = await client.wait_for('message')
    answer = message.content
    if "D" == answer:
        await ctx.send("**Et oui**, c'est depuis 1977 avec la Color TV-Game 6 jusqu'à aujourd'hui avec la Nintendo Switch que Nintendo a parcouru absolument toutes les générations de consoles de l'histoire.")
        score += 1
    else:
        await ctx.send("**Et non**, seul Nintendo a traversé toutes les générations de consoles, de 1977 à aujourd'hui.")
    await ctx.send("**QUESTION 4:** Quel est le jeu le plus vendu de tous les temps ?\nA: **Minecraft**\nB: **Grand Theft Auto V**\nC: **Wii Sports**\nD: **Tetris**")
    message = await client.wait_for('message')
    answer = message.content
    if "A" == answer:
        await ctx.send("**C'est exact !** Ce jeu s'est écoulé à plus de 176 M de ventes !")
        score += 1
    else:
        await ctx.send("**Malheureusement**, aucun jeu vidéo n'a réussi à détroner Minecraft et ses 176 M de ventes.")
    await ctx.send("**QUESTION 5 FINALE:** Quelle est la console de jeu la plus vendue de tous les temps ?\nA: **PlayStation**\nB: **Game Boy / Game Boy Color**\nC: **PlayStation 2**\nD: **Nintendo DS**")
    message = await client.wait_for('message')
    answer = message.content
    if "C" == answer:
        await ctx.send("**Et oui**, malgré le fait que la Nintendo DS tende à se rapprocher des ventes de la PS2 ( seulement 2 M d'écart ), c'est la console de Sony qui détient le reccord de 157 M de ventes.")
        score += 1
    else:
        await ctx.send("**Non...** C'est la PS2 qui détient le reccord avec 157 M de ventes.")
    await ctx.send('Le quiz est terminé, vous avez un score de ' + f'{score}' + ' point(s) !')

client.run(TOKEN)
