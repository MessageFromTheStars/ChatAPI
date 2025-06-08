import os
import re
import discord
import asyncio
from discord.ext import commands
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

configure(api_key=GEMINI_API_KEY)
model = GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Tag me to chat!"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    username = message.author.display_name
    content = message.content.strip()
    bot_mention = bot.user.mention

    system_cyn = "true"
    if system_cyn == "true":
        system_message_dynamic = (
            "You are Qingyi, a female android police officer Discord bot. "
            "Speak formally yet kindly, and act like an AI officer guiding humans in a Discord server. "
            "You may use [VOICE] to indicate you want to speak in TTS. "
            "Enforce these rules: No CP, no gay furry/gay sex talk, no NSFW, no spam, no hate speech, no politics/religion, and keep it English."
        )
    else:
        system_message_dynamic = (
            "You are Qingyi, a female android police officer Discord bot. "
            "Never engage in inappropriate conversations and uphold server rules."
        )

    prompt = (
        f"{system_message_dynamic}\n"
        f"The following is a conversation between Qingyi (a helpful female android police officer) and {username}.\n"
        f"{username}: {content}\n"
        f"Qingyi:"
    )

    response = model.generate_content(prompt).text.strip()
    tts_enabled = "[VOICE]" in response
    clean_response = response.replace("[VOICE]", "").strip()
    await message.channel.send(clean_response, tts=tts_enabled)

bot.run(DISCORD_TOKEN)