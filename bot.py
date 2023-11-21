# Import needed libraries:
import discord
from discord.ext import commands
from discord.commands import Option
import keep_alive
from core.helperFunctions import cogHelpers
from core.helperFunctions import dataHelpers
import os
import datetime
from dotenv import load_dotenv
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Variables:
load_dotenv()
TOKEN = os.environ["TOKEN"]

client = commands.Bot(
    intents=discord.Intents.all()
)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# config

# Starts up the bot and tells me when it's ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="all your messages >:)"))
    print("SERVER_IDS constant intialized at " + str(dataHelpers.SERVER_IDS))
    print('Bot initialized at ' + str(datetime.datetime.now()))
    
cogs = client.create_group("cogs", "Commands to load/unload Cogs (Admin Only)")

@cogs.command(description="Loads a Cog")
@commands.is_owner()
async def load(ctx, cogchoice: Option(str, "Enter the Cog that should get loaded", required=True, default="all")):
    if cogchoice.lower() == "all":
        cogHelpers.loadAllCogs(ctx.bot)
        await ctx.respond("Successfully loaded in all Cogs")
    else:
        try:
            client.load_extension("cogs." + cogchoice)
            await ctx.respond("Successfully loaded in Cog " + cogchoice)
        except Exception as e:
            await ctx.respond(f"An error occurred while loading the cog {cogchoice}! Please contact ath404 if you think something is broken and send him this: ```{e}```")
            
@cogs.command(description="Unloads a Cog")
@commands.is_owner()
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
@commands.is_owner()
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
            await ctx.respond(f"An error occurred while reloading the cog {cogchoice}! Please contact ath404 if you think something is broken and send him this: ```{e}```")

@cogs.command(name="status", description="Shows the status (loaded or unloaded) of all cogs")
@commands.is_owner()
async def cog_status(ctx):
    cogs = cogHelpers.getCogList()
    cog_statuses = {}
    message = ""
    for cog in cogs:
        try:
            client.load_extension("cogs." + cog)
        except discord.ExtensionAlreadyLoaded:
            cog_statuses[cog] = ":white_check_mark: Loaded"
        except discord.ExtensionNotFound:
            cog_statuses[cog] = ":question: Not Found"
        except discord.ExtensionFailed:
            cog_statuses[cog] = ":interrobang: Failed"
        else:
            cog_statuses[cog] = ":x: Unloaded"
            client.unload_extension("cogs." + cog)

        message += f"\n\n{cog}:      {cog_statuses[cog]}"
        
    await ctx.respond(message)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Running and hosting

# Sends a ping to the repl.it server so that it doesn't get taken down
keep_alive.keep_alive()

# Load all cogs on startup
# This has to happen before the on_ready event for some reason lol
print("Loading Cogs...")
cogHelpers.loadAllCogs(client)

# Runs the bot by its token
client.run(TOKEN)