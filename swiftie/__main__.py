import asyncio
import contextlib
import logging
import time
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands

from .bot import Swiftie


class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name="discord.state")

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == "WARNING" and "referencing an unknown" in record.msg:
            return False
        return True


@contextlib.contextmanager
def setup_logging():
    log = logging.getLogger()

    try:
        discord.utils.setup_logging()
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.getLogger("discord.state").addFilter(RemoveNoise())

        log.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            filename="swiftie.log",
            encoding="utf-8",
            mode="w",
            maxBytes=max_bytes,
            backupCount=5,
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter(
            "[{asctime}] [{levelname:<7}] {name}: {message}",
            dt_fmt,
            style="{",
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)


async def main():
    discord.VoiceClient.warn_nacl = False

    async with Swiftie() as bot:

        @bot.command(name="ping")
        async def ping(ctx: commands.Context):
            socket = bot.latency * 1000
            response = [
                "Pong! :ping_pong:",
                f"-# ⏲ Socket round-trip took {socket:.2f}ms",
            ]

            start = time.perf_counter()
            message = await ctx.send("\n".join(response))
            end = time.perf_counter()
            duration = (end - start) * 1000

            response[1] += (
                f" and server round-trip took {duration:.2f}ms • [Read more](<https://en.wikipedia.org/wiki/Lag_(video_games)#Ping_time>)"
            )
            await message.edit(content="\n".join(response))

        @bot.listen()
        async def on_command_error(ctx: commands.Context, error: commands.CommandError):
            if not isinstance(error, commands.CommandNotFound):
                raise error

        await bot.start()


with setup_logging():
    log = logging.getLogger()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Received exit signal from user, shutting down...")
