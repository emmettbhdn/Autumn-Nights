import discord
from discord.ext import commands
from discord.commands import Option
from core.helperFunctions import dataHelpers
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.slash_command(name="send_bot_message", description="Sends a message to a specified channel (Admin only)", guild_ids=dataHelpers.SERVER_IDS)
    @commands.has_permissions(administrator=True)
    async def send_bot_message(self, ctx, message: Option(str, "Message to be sent", required=True), channel_id: Option(str, "Id of the channel, where the message should get sent", required=True)):
        try:
            channel_id = int(channel_id)
        except TypeError:
            await ctx.respond("Error: Channel Id must be a number")
        
        channel = await self.bot.fetch_channel(channel_id)
        await channel.send(message)
    
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if random.randint(1, 1) == 1: # 1 in 1000 Chance
            author = message.author
            guild = await self.bot.fetch_guild(dataHelpers.SERVER_IDS[0])
            role = guild.get_role(dataHelpers.RANDOM_CHANCE_ROLE_ID)
            await message.reply("Congrats! You won the 1 in 1000 odds and have recieved the Cookie role!")
            await author.add_roles(role, reason="Random Chance Role")
            
     
        
def setup(bot):
    bot.add_cog(Fun(bot))