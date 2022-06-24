import discord
from discord.ext import bridge, commands
from discord.ui import View

GUILD_ID = 918985655449681930

# Select Menu Subclass

class RolesView(View):

	def __init__(self):
		super().__init__(timeout = None)

	# Select Menu

	@discord.ui.select( 
		placeholder = "Selecciona un rol", 
		min_values = 0,
		max_values = 4,
		options = [
			discord.SelectOption(
				label = "Estado del servidor",
				description = "Recibirás notificaciones del estado de los servidores!",
				emoji = "📊",
				value = "987875091306119188"
			),
			discord.SelectOption(
				label = "Anuncios",
				description="Recibirás notificaciones del servidor de Discord!",
				emoji = "📣",
				value = "987874811642531840"
			),
			discord.SelectOption(
				label = "Sorteos",
				description = "Recibirás notificaciones de nuevos sorteos!",
				emoji = "🎁",
				value = "987874982065487872"
			),
			discord.SelectOption(
				label = "Encuestas",
				description = "Recibirás notificaciones de nuevas encuestas!",
				emoji = "📋",
				value = "989308826274631770"
			)
		]
	)

	# Callback

	async def select_callback(self, select, interaction):

		await interaction.response.defer()

		status_role = discord.utils.get(interaction.user.guild.roles, name = "Estado del servidor")
		announces_role = discord.utils.get(interaction.user.guild.roles, name = "Anuncios generales")
		giveaways_role = discord.utils.get(interaction.user.guild.roles, name = "Sorteos")		
		poll_role = discord.utils.get(interaction.user.guild.roles, name = "Encuestas")

		list_roles = [announces_role, giveaways_role, status_role, poll_role]

		for role in interaction.user.roles:
			for rolelist in list_roles:
				if role == rolelist:
					if role not in select.values: 
						await interaction.user.remove_roles(role)

		if len(select.values) != 0:
			for choice in select.values:
				if choice == "987875091306119188":
					await interaction.user.add_roles(status_role)
				elif choice == "987874811642531840":
					await interaction.user.add_roles(announces_role)
				elif choice == "987874982065487872":
					await interaction.user.add_roles(giveaways_role)
				elif choice == "989308826274631770":
					await interaction.user.add_roles(poll_role)

# AutoRoles Cog

class AutoRoles(commands.Cog, description = "Categoria de selección de roles"):

	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description = "Enviar el mensaje para escoger los roles (ADMIN ONLY).", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def roles(self, ctx):

		embed = discord.Embed(title = "🔊 Notificaciones del servidor", description = "Selecciona los roles de las notificaciones que quieres recibir en el servidor. Elige entre los siguientes roles:")

		embed.add_field(name = "\u2063", value = "**📊 Estado del servidor\n📣 Anuncios generales\n🎁 Sorteos\n📋 Encuestas**")

		embed.set_footer(text = "\u2063")

		await ctx.send(embed = embed, view = RolesView())

def setup(bot):
	bot.add_cog(AutoRoles(bot))