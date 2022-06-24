import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Error Handler

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"No tienes permisos para usar este comando. Permisos faltantes: `{error.missing_permissions}`.")
		elif isinstance(error, commands.MissingAnyRole):
			await ctx.send(f"Te faltan los roles `{error.missing_roles}` para ejecutar este comando.")
		elif isinstance(error, commands.MissingRole):
			await ctx.send(f"Necesitas el rol `{error.missing_role}` para ejecutar este comando.")
		elif isinstance(error, commands.MemberNotFound):
			await ctx.send(f"Lo siento, no pude encontrar a `{error.argument}` en el servidor.")
		elif isinstance(error, commands.TooManyArguments):
			await ctx.send(f"Proporcionaste demasiados argumentos. Argumentos que sobran: `{error.args}`")

def setup(bot):
	bot.add_cog(ErrorHandler(bot))