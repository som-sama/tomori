from  dotenv import load_dotenv
import os
import random
import openai 
import discord
import time
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

from personality import personality 

openai.api_key = os.getenv("OPENAI_API_KEY")

# Store the chat history
chat_history = {}

def generate_response(user, query):
    # Convert the identity and behavior into a single string with all the details
    identity_info = ' '.join(personality['identity'] + personality['behavior'])
    
    # Use that identity information as part of the prompt
    prompt = f"I am {personality['name']} ({personality['byline']}). {identity_info}\nQ: {query}\nA:"

    if "who is your bf?" in query.lower() or "who is your boyfriend?" in query.lower():
        return "Som"
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
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


