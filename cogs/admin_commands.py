import discord
from discord.ext import bridge, commands

class AdminCommands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Rules Command

	@bridge.bridge_command(description = "Comando para mostrar las reglas en el canal (ADMIN ONLY)", guild_ids = [918985655449681930])
	@commands.has_permissions(administrator = True)
	async def rules(self, ctx):
		embed = discord.Embed(color = discord.Colour.blue())

		embed.add_field(name = "\u2063", value = "1. Respetar a todos los usuarios del Discord.", inline = False)
		embed.add_field(name = "\u2063", value = "2. Respetar los canales del servidor.", inline = False)

		embed.set_author(name = "Normas del Discord", icon_url = self.bot.user.avatar.url)

		embed.set_footer(text = "Cualquier incumplimiento de las normas puede resultar en una sanción por parte del staff.")

		await ctx.respond(embed = embed)

	# Info Command

	@bridge.bridge_command(description = "Comando para mostrar la información (ADMIN ONLY)", guild_ids = [918985655449681930])
	@commands.has_permissions(administrator = True)
	async def info(self, ctx):
		embed = discord.Embed(color = discord.Colour.blue())

		embed.add_field(name = "Rentar un servidor", value = "Para rentar un servidor, cree un Ticket reaccionando al mensaje en <#918991652444586064>", inline = False)
		embed.add_field(name = "Precios", value = "1 USD = 1 GB de RAM", inline = True)
		embed.add_field(name = "Stock", value = "[Disponible / ~~No disponible~~]", inline = True)
		embed.add_field(name = "Hardware", value = " - Procesador: AMD Ryzen 5 3600 6-Core\n - RAM: Tamaño elegible\n - Almacenamiento: NVMe Tamaño elegible", inline = False)
		embed.add_field(name = "Localización", value = "Actualmente los servicios solo están disponibles en Frankfurt, Alemania", inline = True)
		embed.add_field(name = "Sistema Operativo", value = "Ubuntu 20.04 LTS")
		embed.add_field(name = "Adiciones", value = "1) Al rentar un servidor, vendrá todo configurado y listo para su uso.\n2) A los 5 primeros compradores se les otorgará gratuitamente una IP dedicada (dominio).\n3) Acceso a los archivos y a la consola del servidor mediante SFTP y SSH respectivamente.", inline = False)

		embed.set_author(name = "Información", icon_url = self.bot.user.avatar.url)
		embed.set_footer(text = "Cualquier duda, puede contactar al Staff del servidor.")

		await ctx.respond(embed = embed)

def setup(bot):
	bot.add_cog(AdminCommands(bot))