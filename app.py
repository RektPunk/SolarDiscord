import os
from typing import Optional

import discord
from discord import app_commands
from command.solar import Solar

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = discord.Object(id=1234)  # replace with your guld id


class DiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


intents = discord.Intents.all()
client = DiscordClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.tree.command(name="solar")
@app_commands.describe(
    input_text="question or chat",
)
async def on_solar(
    interaction: discord.Interaction,
    input_text: str,
):
    await Solar().execute(interaction, input_text)


client.run(TOKEN)
