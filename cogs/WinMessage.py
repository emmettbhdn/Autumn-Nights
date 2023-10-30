import discord
from discord.ext import commands
from core.helperFunctions import dataHelpers

class WinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Member of the Week
    @discord.slash_command(name="week_member_test", description="Tests the embed that will be used for the member of the week messages", guild_ids=dataHelpers.SERVER_IDS)
    async def week_member_test(self, ctx):
        embed=discord.Embed(title="Member of the Week: start date - end date", color=0xf38a44)
        embed.add_field(name="Winner:", value="@ath404: 123 Messages!", inline=False)
        embed.add_field(name="Runner-Up:", value="@Gorgulous-the-3st: 3 Messages!", inline=False)
        embed.set_footer(text="Congratulations to the winners! To everyone else, better luck next week!")
        await ctx.respond("Embed successfully generated!", ephemeral=True)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(WinMessage(bot))