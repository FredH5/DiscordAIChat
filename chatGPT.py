import os
import discord
from discord import app_commands
import openai
import requests
from datetime import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

openai.api_key = OPENAI_API_KEY

GUILD_ID = os.getenv("GUILD_ID")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

@tree.command(
    name="gpt_usage",
    description="Get current usage",
    guild=discord.Object(id=GUILD_ID),
)
async def gpt_ask(interaction):
    await interaction.response.defer()
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    params = {
        "date": datetime.today().strftime('%Y-%m-%d')
    }
    response = requests.get("https://api.openai.com/v1/usage", headers=headers, params=params)
    answer = response.json()
    await interaction.followup.send(content="What is my current API usage?")
    await interaction.followup.send(content=answer)


@tree.command(
    name="gpt_ask",
    description="Get a response from GPT",
    guild=discord.Object(id=GUILD_ID),
)
async def gpt_ask(interaction, prompt: str):
    await interaction.response.defer()
    response = openai.ChatCompletion.create(
       model=OPENAI_MODEL,
       messages=[
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": prompt},
       ],
       max_tokens=200,
       n=1,
       stop=None,
       temperature=1,
    )

    answer = response['choices'][0]['message']['content'].strip()
    await interaction.followup.send(content=f"{prompt}")
    await interaction.followup.send(content=answer)


@tree.command(
    name="gpt",
    description="Get a response from GPT with context",
    guild=discord.Object(id=GUILD_ID),
)
async def gpt(interaction, prompt: str, x: int=10):
    await interaction.response.defer()
    messages = []
    async for msg in interaction.channel.history(limit=x):
        messages.append(msg)

    conversation_messages = [{"role": "assistant" if (msg.author.bot and msg.type == discord.MessageType.reply) else "user", "content": msg.content} for msg in reversed(messages) if msg.content]

    for msg in conversation_messages:
        print(msg)

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are part of a Discord conversation. Answer what's being asked in the context of the conversation history."},
            *conversation_messages,
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=1,
    )

    answer = response['choices'][0]['message']['content'].strip()
    await interaction.followup.send(content=f"{prompt}")
    await interaction.followup.send(content=answer)


client.run(DISCORD_TOKEN)

