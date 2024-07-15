import logging

import discord
from discord.ext import commands

from .jdoodle import JDoodleClient

log = logging.getLogger(__name__)

initial_extensions = ("cogs.events", "cogs.misc", "cogs.eval")


class Swiftie(commands.Bot):
    def __init__(self, session: JDoodleClient):
        from . import config

        allowed_mentions = discord.AllowedMentions(
            roles=False,
            everyone=False,
            users=True,
        )
        intents = discord.Intents(
            messages=True,
            message_content=True,
            guilds=True,
        )
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX),
            allowed_mentions=allowed_mentions,
            intents=intents,
        )

        self.jdoodle = session

    async def setup_hook(self) -> None:
        for extension in initial_extensions:
            try:
                await self.load_extension(f"swiftie.{extension}")
            except Exception:
                log.exception(f"Failed to load extension '{extension}'")

    async def start(self) -> None:
        from . import config

        await super().start(
            config.TOKEN,
            reconnect=True,
        )
