import os
import discord
from discord.ext import commands
import openai

# Load your Discord bot token and OpenAI API key from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Set up the Discord bot client
bot = commands.Bot(command_prefix="/")

# Define the /gpt command
@bot.command()
async def gpt(ctx, *, prompt: str):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    await ctx.send(answer)

# Define the /gpt_context command
@bot.command()
async def gpt_context(ctx, x: int, *, prompt: str):
    messages = await ctx.channel.history(limit=x).flatten()
    conversation = " ".join(msg.content for msg in messages[-x:])
    prompt_with_context = f"{conversation}\n{prompt}"

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt_with_context,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    await ctx.send(answer)

# Start the bot
bot.run(DISCORD_TOKEN)
