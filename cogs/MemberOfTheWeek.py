import discord
from discord.ext import commands, tasks
from core.helperFunctions import memberHelpers, dataHelpers 
from discord.commands import Option
import datetime

# TODO: Reset the Message count database every week and send a winner message in the appropriate channel. It should happen at the same time each week and the exact time should not depend on startup time

class MemberOfTheWeek(commands.Cog):
		def __init__(self, bot):
				self.bot = bot

		# Member of the Week
		@discord.slash_command(name="week_member_test", description="Tests the embed that will be used for the member of the week messages", guild_ids=dataHelpers.SERVER_IDS)
		async def week_member_test(self, ctx):
				embed=discord.Embed(title=f"Member of the Week: {(datetime.date.today() - datetime.timedelta(days=7)).strftime(r'%m/%d/%y')}  -  {datetime.date.today().strftime(r'%m/%d/%y')}", color=0xf38a44)
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
						# print(f"Added 1 message to member {message.author.id} ({message.author.name})")
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

		@commands.Cog.listener()
		async def on_ready(self):
				self.weekly_message_loop.start()

		@tasks.loop(time=datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc))
		async def weekly_message_loop(self, weekday_check_override = True):
				if datetime.datetime.now().weekday() != 6 and weekday_check_override == False: # Only allow the loop to execute if it is monday. This allows the loop to only execute on Monday at 21:00
						return
				print("Weekly member message loop being run...")

				message_dict = memberHelpers.loadMemberMessageDict()

				winner_member = memberHelpers.getMember(self.bot, dataHelpers.getNthKeyInSortedDict(message_dict, 0))
				winner_messages = message_dict[winner_member.id]
				runner_up_member = memberHelpers.getMember(self.bot, dataHelpers.getNthKeyInSortedDict(message_dict, 1))
				runner_up_messages = message_dict[runner_up_member.id]

				winner_embed = discord.Embed(
						title=f"Member of the Week: {(datetime.date.today() - datetime.timedelta(days=7)).strftime(r'%m/%d/%y')}  -  {datetime.date.today().strftime(r'%m/%d/%y')}",
						color=0xf38a44
				)

				winner_embed.add_field(name="Winner:", value=f"{winner_member.mention}: {winner_messages} messages!", inline=False)
				winner_embed.add_field(name="Runner-Up:", value=f"{runner_up_member.mention}: {runner_up_messages} messages!", inline=False)
				winner_embed.set_footer(text="Congratulations to the winners! To everyone else, better luck next week!")

				weekly_message_channel = await self.bot.fetch_channel(dataHelpers.WEEKLY_MESSAGE_CHANNEL_ID)
				weekly_message_role = discord.utils.get(weekly_message_channel.guild.roles, id=dataHelpers.MEMBER_OF_THE_WEEK_ROLE_ID)
				#await weekly_message_channel.send(content=f"{weekly_message_role.mention}", embed=winner_embed)
				await weekly_message_channel.send(embed=winner_embed)

				if weekday_check_override == False:
						guild = self.bot.fetch_guild(dataHelpers.SERVER_IDS[0])
						await memberHelpers.resetMemberMessageDict(guild)


def setup(bot):
		bot.add_cog(MemberOfTheWeek(bot))