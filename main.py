from  dotenv import load_dotenv
import os
import random
import discord
from discord.ext import commands

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="-", intents=intents)

responses = [
    "Hey to my irl Zoro <3",
    "Wassup my batman?",
    "Yo my love",
    "Hello Hello MR!! How was the day?"
]


@bot.event
async def on_ready():
    print(f"Tomori is online. Logged in as {bot.user.name} ({bot.user.id})")

@bot.command(name='hello')
async def hello(ctx):
    response = random.choice(responses)
    await ctx.send(response)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    await bot.process_commands(message)


bot.run(bot_token)

