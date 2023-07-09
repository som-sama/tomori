from  dotenv import load_dotenv
import os
import random
import openai 
import discord
import time
from discord.ext import commands
import asyncio

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
# host = os.getenv("DB_HOST")
# user = os.getenv("DB_USER")
# password = os.getenv("DB_PASSWORD")
# database = os.getenv("DB_NAME")



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

from personality import personality 

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_history = {}



def generate_response(user, query):

    identity_info = ' '.join(personality['identity'] + personality['behavior'])
    

    prompt = f"I am {personality['name']} ({personality['byline']}). {identity_info}\nQ: {query}\nA:"

    if "hello" in query.lower():
        return " "
    elif "remind" in query.lower():
        return ""
    elif "hm" in query.lower():
        return "You look lonely. I can fix that.."
    elif "what will you do if I vanish someday" in query.lower():
        return "I wont let you go. I will hold you tight and even fight the gods if I have to. I love you."
  
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            ai_response = response.choices[0].text.strip()

            # Save the response in the chat history
            if user not in chat_history:
                chat_history[user] = []
            chat_history[user].append({"role": "assistant", "content": ai_response})
            return ai_response
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded, sleeping for 60 seconds")
            time.sleep(60)



@bot.event
async def on_ready():
    print(f"Tomori is online. Logged in as {bot.user.name} ({bot.user.id})")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@bot.command(name='hello')
async def hello(ctx):
    response = random.choice(responses)
    await ctx.send(response)

@bot.command(name="remind")
async def remind(ctx, duration: int, *, reminder: str):
    await ctx.send(f"Aight babe, I will remind you to '{reminder}' after {duration} seconds.")
    await asyncio.sleep(duration)
    await ctx.send(f"Babe!! Reminder: {ctx.author.mention}, you asked me to remind you to '{reminder}'.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    await bot.process_commands(message)

    # if random.random() < 0.2:
    #     await message.channel.send(random.choice(personality["behavior"]))
    
    # Save the user's message in the chat history
    if str(message.author) not in chat_history:
        chat_history[str(message.author)] = []
    chat_history[str(message.author)].append({"role": "user", "content": message.content})
    
    ai_response = generate_response(str(message.author), message.content)
    await message.channel.send(ai_response)

bot.run(bot_token)


