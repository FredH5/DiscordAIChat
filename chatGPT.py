import os
import discord
from discord import app_commands
import openai

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

GUILD_ID = os.getenv("GUILD_ID")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

@tree.command(
    name="gpt_ask",
    description="Get a response from GPT",
    guild=discord.Object(id=GUILD_ID),
)
async def gpt_ask(interaction, prompt: str):
    await interaction.response.defer()
    response = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       messages=[
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": prompt},
       ],
       max_tokens=200,
       n=1,
       stop=None,
       temperature=0.5,
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

    conversation_messages = [{"role": "assistant" if msg.author.bot else "user", "content": f"{msg.author.name}: {str(msg.content)}"} for msg in messages if msg.content]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are part of a Discord conversation. Each message will be sent to you with the name of the person that typed the message. You should absolutely not write GPT: at the beggining of your response. If your response starts by GPT:, you should remove it."},
            *conversation_messages,
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response['choices'][0]['message']['content'].strip()
    await interaction.followup.send(content=f"{prompt}")
    await interaction.followup.send(content=answer)


client.run(DISCORD_TOKEN)

