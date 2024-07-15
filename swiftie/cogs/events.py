from discord.ext import commands

from ..bot import Swiftie


class Events(commands.Cog):
    def __init__(self, bot: Swiftie):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, _: commands.Context, error: commands.CommandError):
        if not isinstance(error, commands.CommandNotFound):
            raise error


async def setup(bot: Swiftie):
    await bot.add_cog(Events(bot))
