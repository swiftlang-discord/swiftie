import logging
import os

from dotenv import load_dotenv

log = logging.getLogger(__name__)

load_dotenv()

PREFIX = os.getenv("BOT_PREFIX") or "!"
TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
JDOODLE_ID = os.getenv("JDOODLE_ID")
JDOODLE_SECRET = os.getenv("JDOODLE_SECRET")

if TOKEN is None:
    log.exception("Couldn't find variable 'BOT_TOKEN' in the environment.")

if GUILD_ID is None:
    log.exception("Couldn't the variable 'GUILD_ID' in the environment.")

if TOKEN is None or GUILD_ID is None:
    exit(1)

if JDOODLE_SECRET is None or JDOODLE_ID is None:
    log.warn(
        "No environment variables found for 'JDOODLE_ID' and 'JDOODLE_SECRET', the 'swiftie.cogs.eval' extension relies on their API service."
    )

JDOODLE_EXECUTE_ENDPOINT = "https://api.jdoodle.com/v1/execute"
JDOODLE_POST_PAYLOAD = {
    "clientId": JDOODLE_ID,
    "clientSecret": JDOODLE_SECRET,
    "language": "swift",
    "versionIndex": 5,
}
