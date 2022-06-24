import discord
from discord.ext import commands

class Welcome(commands.Cog, description = "Categoria de bienvenida"):

	def __init__(self, bot):
		self.bot = bot

	# Welcome

	@commands.Cog.listener()
	async def on_member_join(self, member):

		channel_id = 987563037479297085

		channel = self.bot.get_channel(channel_id)

		channel.send(f"**{member.user}** se ha unido al servidor.")

def setup(bot):
	bot.add_cog(Welcome(bot))