# main.py
from nextcord.ext import commands
from nextcord import slash_command
from utilities.locate.main import locale
from utilities.ui.ui import UI

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        if amount <= 0 or amount > 100:
            embed = UI.error_embed(
                description=locale.get(
                    "moderation.clear.invalid_amount",
                    ctx.locale_code,
                    max=100
                )
            )
            await ctx.send(embed=embed, delete_after=5)
            return

        await ctx.channel.purge(limit=amount + 1)
        embed = UI.success_embed(
            description=locale.get(
                "moderation.clear.success",
                ctx.locale_code,
                count=amount
            )
        )
        await ctx.send(embed=embed, delete_after=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = UI.error_embed(
                description=locale.get(
                    "moderation.clear.error_permissions",
                    ctx.locale_code
                )
            )
            await ctx.send(embed=embed, delete_after=5)

def setup(bot):
    bot.add_cog(ModCommands(bot))