import discord
from discord.ext import commands

import datetime
from pytz import timezone

# Log Nickname, Discriminator, Username, Nickname in server, Avatar, Roles, Message Edit, Message Delete, Join Server, Leave Server, Join Voice, Leave Voice, Server Deaf, Server Undeaf, Server Mute, Server Unmute, Start Stream, Stop Stream, Start Video, Stop Video

class Logger(commands.Cog, description = "Categoria de registro"):

	def __init__(self, bot):
		self.bot = bot
	
	# Ready and get Log Channel

	@commands.Cog.listener()
	async def on_ready(self):
		self.log_channel = self.bot.get_channel(919014237458804736)

	# Nickname and Role Changes Logger

	@commands.Cog.listener()
	async def on_member_update(self, after, before):
		if before.display_name != after.display_name:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(title = "Cambio de apodo", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = after, icon_url = after.avatar.url)

			embed.add_field(name = "Nuevo apodo", value = before.display_name, inline = False)
			embed.add_field(name = "Antiguo apodo", value = after.display_name, inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {after.id}\n```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.roles != after.roles:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(title = "Actualización de roles", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = after, icon_url = after.avatar.url)

			embed.add_field(name = "Roles nuevos", value = ", ".join([r.mention for r in before.roles if r != before.guild.default_role]), inline = False)
			embed.add_field(name = "Roles antiguos", value = ", ".join([r.mention for r in after.roles if r != after.guild.default_role]), inline = False)

			await self.log_channel.send(embed = embed)

	# Discord Username, Discriminator and Avatar Changes Logger

	@commands.Cog.listener()
	async def on_user_update(self, after, before):
		if before.name != after.name:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(title = "Cambio de nombre de usuario", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = after, icon_url = after.avatar.url)

			embed.add_field(name = "Nuevo nombre de usuario", value = before.name, inline = False)
			embed.add_field(name = "Antiguo nombre de usuario", value = after.name, inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {after.id}\n```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.discriminator != after.discriminator:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(title = "Cambio de discriminador", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = after, icon_url = after.avatar.url)

			embed.add_field(name = "Nuevo discriminador", value = before.discriminator, inline = False)
			embed.add_field(name = "Antiguo discriminador", value = after.discriminator, inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {after.id}\n```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.avatar.url != after.avatar.url:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(title = "Cambio de avatar", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = after, icon_url = before.avatar.url)

			embed.add_field(name = "Nueva foto", value = "(Foto de abajo)", inline = False)
			embed.add_field(name = "Antigua foto", value = "(Foto de la derecha)", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {after.id}\n```", inline = False)

			embed.set_thumbnail(url = after.avatar.url)
			embed.set_image(url = before.avatar.url)

			await self.log_channel.send(embed = embed)

	# Edited Message Logger

	@commands.Cog.listener()
	async def on_message_edit(self, after, before):
		if not after.author.bot:
			if before.content != after.content:

				utc = datetime.datetime.now()
				local = utc.astimezone(timezone('Etc/GMT+3'))

				embed = discord.Embed(description = f"{after.author} ha actualizado su mensaje en: {after.channel.name}.", timestamp = local, color = discord.Color.blue())

				embed.add_field(name = "Canal", value = f"{after.channel.mention} ({after.channel.name})\n[Ir al mensaje]({after.jump_url})", inline = False)
				embed.add_field(name = "Mensaje actual", value = before.content, inline = False)
				embed.add_field(name = "Mensaje antiguo", value = after.content, inline = False)
				embed.add_field(name = "ID", value = f"```fix\nUsuario = {after.author.id}\nMensaje = {after.id}```", inline = False)

				embed.set_author(name = after.author, icon_url = after.author.avatar.url)

				await self.log_channel.send(embed = embed)

	# Delete Message Logger

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))  

			embed = discord.Embed(description = f"Mensaje borrado en {message.channel.mention}", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = message.author, icon_url = message.author.avatar.url)

			embed.add_field(name = "Contenido", value = message.content, inline = False)

			utc_time = message.created_at
			local_time = utc_time.astimezone(timezone('Etc/GMT+3'))
			time = local_time.__format__("%A, %B %d, %Y %H:%M %p")

			embed.add_field(name = "Fecha", value = time, inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {message.author.id}\nMensaje = {message.id}```", inline = False)

			await self.log_channel.send(embed = embed)

	# Join Logger

	@commands.Cog.listener()
	async def on_member_join(self, member):

		utc_time = member.created_at
		local_time = utc_time.astimezone(timezone('Etc/GMT+3'))
		time = local_time.__format__("%A, %B %d, %Y %H:%M %p")

		utc_time_joined = member.joined_at
		local_time_joined = utc_time_joined.astimezone(timezone('Etc/GMT+3'))
		time_joined = local_time_joined.__format__("%A, %B %d, %Y %H:%M %p")

		utc = datetime.datetime.now()
		local = utc.astimezone(timezone('Etc/GMT+3'))  

		embed = discord.Embed(description = f"{member.mention} se ha unido", timestamp = local, color = discord.Colour.green())

		embed.set_author(name = member, icon_url = member.avatar.url)

		embed.add_field(name = "Nombre", value = f"{member} ({member.id}) {member.mention}", inline = False)
		embed.add_field(name = "Fecha de ingreso", value = time_joined, inline = False)
		embed.add_field(name = "Fecha de creación", value = time, inline = False)
		embed.add_field(name = "Miembros totales", value = member.guild.member_count, inline = True)

		embed.add_field(name = "ID", value = f"```fix\nMember = {member.id}```", inline = False)

		await self.log_channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_member_remove(self, member):

		utc_time = member.created_at
		local_time = utc_time.astimezone(timezone('Etc/GMT+3'))
		time = local_time.__format__("%A, %B %d, %Y %H:%M %p")

		utc_time_joined = member.joined_at
		local_time_joined = utc_time_joined.astimezone(timezone('Etc/GMT+3'))
		time_joined = local_time_joined.__format__("%A, %B %d, %Y %H:%M %p")

		utc = datetime.datetime.now()
		local = utc.astimezone(timezone('Etc/GMT+3'))  

		embed = discord.Embed(description = f"{member} ha salido", timestamp = local, color = discord.Colour.red())

		embed.set_author(name = member, icon_url = member.avatar.url)

		embed.add_field(name = "Información del usuario", value = f"{member} ({member.id}) {member.mention}", inline = False)
		embed.add_field(name = "Roles", value = ", ".join([r.mention for r in member.roles if r != member.guild.default_role]), inline = False)
		embed.add_field(name = "Fecha de ingreso", value = time_joined, inline = False)
		embed.add_field(name = "Fecha de creación", value = time, inline =  False)
		embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```")

		await self.log_channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if before.channel is None and after.channel is not None:
				
			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** se unió a: {after.channel.name}", timestamp = local, color = discord.Colour.green())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "Canal", value = f"{after.channel.mention} ({after.channel.id})", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False) 

			await self.log_channel.send(embed = embed)

		elif before.channel is not None and after.channel is None:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** salió de: {before.channel.name}", timestamp = local, color = discord.Colour.red())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "Canal", value = f"{before.channel.mention} ({before.channel.id})", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False) 

			await self.log_channel.send(embed = embed)

		if before.self_video is False and after.self_video is True:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** encedió su cámara en: {after.channel.name}", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "Canal", value = f"{after.channel.mention} ({after.channel.id})", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.self_video is True and after.self_video is False:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** apagó su cámara en: {before.channel.name}", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "Canal", value = f"{before.channel.mention} ({before.channel.id})", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		if before.self_stream is False and after.self_stream is True:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** empezó a compartir pantalla en: {after.channel.name}", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "Canal", value = f"{after.channel.mention} ({after.channel.id})", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.self_stream is True and after.self_stream is False:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** dejó de compartir pantalla en: {before.channel.name}", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "Canal", value = f"{before.channel.mention} ({before.channel.id})", inline = False)
			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		if before.mute is False and after.mute is True:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** fué silenciado en el servidor", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.mute is True and after.mute is False:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** fué desilenciado en el servidor", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		if before.deaf is False and after.deaf is True:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** fué ensordecido en el servidor", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

		elif before.deaf is True and after.deaf is False:

			utc = datetime.datetime.now()
			local = utc.astimezone(timezone('Etc/GMT+3'))

			embed = discord.Embed(description = f"**{member}** fué desensordecido en el servidor", timestamp = local, color = discord.Color.blue())

			embed.set_author(name = f"{member} ({member.display_name})", icon_url = member.avatar.url)

			embed.add_field(name = "ID", value = f"```fix\nUsuario = {member.id}```", inline = False)

			await self.log_channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		...

def setup(bot):
	bot.add_cog(Logger(bot))