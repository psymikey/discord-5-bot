import os
import asyncio
import discord

VOICE_CHANNEL_ID = 1546934294004633621

TOKENS = [
    os.environ["DISCORD_TOKEN_1"],
    os.environ["DISCORD_TOKEN_2"],
    os.environ["DISCORD_TOKEN_3"],
    os.environ["DISCORD_TOKEN_4"],
    os.environ["DISCORD_TOKEN_5"],
    os.environ["DISCORD_TOKEN_6"],
    os.environ["DISCORD_TOKEN_7"],
    os.environ["DISCORD_TOKEN_8"],
    os.environ["DISCORD_TOKEN_9"],
    os.environ["DISCORD_TOKEN_10"],
]

clients = []

async def start_bot(token):
    intents = discord.Intents.default()
    intents.voice_states = True

    bot = discord.Client(intents=intents)
    clients.append(bot)

    @bot.event
    async def on_ready():
        print(f"✅ Online: {bot.user}")

        channel = bot.get_channel(VOICE_CHANNEL_ID)

        if channel is None:
            print(f"❌ Channel not found: {bot.user}")
            return

        if not bot.voice_clients:
            try:
                await channel.connect()
                print(f"🔊 Voice joined: {bot.user}")
            except Exception as e:
                print(f"❌ Voice error {bot.user}: {e}")

    try:
        await bot.start(token)
    except Exception as e:
        print(f"❌ Bot error: {e}")

async def main():
    await asyncio.gather(*(start_bot(token) for token in TOKENS))

asyncio.run(main())
