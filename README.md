# Swiftie

Discord bot for The Swift Programming Language community.

---

### Setting up the project

#### Setup project dependencies
1. Make sure you have [python 3.12](https://www.python.org/downloads/) installed.
    - macOS: ``brew install python``
2. Install [poetry](https://python-poetry.org).
    - macOS: ``brew install poetry``
3. Install the project's dependencies.
    - ``poetry install``

#### Setup a test server
Create a Discord server for you to test the bot.

#### Setup a bot account
You will need your own bot account on Discord to test your changes to the bot. See [here](https://discordpy.readthedocs.io/en/stable/discord.html) for help with setting up a bot account. Once you have a bot account, invite it to the test server you created in the previous section.

Make sure you enable ``Message Content Intent``and ``Server Member Intent`` in the Privileged Gateway Intents section of your bot page at the developer portal.

#### Configure the bot

Create a ``.env`` file in the project root with the below content:
```
BOT_TOKEN=YourDiscordBotTokenHere
BOT_PREFIX=YourDesiredPrefixHere
GUILD_ID=YourDiscordTestServerIdHere
```
See [here](https://discordpy.readthedocs.io/en/latest/discord.html) for help obtaining the bot token, and for obtaining the guild ID you need to:
- Go to your discord user ``Settings`` -> ``Advanced`` and enable ``Developer Mode``.
- Right click the icon of your test server, and select ``Copy Server ID`` at the bottom.

---

#### Running the project
Use the ``start`` poetry task to run the python project:
- ``poetry run task start``
