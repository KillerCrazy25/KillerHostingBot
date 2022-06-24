import discord
from discord.ext import bridge, commands

GUILD_ID = 918985655449681930
SUGGESTION_CHANNEL_ID = 989308238799470593

# Suggestions Cog

class Suggestions(commands.Cog, description = "Categoria del comando de sugerencias"):

	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description = "Comando para realizar sugerencias", guild_ids = [GUILD_ID])
	async def sugerir(self, ctx, *, suggestion: str):
		if suggestion:
			embed = discord.Embed(
				description = f"📋 Una nueva sugerencia ha sido recibida!",
				color = discord.Color.blue()
			)

			embed.add_field(name = "Sugerencia", value = f"{suggestion}", inline = False)
			embed.add_field(name = "Autor", value = f"{ctx.author.mention}", inline = True)
			embed.add_field(name = "Estado", value = "Votando | Esperando aprobación del Staff.", inline = True)

			embed.set_author(name = "Killer Hosting | Sugerencias", icon_url = self.bot.user.avatar.url)

			channel = self.bot.get_channel(SUGGESTION_CHANNEL_ID)

			msg = await channel.send(embed = embed)

			await msg.add_reaction("✅")
			await msg.add_reaction("❌")

			await msg.edit(f"ID: {msg.id}")
			
		else:
			await ctx.respond("Por favor describe tu sugerencia.")

	@bridge.bridge_command(description = "Comando para aprobar sugerencia (ADMIN ONLY).", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def aprobar(self, ctx, id, *, comment):
		if id is None:
			await ctx.send("Por favor especifica la ID de la sugerencia que deseas aprobar.")
			return

		channel = self.bot.get_channel(SUGGESTION_CHANNEL_ID)
		suggestion = await channel.fetch_message(id)

		embed = discord.Embed(
			description = f"✅ Sugerencia aprobada!",
			color = discord.Color.blue()
		)

		embed.add_field(name = "Comentario", value = f"{comment}", inline = False)
		embed.add_field(name = "Staff", value = f"{ctx.author.mention}", inline = True)
		embed.add_field(name = "ID", value = f"{id}", inline = True)

		embed.set_author(name = "Killer Hosting | Sugerencias", icon_url = self.bot.user.avatar.url)

		await suggestion.reply(embed = embed)

	@bridge.bridge_command(description = "Comando para desaprobar sugerencia (ADMIN ONLY).", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def desaprobar(self, ctx, id, *, comment):
		if id is None:
			await ctx.send("Por favor especifica la ID de la sugerencia que deseas aprobar.")
			return

		channel = self.bot.get_channel(SUGGESTION_CHANNEL_ID)
		suggestion = await channel.fetch_message(id)

		embed = discord.Embed(
			description = f"❌ Sugerencia desaprobada!",
			color = discord.Color.blue()
		)

		embed.add_field(name = "Comentario", value = f"{comment}", inline = False)
		embed.add_field(name = "Staff", value = f"{ctx.author.mention}", inline = True)
		embed.add_field(name = "ID", value = f"{id}", inline = True)

		embed.set_author(name = "Killer Hosting | Sugerencias", icon_url = self.bot.user.avatar.url)

		await suggestion.reply(embed = embed)

def setup(bot):
	bot.add_cog(Suggestions(bot))