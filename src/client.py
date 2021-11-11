from discord.ext import commands
import logging


logger = logging.getLogger("seagull_client")
logger.setLevel("DEBUG")


class SealgullClient(commands.Bot):
    def __init__(self, args):
        super().__init__(command_prefix=args.command_prefix)

    async def on_ready(self):
        """
        When the bot is ready to work on the server
        the function is called
        :return: None
        """
        logger.info("Logged in!")
