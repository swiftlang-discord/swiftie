import asyncio

from discord.ext import commands

from ..bot import Swiftie
from ..converters import CodeBlock


class Eval(commands.Cog):
    def __init__(self, bot: Swiftie):
        self.bot = bot

    @commands.command(aliases=["e"])
    async def eval(self, ctx: commands.Context, code: CodeBlock | None):
        if code is None:
            first_line = ctx.message.content.split("\n")[0]
            if first_line.count("`") >= 2:
                try:
                    first_index = first_line.index("`")

                    if first_line[first_index + 1] == "`":
                        first_index += 1

                    second_index = first_line.index("`", first_index + 1)
                except Exception:
                    return

                code = (
                    f"import Foundation\nprint({first_line[first_index+1:second_index]})"
                )
            else:
                return

        message = await ctx.reply("Processing...")

        try:
            resp = await self.bot.jdoodle.execute(script=code)
        except asyncio.TimeoutError:
            return await message.edit(
                content="Timeout! Took too long for the server to retrieve output..."
            )

        if resp is None:
            return await message.edit(content="Oops! Unexpected internal error.")

        content: str = resp["output"]

        if not content and resp["isExecutionSuccess"]:
            return await message.edit(content="Compilation was successful.")

        if resp["isExecutionSuccess"]:
            if 20 < len(content.splitlines()) > 30:
                content = "\n".join(content.splitlines()[0:20]) + "\n..."
            elif 30 < len(content.splitlines()):
                content = content = "\n".join(content.splitlines()[0:10]) + "\n..."

        if not resp["isExecutionSuccess"]:
            if len(content) > 4000:
                content = content[3997] + "..."

        if content:
            if "timeout" in content.lower() and "jdoodle" in content.lower():
                return await message.edit(
                    content="Timeout! Took too long to evaluate code..."
                )

            content = f"""
```{"swift" if not resp["isExecutionSuccess"] else ""}
{content}
```
"""
            return await message.edit(content=content)

        await message.edit(
            content=f"Something went wrong parsing the output... Raw response:```\n{resp}\n```"
        )


async def setup(bot: Swiftie):
    await bot.add_cog(Eval(bot))
