import logging

from client import SealgullClient
from discord.ext import commands


logger = logging.getLogger(__name__)


class Polls(commands.Cog):
    def __init__(self, bot: SealgullClient, args):
        """
        Cog Polls

        This cog allows users to create polls in the server.
        A poll is a message with a suggestion text and three buttons:
        "Yes", "No", "Skip"

        :param bot: bot client
        :param args: arguments for the bot
        """
        self.bot_ = bot
        self.args = args

        self.emojis = [
            "✅",
            "❌",
            "<:dashkoff:889896793687609354>"
        ]

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, proposition: str):
        await ctx.message.delete()
        message = await ctx.send(
            f"{ctx.author.name} suggested: \n{proposition}"
        )
        for emoji in self.emojis:
            await message.add_reaction(emoji)

    @suggest.error
    async def suggest_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't make a suggestion because of an internal error"
        )


def setup(bot: SealgullClient, args):
    bot.add_cog(Polls(bot, args))
