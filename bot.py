import os
import asyncio
import discord
from discord import app_commands
import yt_dlp

VOICE_CHANNEL_ID = 1546934294004633621

TOKENS = [
    os.getenv("DISCORD_TOKEN_1"),
    os.getenv("DISCORD_TOKEN_2"),
    os.getenv("DISCORD_TOKEN_3"),
    os.getenv("DISCORD_TOKEN_4"),
    os.getenv("DISCORD_TOKEN_5"),
    os.getenv("DISCORD_TOKEN_6"),
    os.getenv("DISCORD_TOKEN_7"),
    os.getenv("DISCORD_TOKEN_8"),
    os.getenv("DISCORD_TOKEN_9"),
    os.getenv("DISCORD_TOKEN_10"),
]

intents = discord.Intents.default()
intents.voice_states = True

clients = []


async def play_on_bot(bot, url):
    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel is None:
        print(f"{bot.user}: Voice channel not found")
        return

    voice = discord.utils.get(bot.voice_clients, guild=channel.guild)

    if voice is None:
        voice = await channel.connect()
    elif voice.channel != channel:
        await voice.move_to(channel)

    if voice.is_playing():
        voice.stop()

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info["url"]

    source = discord.FFmpegPCMAudio(
        audio_url,
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        options="-vn"
    )

    voice.play(source)

    print(f"▶️ {bot.user} playing")


async def start_bot(token, index):
    bot = discord.Client(intents=intents)
    tree = app_commands.CommandTree(bot)
    clients.append(bot)

    @bot.event
    async def on_ready():
        print(f"✅ Bot {index} online: {bot.user}")

        # Slash command only on Bot 1
        if index == 1:
            await tree.sync()
            print("✅ /play synced")

    if index == 1:
        @tree.command(name="play", description="Play music on all 10 bots")
        @app_commands.describe(url="YouTube URL or supported audio URL")
        async def play(interaction: discord.Interaction, url: str):

            await interaction.response.send_message(
                "▶️ 10 bots music start panranga..."
            )

            # Start all 10 bots together
            await asyncio.gather(
                *(play_on_bot(client, url) for client in clients)
            )

    await bot.start(token)


async def main():
    await asyncio.gather(
        *(start_bot(token, i + 1)
          for i, token in enumerate(TOKENS)
          if token)
    )


asyncio.run(main())
