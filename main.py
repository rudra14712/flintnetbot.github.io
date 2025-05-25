import discord
from discord.ext import commands
from mcstatus import MinecraftServer
import json
import os

# ---------- CONFIG ----------
MINECRAFT_SERVER_IP = "Flint-net.aternos.me:43278"
DISCORD_BOT_TOKEN = "MTM3NjEzNzM0NzY2MTU2MTg4Nw.GHBed6.vn9Xl6KR-tgOaGEgA2mPaxnROO9-oiYron76r0"
DATA_FILE = "player_data.json"

# ---------- INIT BOT ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- LOAD PLAYER DATA ----------
def load_player_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_player_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

player_data = load_player_data()

# ---------- BOT EVENTS ----------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ---------- STATUS COMMAND ----------
@bot.command()
async def status(ctx):
    try:
        server = MinecraftServer.lookup(f"{MINECRAFT_SERVER_IP}:{MINECRAFT_SERVER_PORT}")
        status = server.status()
        online = status.players.online
        max_players = status.players.max
        motd = status.description

        message = f"🟢 **Server is online**\nPlayers online: **{online}/{max_players}**\nMOTD: `{motd}`\n"

        # Update player stats
        if status.players.sample:
            message += "\n👥 **Online Players:**\n"
            for player in status.players.sample:
                name = player.name
                message += f" - {name}\n"
                if name in player_data:
                    player_data[name] += 1
                else:
                    player_data[name] = 1
            save_player_data(player_data)
        else:
            message += "No players online."

        # Add ranking board
        if player_data:
            sorted_data = sorted(player_data.items(), key=lambda x: x[1], reverse=True)
            message += "\n🏆 **Top Players (Rank Board):**\n"
            for rank, (name, count) in enumerate(sorted_data[:5], start=1):
                message += f" {rank}. {name} — {count} times\n"

        await ctx.send(message)

    except Exception as e:
        await ctx.send("🔴 **Server is offline.**\nNo info available.")

# ---------- RUN BOT ----------
bot.run(DISCORD_BOT_TOKEN)


