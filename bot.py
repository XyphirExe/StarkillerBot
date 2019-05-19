import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import typing

TOKEN = ''

client = commands.Bot(command_prefix = '.')
status = ['réfléchir','rien']

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(600)

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@client.command()
async def salut():
    """Il a dit bonjour."""
    await client.say("Salut petit scarabée")

@client.command()
async def wsh():
    await client.say('Wsh la famille ! Bien ou bien ?')

@client.command()
async def ping():
    await client.say('Pong ta mère ! (Ceci est un test.)')

@bot.command()
async def bottles(ctx, amount: typing.Optional[int] = 99, *, liquid="beer"):
    await ctx.send('{} bouteilles de {} dans ta mère! Cheh!'.format(amount, liquid))

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))

class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @property
    def delta(self):
        return self.joined - self.created

class JoinDistanceConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return JoinDistance(member.joined_at, member.created_at)

@bot.command()
async def delta(ctx, *, member: JoinDistanceConverter):
    is_new = member.delta.days < 100
    if is_new:
        await ctx.send("Yo le nouveau!")
    else:
        await ctx.send("Hmmm")

client.run(TOKEN)
