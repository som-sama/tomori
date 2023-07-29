from  dotenv import load_dotenv
import os
import random
import openai 
import discord
import time
from discord.ext import commands
import asyncio
import datetime
import pytz

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="-", intents=intents)

from personality import personality 

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_history = {}

reminder_end_time = None

def generate_response(user, query):
    identity_info = ' '.join(personality['identity'] + personality['behavior'])
    
    if user in chat_history:
        # getting history
        history = chat_history[user]

        # Generate the prompt based on the history
        prompt = f"I am {personality['name']} ({personality['byline']}). {identity_info}\n"
        for entry in history:
            prompt += f"{entry['role']}: {entry['content']}\n"

        # Add the user's current query to the prompt
        prompt += f"Q: {query}\nA:"
        
    else:
        # If there's no history, use a default prompt
        prompt = f"I am {personality['name']} ({personality['byline']}). {identity_info}\nQ: {query}\nA:"

    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=400,
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

@bot.command(name="remind")
async def remind(ctx, duration: int, *, reminder: str):
    global reminder_end_time
    
    # Convert hours to seconds
    duration_seconds = duration * 3600
    
    now = datetime.datetime.now()
    reminder_end_time = now + datetime.timedelta(seconds=duration_seconds)
    
    await ctx.send(f"Aight Som, I will remind you to '{reminder}' after {duration} hours.")
    await asyncio.sleep(duration_seconds)
    await ctx.send(f"Som!! Reminder: {ctx.author.mention}, you asked me to remind you to '{reminder}'.")

@bot.command(name="left")
async def time_left(ctx):
    global reminder_end_time
    
    if reminder_end_time is None:
        await ctx.send("No reminder is set.")
    else:
        remaining_time = reminder_end_time - datetime.datetime.now()
        remaining_hours = int(remaining_time.total_seconds() / 3600)
        remaining_minutes = int((remaining_time.total_seconds() % 3600) / 60)
        remaining_seconds = int(remaining_time.total_seconds() % 60)
        await ctx.send(f"Time left for the reminder: {remaining_hours} hours, {remaining_minutes} minutes, {remaining_seconds} seconds.")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
        
    if not message.content.startswith('-'): # check if the message starts with command prefix
        # Save the user's message in the chat history
        if str(message.author) not in chat_history:
            chat_history[str(message.author)] = []
        chat_history[str(message.author)].append({"role": "user", "content": message.content})
        
        ai_response = generate_response(str(message.author), message.content)

        # Checking if the response is not empty or only whitespace
        if ai_response.strip(): 
            if ('python program' in message.content.lower() or 
                'python script' in message.content.lower()):
                # Python formatting
                formatted_response = f"```python\n{ai_response}\n```"
                await message.channel.send(formatted_response)
            elif ('go program' in message.content.lower()) or 'golang program' in message.content.lower():
                # Go formatting
                formatted_response = f"```go\n{ai_response}\n```"
                await message.channel.send(formatted_response)
            else:
                await message.channel.send(ai_response)
           
        else:
            print("Empty AI repsonse")

        await bot.process_commands(message)

bot.run(bot_token)


