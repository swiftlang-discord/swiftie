import time

from discord.ext import commands

from ..bot import Swiftie


class Misc(commands.Cog):
    def __init__(self, bot: Swiftie):
        self.bot = bot

    @commands.command(aliases=["p"])
    async def ping(self, ctx: commands.Context):
        socket = self.bot.latency * 1000
        response = [
            "Pong! :ping_pong:",
            f"-# ⏲ Socket round-trip took {socket:.2f}ms",
        ]

        start = time.perf_counter()
        message = await ctx.send("\n".join(response))
        end = time.perf_counter()
        duration = (end - start) * 1000

        response[1] += (
            f" and server round-trip took {duration:.2f}ms • [Read more](<https://en.wikipedia.org/wiki/Network_delay>)"
        )
        await message.edit(content="\n".join(response))


async def setup(bot: Swiftie):
    await bot.add_cog(Misc(bot))
