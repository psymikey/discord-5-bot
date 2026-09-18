import os
import asyncio
import discord

VOICE_CHANNEL_ID = 1548051069504851970

TOKENS = [
    os.environ.get(f"DISCORD_TOKEN_{i}")
    for i in range(1, 11)
]

clients = []


async def start_bot(token, bot_number):
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = discord.Client(intents=intents)
    clients.append(bot)

    @bot.event
    async def on_ready():
        print(f"✅ Bot {bot_number} online: {bot.user}")

    @bot.event
    async def on_message(message):
        # Only Bot 1 handles the command,
        # so the command isn't executed 10 times.
        if bot_number != 1:
            return

        if message.author.bot:
            return

        if not message.content.startswith("!play "):
            return

        audio_url = message.content[6:].strip()

        if not audio_url:
            await message.channel.send("❌ Audio URL கொடு.")
            return

        print(f"🎵 Playing on 10 bots: {audio_url}")

        for i, client in enumerate(clients):
            try:
                channel = client.get_channel(VOICE_CHANNEL_ID)

                if channel is None:
                    print(f"❌ Bot {i+1}: Voice channel not found")
                    continue

                voice = discord.utils.get(
                    client.voice_clients,
                    guild=channel.guild
                )

                if voice is None:
                    voice = await channel.connect()
                elif not voice.is_connected():
                    await voice.move_to(channel)

                if voice.is_playing():
                    voice.stop()

                source = discord.FFmpegPCMAudio(audio_url)
                voice.play(source)

                print(f"🔊 Bot {i+1}: Playing")

            except Exception as e:
                print(f"❌ Bot {i+1} error: {e}")

    try:
        await bot.start(token)
    except Exception as e:
        print(f"❌ Bot {bot_number} error: {e}")


async def main():
    await asyncio.gather(
        *(start_bot(token, i)
          for i, token in enumerate(TOKENS, start=1)
          if token)
    )


asyncio.run(main())
