import discord
from discord.ext import bridge, commands

GUILD_ID = 918985655449681930
POLL_CHANNEL_ID = 989680051786227802

class Polls(commands.Cog, description = "Categoria de encuestas"):

	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description = "Comando para realizar una encuesta (ADMIN ONLY).", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def encuesta(self, ctx, agree_emoji : discord.Emoji, disagree_emoji : discord.Emoji, *, poll_text):

		channel = self.bot.get_channel(POLL_CHANNEL_ID)

		embed = discord.Embed(
			description = "📤 Nueva encuesta!",
			color = discord.Color.blue()
		)

		embed.add_field(name = "Encuesta", value = f"{poll_text}", inline = False)
		embed.add_field(name = "Staff", value = f"{ctx.author.mention}", inline = True)

		embed.set_author(name = f"Killer Hosting | Encuestas", icon_url = self.bot.user.avatar.url)

		poll_role = discord.utils.get(ctx.guild.roles, name = "Encuestas")

		msg = await channel.send(f"{poll_role.mention}", embed = embed)

		await msg.add_reaction(agree_emoji)
		await msg.add_reaction(disagree_emoji)

def setup(bot):
	bot.add_cog(Polls(bot))