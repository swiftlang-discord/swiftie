import asyncio

from discord.ext import commands
import discord

from ..bot import Swiftie
from ..converters import CodeBlock


class Eval(commands.Cog):
    def __init__(self, bot: Swiftie):
        self.bot = bot

    @commands.command(aliases=["e"])
    async def eval(self, ctx: commands.Context, code: CodeBlock | None):
        with_reply_code = False

        if ctx.message.reference:
            if isinstance(ctx.message.reference.resolved, discord.Message):
                code = await CodeBlock().convert(ctx, "")
                if code:
                    with_reply_code = True

        if code is None or with_reply_code:
            first_line = ctx.message.content.split("\n")[0]
            if first_line.count("`") >= 2:
                try:
                    first_index = first_line.index("`")

                    if first_line[first_index + 1] == "`":
                        first_index += 1

                    second_index = first_line.index("`", first_index + 1)
                except Exception:
                    return await ctx.reply("""
Missing code block. Please use the following markdown:
`` `code here` ``
or
```ansi
`\x1b[0m`\x1b[0m`swift
code here
`\x1b[0m`\x1b[0m`
```""")

                print_code = f"import Foundation\nprint({first_line[first_index+1:second_index]})"
                
                if with_reply_code:
                    code += "\n" + print_code
                else:
                    code = print_code
            elif with_reply_code:
                pass
            else:
                return await ctx.reply("""
Missing code block. Please use the following markdown:
`` `code here` ``
or
```ansi
`\x1b[0m`\x1b[0m`swift
code here
`\x1b[0m`\x1b[0m`
```""")

        message = await ctx.reply("*Running code on playground...*")

        try:
            resp = await self.bot.jdoodle.execute(script=code)
        except asyncio.TimeoutError:
            return await message.edit(
                content="The operation timed out, took too long to retrieve output from playground..."
            )

        if resp is None:
            return await message.edit(content="Oops! Unexpected internal error.")

        content: str = resp["output"]

        if not content and resp["isExecutionSuccess"]:
            return await message.edit(content="Compilation was successful.")

        if resp["isExecutionSuccess"]:
            if 20 < len(content.splitlines()) < 30:
                content = "\n".join(content.splitlines()[0:20]) + "\n..."
            elif 30 <= len(content.splitlines()):
                content = content = "\n".join(content.splitlines()[0:10]) + "\n..."

        if not resp["isExecutionSuccess"]:
            content = content.replace("error: fatalError\n\n", "")
            content = content.replace("jdoodle.", "")
            if len(content) > 4000:
                content = content[3997] + "..."

        if content:
            if "timeout" in content.lower() and "jdoodle" in content.lower():
                return await message.edit(
                    content="The operation timed out, evaluation took too long..."
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
