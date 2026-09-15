import os
import discord

VOICE_CHANNEL_ID = 1546934294004633621

intents = discord.Intents.default()
intents.voice_states = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Online: {bot.user}")

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel is None:
        print("❌ Voice channel not found")
        return

    if not bot.voice_clients:
        await channel.connect()
        print("🔊 Voice joined!")
    else:
        print("🔊 Already in voice")

bot.run(os.environ["DISCORD_TOKEN"])
