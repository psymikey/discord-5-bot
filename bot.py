import os
import asyncio
import discord
from discord import app_commands

TOKENS = [
    os.getenv("BOT_TOKEN_1"),
    os.getenv("BOT_TOKEN_2"),
    os.getenv("BOT_TOKEN_3"),
    os.getenv("BOT_TOKEN_4"),
    os.getenv("BOT_TOKEN_5"),
]

intents = discord.Intents.default()

clients = []
controller = None


class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


async def join_all(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message(
            "❌ First join a voice channel!",
            ephemeral=True
        )
        return

    channel = interaction.user.voice.channel
    await interaction.response.send_message(
        f"🔊 Connecting 5 bots to **{channel.name}**..."
    )

    results = []

    for client in clients:
        try:
            existing = discord.utils.get(
                client.voice_clients,
                guild=interaction.guild
            )

            if existing:
                if existing.channel.id != channel.id:
                    await existing.move_to(channel)
            else:
                await channel.connect()

            results.append(f"✅ {client.user}")

        except Exception as e:
            results.append(f"❌ {client.user}: {e}")

    await interaction.followup.send("\n".join(results))


async def start_bot(token, is_controller=False):
    global controller

    bot = MyBot()
    clients.append(bot)

    if is_controller:
        controller = bot

        @bot.tree.command(
            name="join",
            description="Join my current voice channel with all 5 bots"
        )
        async def join(interaction: discord.Interaction):
            await join_all(interaction)

    await bot.start(token)


async def main():
    valid_tokens = [t for t in TOKENS if t]

    if len(valid_tokens) != 5:
        print("❌ All 5 BOT_TOKEN secrets are required.")
        return

    await asyncio.gather(
        start_bot(valid_tokens[0], True),
        start_bot(valid_tokens[1]),
        start_bot(valid_tokens[2]),
        start_bot(valid_tokens[3]),
        start_bot(valid_tokens[4]),
    )


asyncio.run(main())
