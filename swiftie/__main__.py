import asyncio
import contextlib
import logging
from logging.handlers import RotatingFileHandler

import discord


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
    from .bot import Swiftie
    from .jdoodle import JDoodleClient

    discord.VoiceClient.warn_nacl = False

    async with JDoodleClient() as session:
        async with Swiftie(session) as bot:
            await bot.start()


with setup_logging():
    log = logging.getLogger()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Received exit signal from user, shutting down...")
