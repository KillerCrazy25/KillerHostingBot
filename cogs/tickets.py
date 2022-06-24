import discord
from discord.ext import bridge, commands
from discord.ui import View
from asyncio import sleep

# Variables

SUPPORT_ROLE_ID = 918986464476418068
ADMIN_ROLE_ID = 918986273211961354
GUILD_ID = 918985655449681930

NEW_TICKETS_NOTIFICATIONS_CHANNEL_NAME_ID = 988593820801327125

TICKET_CATEGORY_NAME = "Tickets Activos"

ticket_category = None
support_role = None
admin_role = None
guild = None

class TicketsView(View):

	def __init__(self):
		super().__init__(timeout = None)

	# Rent Server Ticket Button

	@discord.ui.button(label = "Rentar Servidor", style = discord.ButtonStyle.primary, emoji = "🖥") 
	async def rent_button_callback(self, button, interaction):
		await interaction.response.defer()

		# Embed

		ticket_create_embed = discord.Embed(
			title = "🖥 | Rentar Servidor",
			description = f"Hola {interaction.user.mention}, tu ticket ha sido creado correctamente, por favor especifica los recursos que necesitarás para tu servidor (Cantidad de RAM, IP Dedicada, Pre-configuración, etc)",
			color = discord.Color.blue()
		)

		# Channel Permissions

		overwrites = {
			guild.default_role: discord.PermissionOverwrite(view_channel = False),
			interaction.user: discord.PermissionOverwrite(view_channel = True)
		}

		ticket = await ticket_category.create_text_channel(f"ticket-{interaction.user.name}", overwrites = overwrites)

		await ticket.send(f"{interaction.user.mention}", embed = ticket_create_embed)
		await notifications_channel.send(f"{support_role.mention} nuevo ticket!")

	# Support Ticket Button

	@discord.ui.button(label = "Soporte General", style = discord.ButtonStyle.primary, emoji = "✉") 
	async def support_button_callback(self, button, interaction):
		await interaction.response.defer()

		# Embed

		ticket_create_embed = discord.Embed(
			title = "✉ | Soporte General",
			description = f"Hola {interaction.user.mention}, tu ticket ha sido creado correctamente, describe tu problema brevemente.",
			color = discord.Color.blue()
		)

		# Channel Permissions

		overwrites = {
			guild.default_role: discord.PermissionOverwrite(view_channel = False),
			interaction.user: discord.PermissionOverwrite(view_channel = True)
		}

		ticket = await ticket_category.create_text_channel(f"ticket-{interaction.user.name}", overwrites = overwrites)

		await ticket.send(f"{interaction.user.mention}", embed = ticket_create_embed)
		await notifications_channel.send(f"{support_role.mention} nuevo ticket!")

# Ticket System Cog

class Tickets(commands.Cog, description = "Categoria de Tickets"):

	def __init__(self, bot):
		self.bot = bot

	# Load Variables

	@commands.Cog.listener()
	async def on_ready(self):
		global guild, ticket_category, ticket_mod_role, management_role, notifications_channel

		guild = self.bot.get_guild(GUILD_ID)

		ticket_category = discord.utils.get(guild.categories, name = TICKET_CATEGORY_NAME)
		support_role = discord.utils.get(guild.roles, id = SUPPORT_ROLE_ID)
		admin_role = discord.utils.get(guild.roles, id = ADMIN_ROLE_ID)
		notifications_channel = self.bot.get_channel(NEW_TICKETS_NOTIFICATIONS_CHANNEL_NAME_ID)

	# Send Ticket Message

	@bridge.bridge_command(description = "Enviar mensaje para crear tickets (ADMIN ONLY)", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def sendticket(self, ctx):
		rent_embed = discord.Embed(
			title = "🖥 | Rentar Servidor",
			description = "Para comenzar el proceso de compra, haz click en el botón `Rentar Servidor`.",
			color = discord.Color.blue()
		)

		support_embed = discord.Embed(
			title = "✉ | Soporte General",
			description = "Para recibir soporte sobre nuestros servicios, haz click en el botón `Soporte General`.",
			color = discord.Color.blue()
		)

		await ctx.respond(embeds = [rent_embed, support_embed], view = TicketsView())

	# Close Ticket

	@bridge.bridge_command(description = "Comando para cerrar un ticket (ADMIN ONLY)", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def closeticket(self, ctx):
		try:
			if ctx.channel.name.startswith("ticket-"):
				await ctx.respond("Este ticket será cerrado en 15 segundos...")
				await sleep(15)
				await ctx.channel.delete()
			else:
				await ctx.respond("❌ Por favor ejecuta el comando en un canal de ticket.")
		except:
			await ctx.respond("❌ Por favor ejecuta el comando en un canal de ticket.")

def setup(bot):
	bot.add_cog(Tickets(bot))
