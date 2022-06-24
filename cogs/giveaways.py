import discord
from discord.ext import commands, bridge
from discord.ui import View, Button

import asyncio
import random

GUILD_ID = 918985655449681930

users = []

# Giveaway Button View Subclass

class GiveawayView(View):

	def __init__(self):
		super().__init__(timeout = None)

	@discord.ui.button(label = "Participar!", style = discord.ButtonStyle.primary, emoji = "🎁") 
	async def first_button_callback(self, button, interaction):
		if interaction.user not in users:
			users.append(interaction.user)
			print(f"Added {interaction.user} to giveaway")
			await interaction.response.send_message("Te has inscrito al sorteo. Suerte!", ephemeral = True)

	@discord.ui.button(label = "Salir del sorteo!", style = discord.ButtonStyle.danger, emoji = "❌")
	async def second_button_callback(self, button, interaction):
		if interaction.user in users:
			users.remove(interaction.user)
			print(f"Removed {interaction.user} from giveaway")
			await interaction.response.send_message("Has abandonado el sorteo.", ephemeral = True)

# Giveaways Cog

class Giveaways(commands.Cog, description = "Categoria de sorteos"):
	
	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description = "Comando para realizar sorteos", guild_ids = [GUILD_ID])
	@commands.has_permissions(administrator = True)
	async def giveaway(self, ctx):
		timeout = 15

		# Question Embeds

		channel_embed = discord.Embed(title = "🎁 | Configuración de sorteos", color = discord.Color.blue())
		channel_embed.add_field(name = "❓ | 1. ¿En que canal se alojará el sorteo?", value = "Ejemplo: `#sorteos`")

		duration_embed = discord.Embed(title = "🎁 | Configuración de sorteos", color = discord.Color.blue())
		duration_embed.add_field(name = "❓ | 2. Especifica el tiempo que tendrán los usuarios para ingresar al sorteo.", value = "Valores válidos: `<s = segundos|m = minutos|h = horas|d = dias|w = semanas>`\nEjemplo: `1d`")

		prize_embed = discord.Embed(title = "🎁 | Configuración de sorteos", color = discord.Color.blue())
		prize_embed.add_field(name = "❓ | 3. ¿Cual es el premio del sorteo?", value = "Ejemplo: `Servidor de Minecraft de 2 GB de RAM`")

		# Lists

		questions = [channel_embed, duration_embed, prize_embed]
		answers = []

		# Check Function

		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel

		# Convert Function

		def convert(time):
			pos = ["s", "m", "h", "d", "w"]
			time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24, "w": 3600 * 24 * 7}
			unit = time[-1]

			if unit not in pos:
				return -1
			try:
				val = int(time[:-1])
			except:
				return -2

			return val * time_dict[unit]

		# Sending Error Embeds

		for i in questions:
			await ctx.respond(embed = i)

			try:
				msg = await self.bot.wait_for("message", timeout = timeout, check = check)

			except asyncio.TimeoutError:
				error_embed = discord.Embed(title = "🎁 | Configuración de sorteos", description = f"No respondiste a tiempo. Recuerda que tu respuesta tiene que ser en menos de {timeout} segundos.")

				await ctx.respond(embed = error_embed)
				return
			
			else:
				answers.append(msg.content)
		
		try:
			channel_id = int(answers[0][2: -1])
			
		except:
			error_embed = discord.Embed(title = "🎁 | Configuración de sorteos", description = "No especificaste un canal correctamente.")

			await ctx.respond(embed = error_embed)
			return
		
		channel = self.bot.get_channel(channel_id)
		global time
		time = convert(answers[1])

		if time == -1:
			error_embed = discord.Embed(title = "🎁 | Configuración de sorteos", description = "No especificaste una duración correcta.")

			await ctx.respond(embed = error_embed)
			return

		elif time == -2:
			error_embed = discord.Embed(title = "🎁 | Configuración de sorteos", description = "La duración debe ser un número entero.")
		
			await ctx.respond(embed = error_embed)
			return

		prize = answers[2]

		setup_embed = discord.Embed(title = "🎁 | Configuración de sorteos", description = "La configuración ha sido finalizada. Iniciando sorteo...")

		setup_embed.add_field(name = "Canal:", value = f"{channel.mention}")
		setup_embed.add_field(name = "Tiempo:", value = f"{answers[1]}")
		setup_embed.add_field(name = "Premio:", value = prize)

		await ctx.respond(embed = setup_embed)

		print(f"New Giveaway Started! Hosted By: {ctx.author.mention} | Channel: {channel.mention} | Time: {answers[1]} | Prize: {prize}")

		public_embed = discord.Embed(title = f"🎁 | Nuevo sorteo!", description = f"Click en el botón para participar!")

		public_embed.add_field(name = "Tiempo:", value = answers[1])
		public_embed.add_field(name = "Anfitrión:", value = ctx.author.mention)

		giveaways_role = discord.utils.get(ctx.guild.roles, name = "Sorteos")
		msg = await channel.send(f"{giveaways_role.mention}", embed = public_embed, view = GiveawayView())

		await asyncio.sleep(time)

		new_msg = await channel.fetch_message(msg.id)

		winner = random.choice(users)

		await channel.send(f"🎁 Felicidades! {winner.mention} ganó: **{prize}**!")

		embed2 = discord.Embed(description = f"🏆 **Ganador:** {winner.mention}")

		embed2.set_footer(text = "El sorteo ha terminado con exito.")

		await msg.edit(embed = embed2, view = None)

def setup(bot):
	bot.add_cog(Giveaways(bot))