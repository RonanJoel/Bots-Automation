import discord
from discord.ext import commands
from commands.tasks import setup_tasks
from commands.reminders import setup_reminders
from utils.database import init_db

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} está en línea.")
    await init_db()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando no encontrado.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan argumentos en el comando.")
    else:
        await ctx.send("⚠️ Ha ocurrido un error.")
        raise error

# Configurar comandos
setup_tasks(bot)
setup_reminders(bot)

if __name__ == "__main__":
    bot.run(TOKEN)

