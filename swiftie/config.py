import logging
import os

from dotenv import load_dotenv

log = logging.getLogger(__name__)

load_dotenv()

PREFIX = os.getenv("BOT_PREFIX") or "!"
TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not TOKEN:
    log.exception("Couldn't find variable 'BOT_TOKEN' in the environment.")

if not GUILD_ID:
    log.exception("Couldn't the variable 'GUILD_ID' in the environment.")

if TOKEN is None or GUILD_ID is None:
    exit(1)
