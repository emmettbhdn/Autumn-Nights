import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option
from core.helperFunctions import dataHelpers
import random

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    random = SlashCommandGroup("random", "Commands to genereate random things")
    
    @random.command(name="member", description="Mentions a random member", guild_ids=dataHelpers.SERVER_IDS)
    async def random_member(self, ctx):
        members = await ctx.guild.fetch_members(limit=None).flatten()
        await ctx.respond(random.choice(members).mention)
    
    @random.command(name="number", description="Generates a random number in a range", guild_ids=dataHelpers.SERVER_IDS)
    async def random_number(self, ctx, min: Option(int, "Enter the minimum number", required=True, default=0), max: Option(int, "Enter the maximum number", required=True, default=100)):
        rand_num = random.randint(min, max)
        await ctx.respond("Your number is " + rand_num)
     
        
def setup(bot):
    bot.add_cog(Random(bot))