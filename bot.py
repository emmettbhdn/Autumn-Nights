# Import needed libraries:
import discord
from discord.ext import commands
from discord.commands import Option
import keep_alive
from core.helperFunctions import cogHelpers
from core.helperFunctions import dataHelpers
import os
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Variables:
TOKEN = os.getenv("TOKEN")

client = commands.Bot(
    intents=discord.Intents.all()
)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# config

# Starts up the bot and tells me when it's ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
    print("SERVER_IDS constant intialized at " + str(dataHelpers.SERVER_IDS))
    print('Bot is ready!')
    
cogs = client.create_group("cogs", "Commands to load/unload Cogs (Admin Only)", checks=[commands.has_permissions(administrator=True)])

@cogs.command(description="Loads a Cog")
async def load(ctx, cogchoice: Option(str, "Enter the Cog that should get loaded", required=True, default="all")):
    if cogchoice.lower() == "all":
        cogHelpers.loadAllCogs(ctx.bot)
        ctx.respond("Successfully loaded in all Cogs")
    else:
        try:
            client.load_extension("cogs." + cogchoice)
            await ctx.respond("Successfully loaded in Cog " + cogchoice)
        except Exception as e:
            await ctx.respond(f"An error occurred while loading the cog {cogchoice}! Please contact ath404 if you think something is broken and send him this: ```{e}```")
            
@cogs.command(description="Unloads a Cog")
async def unload(ctx, cogchoice: Option(str, "Enter the Cog that should get unloaded", required=True, default="all")):
    if cogchoice.lower() == "all":
        cogHelpers.unloadAllCogs(ctx.bot)
        await ctx.respond("Successfully unloaded all Cogs")
    else:
        try:
            client.unload_extension("cogs." + cogchoice)
            await ctx.respond("Successfully unloaded Cog " + cogchoice)
        except Exception as e:
            await ctx.respond(f"An error occurred while unloading the cog {cogchoice}! Please contact ath404 if you think something is broken and send him this: ```{e}```")

@cogs.command(description="Reloads a Cog")
async def reload(ctx, cogchoice: Option(str, "Enter the Cog that should get reloaded", required=True, default="all")):
    if cogchoice.lower() == "all":
        cogHelpers.unloadAllCogs(ctx.bot)
        cogHelpers.loadAllCogs(ctx.bot)
        await ctx.respond("Successfully reloaded all Cogs")
    else:
        try:
            client.unload_extension("cogs." + cogchoice)
            client.load_extension("cogs." + cogchoice)
            await ctx.respond("Successfully reloaded Cog " + cogchoice)
        except Exception as e:
            await ctx.respond(f"An error occurred while unloading the cog {cogchoice}! Please contact ath404 if you think something is broken and send him this: ```{e}```")
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Running and hosting

# Sends a ping to the repl.it server so that it doesn't get taken down
#keep_alive.keep_alive()

# Load all cogs on startup
# This has to happen before the on_ready event for some reason lol
print("Loading Cogs...")
cogHelpers.loadAllCogs(client)

# Runs the bot by its token
client.run(TOKEN)