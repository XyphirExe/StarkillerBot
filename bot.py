import discord
from discord.ext import commands

TOKEN = 'NTU2OTMyMjgzMTM1OTUwODQ5.D3A_Uw.pr3hw_8BQFRWvYIMHpUxVgo0nnE'

client = commands.Bot(command_prefix = 'star')

@client.event
async def on_ready():
    print('Je suis prêt.')

client.run(TOKEN)
