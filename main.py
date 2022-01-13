import discord
from discord.ext import commands
import asyncio
import random
import youtube_dl

bot = commands.Bot(command_prefix="!")

def isOwner(context):
    return context.message.author.id == 213078092162400257

@bot.event
async def on_ready():
    print("Ready !")

@bot.command()
async def coucou(context):
    await context.send("Coucou !")

@bot.command()
async def bonjour(context):
    server = context.guild
    server_name = server.name
    await context.send(f"Salut jeune *padawan*, tu te trouve sur le serveur {server_name} qui est un serveur génial, la preuve, **JE** suis dedans !")

@bot.command()
async def say(context, *text):
    await context.send(" ".join(text))

@bot.command()
async def repeat(context, number, *text):
    number_remaining = int(number)
    while number_remaining > 0:
        await context.send(" ".join(text))
        number_remaining -= 1

@bot.command()
async def getinfo(context, text, *reste):
    server = context.guild
    member_count = server.member_count
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    number_of_channels = text_channels + voice_channels
    server_name = server.name
    reste_true = len(reste)
    if reste_true == 0:
        if text == "MemberCount":
            await context.send(f"Ce serveur à actuellement {member_count} membres")
        elif text == "NumberOfChannels":
            await context.send(f"Ce serveur possède {number_of_channels} channels")
        elif text == "Name":
            await context.send(f"Ce serveur s'appelle {server_name}")
        else:
            await context.send("Etrange... je ne trouve pas cela")
    else:
        await context.send("Vérifie ton message il y a peut-être quelque chose en trop")

@bot.command()
@commands.has_permissions(administrator=True)
async def clearall(context):
    messages = await context.channel.history().flatten()
    for message in messages:
        await message.delete()

@bot.command()
@commands.check(isOwner)
async def roulette(context):
    await context.send("La roulette Russe commencera dans 10 seconde dites 'moi' pour y participer!")

    player_say = []
    def checkMessage(message):
        return message.content == "moi" and message.channel == context.message.channel and message.author not in player_say

    try:
         while True:
             participation = await bot.wait_for("message", timeout=10, check=checkMessage)
             player_say.append(participation.author)
             await context.send(f"Nouveau participant : **{participation.author.name}**, le tirage commence dans 10 seconde !")
    except:
        gagner = ["Mute", "Ban", "Kick", "gage"]
        gage_list = ["logobi", ]
        await context.send("Début du tirage dans 3...")
        await asyncio.sleep(1)
        await context.send("2")
        await asyncio.sleep(1)
        await context.send("1")
        await asyncio.sleep(1)
        loser_say = random.choice(player_say)
        price = random.choice(gagner)
        if price == "Mute":
            await context.send(f"Et c'est **{loser_say}** qui ce prend un mute pour 2 minutes ! Ce sera effectif dans 5 secondes !")
            await asyncio.sleep(5)
            await loser_say.edit(mute=True)
            await asyncio.sleep(120)
            await loser_say.edit(mute=False)
        elif price == "Kick":
            await context.send(f"Et c'est **{loser_say}** qui se prend un kick dans 5")
            await asyncio.sleep(1)
            await context.send("4")
            await asyncio.sleep(1)
            await context.send("3")
            await asyncio.sleep(1)
            await context.send("2")
            await asyncio.sleep(1)
            await context.send("1")
            await asyncio.sleep(1)
            await context.send("👋")
            await context.guild.kick(loser_say, reason="T'as perdu !")
        elif price == "Ban":
            await context.send(f"Et c'est **{loser_say}** qui se mange un Ban dans 5")
            await asyncio.sleep(1)
            await context.send("4")
            await asyncio.sleep(1)
            await context.send("3")
            await asyncio.sleep(1)
            await context.send("2")
            await asyncio.sleep(1)
            await context.send("1")
            await asyncio.sleep(1)
            await context.send("👋")
            await context.guild.ban(loser_say, reason="T'as joué, t'as perdu !")
        else:
            await context.send(f"C'est {loser_say} qui gagne un gage, décidez le entre-vous !")


@bot.command()
@commands.check(isOwner)
async def rouletteGage(context):
    await context.send("La roulette Russe commencera dans 10 seconde dites 'moi' pour y participer!")

    player = []
    def checkMessage(message):
        return message.content == "moi" and message.channel == context.message.channel and message.author not in player

    try:
         while True:
             participation = await bot.wait_for("message", timeout=10, check=checkMessage)
             player.append(participation.author.name)
             await context.send(f"Nouveau participant : **{participation.author.name}**, le tirage commence dans 10 seconde !")
    except:
        gage_list = ["logobi"]
        await context.send("Début du tirage d'un gage dans 3...")
        await asyncio.sleep(1)
        await context.send("2")
        await asyncio.sleep(1)
        await context.send("1")
        await asyncio.sleep(1)
        loser = random.choice(player)
        price = random.choice(gage_list)
        await context.send(f"Bravo **{loser}** ton gage sera : **{price}** !")


musics = {}
ytdl = youtube_dl.YoutubeDL()


@bot.event
async def on_ready():
    print("Ready")


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)





bot.run("OTI5NDI3NDA1MDU4MjExOTAw.YdnKuQ.yt-dZoz1t9fDJoY-hkYXpEqaeos")