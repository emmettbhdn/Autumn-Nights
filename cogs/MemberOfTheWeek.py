import discord
from discord.ext import commands
from core.helperFunctions import memberHelpers, dataHelpers 
from discord.commands import Option

class MemberOfTheWeek(commands.Cog):
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

    @discord.slash_command(name="get_member_messages", guild_ids=dataHelpers.SERVER_IDS)
    @commands.has_permissions(administrator=True)
    async def get_member_messages(self, ctx, member_id: Option(str, "Id of the Member", required=True)):
        await ctx.respond(memberHelpers.getMemberMessages(int(member_id)), ephemeral=True)
        
    @discord.slash_command(name="generate_member_message_dict", guild_ids=dataHelpers.SERVER_IDS)
    @commands.has_permissions(administrator=True)
    async def gen_dict(self, ctx):
        await memberHelpers.resetMemberMessageDict(ctx.guild)
        await ctx.respond("Generated member message dict!")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            memberHelpers.addMemberMessages(message.author.id, 1)
            print(f"Added 1 message to member {message.author.id} ({message.author.name})")
        else:
            pass
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        dict = memberHelpers.loadMemberMessageDict()
        del dict[member.id]
        memberHelpers.saveMemberMessageDict(dict)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        dict = memberHelpers.loadMemberMessageDict()
        dict[member.id] = 0
        memberHelpers.saveMemberMessageDict(dict)
        
def setup(bot):
    bot.add_cog(MemberOfTheWeek(bot))