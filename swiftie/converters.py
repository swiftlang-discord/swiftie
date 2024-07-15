from discord.ext import commands


class CodeBlock(commands.Converter):
    async def convert(self, ctx: commands.Context, _: str):
        splat = ctx.message.content.split("\n")
        in_block: bool = False
        lang: str | None = None
        lines: list[str] = []
        blocks: list[dict[str, str]] = []

        for line in splat:
            if in_block and "```" not in line:
                lines.append(line)

            elif not in_block and "```" in line:
                lang = line[line.index("`") :].split()[0].strip("```") or None
                line = line.replace("```", "", 1)

                if "```" in line:
                    data = line.replace("```", "")

                    if data:
                        blocks.append({"language": None, "content": data})

                    lang = None
                    lines = []
                    continue

                in_block = True

            elif in_block and "```" in line:
                if not lines:
                    continue

                joined: str = "\n".join(lines)
                blocks.append({"language": lang, "content": joined})

                lang = None
                lines = []

                in_block = False

        if not blocks:
            return None

        if all([block["language"] is None for block in blocks]) or all(
            [block["language"] == "swift" for block in blocks]
        ):
            code_content = "\n".join([block["content"] for block in blocks])
            return code_content

        return None
