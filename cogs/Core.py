import discord
from discord.ext import commands
from time import sleep as sl
from core.helperFunctions import dataHelpers

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
        # Shuts the bot down
    @discord.slash_command(name="shutdown", description="Shuts the bot down (Admin Only)", guild_ids=dataHelpers.SERVER_IDS)
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        try:
            print("Shutting down the bot...")
            await ctx.respond("Shutting down the bot...\n(This might take a few seconds)\nMessage ath404 to get it back up!")
            sl(1)
            await ctx.bot.close()
            print("Goodbye! :)")
            sl(2)
        except discord.ext.commands.MissingPermissions:
            await ctx.respond("Sorry, but you can't run that command!")

    # General testing command
    @discord.slash_command(name="test", description="General testing command", guild_ids=dataHelpers.SERVER_IDS)
    async def test(self, ctx):
        await ctx.respond('Test successful!')

    @discord.slash_command(name="embed_test", description="General embed testing command", guild_ids=dataHelpers.SERVER_IDS)
    async def embed_test(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title="Testing Embed",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer a dui sed nunc vestibulum tristique sed ac metus. Vestibulum id est a urna auctor lacinia. Mauris accumsan sem at est iaculis, in hendrerit diam faucibus. Vestibulum vehicula nibh eget iaculis facilisis. In in ornare neque. Mauris laoreet ex ac condimentum tincidunt. Nam placerat, dui eget finibus malesuada, urna mi rhoncus arcu, non consectetur sem velit a sapien. In eu tortor in dolor rutrum porta. Nam id ligula metus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aenean vitae bibendum libero."
        )
        embed.set_author(name="ath404")
        embed.set_footer(text="Autumn Nights is objectively the best server on discord")
        await ctx.respond(embed=embed)

    # Command to get the latency(ping) of the bot/api
    @discord.slash_command(name="ping", description="Displays the bot's latency(ping)", guild_ids=dataHelpers.SERVER_IDS)
    async def ping(self, ctx):
        await ctx.respond(f':ping_pong:Pong!\n```ini\n[{round(self.bot.latency * 1000)}ms]\n```')
    
    @discord.slash_command(name="test2", guild_ids=dataHelpers.SERVER_IDS)
    async def test2(self, ctx):
        await ctx.respond("Test 2 message")

def setup(bot):
    bot.add_cog(Core(bot))