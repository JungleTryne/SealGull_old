import logging

from queue import Queue
from client import SealgullClient
from discord.ext import commands

from ext.dpy_basic_voice import YTDLSource

logger = logging.getLogger(__name__)


class YTPlayer(commands.Cog):
    def __init__(self, bot: SealgullClient, args):
        """
        Cog YTPlayer

        This cog allows users to play youtube music on the server
        :param bot: bot client
        :param args: arguments for the bot
        """
        self.bot_ = bot
        self.args = args

        # TODO: Might me not thread-safe
        self.current_player_ = None
        self.songs_queue_ = Queue()

    def update_queue(self, ctx: commands.Context):
        if self.songs_queue_.empty():
            self.current_player_ = None
            return

        player = self.songs_queue_.get()
        self.play_song_(ctx, player)

    def play_song_(self, ctx, player):
        self.current_player_ = player
        ctx.voice_client.play(
            player,
            after=lambda e: print(f'Player error: {e}') if e else self.update_queue(ctx)
        )

    @commands.command()
    async def join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        await channel.connect()

    @join.error
    async def join_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't join a channel because of an internal error"
        )

    @commands.command()
    async def leave(self, ctx: commands.Context):
        await self.clear(ctx)
        await ctx.voice_client.disconnect()

    @leave.error
    async def leave_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't leave a channel because of an internal error"
        )

    @commands.command()
    async def play(self, ctx: commands.Context, link: str):
        """Streams from a url (same as yt, but doesn't predownload)"""

        if not ctx.voice_client:
            await self.join(ctx)

        async with ctx.typing():
            player = await YTDLSource.from_url(link, loop=self.bot_.loop, stream=True)

            if self.songs_queue_.empty() and not self.current_player_:
                self.play_song_(ctx, player)
                await ctx.send(f'Now playing: {player.title}')
            else:
                self.songs_queue_.put(player)
                await ctx.send(f'Added {player.title} to queue')

    @play.error
    async def play_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't play a video because of an internal error"
        )

    @commands.command()
    async def pause(self, ctx: commands.Context):
        ctx.voice_client.pause()
        await ctx.send("Pause")

    @pause.error
    async def pause_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't pause because of an internal error"
        )

    @commands.command()
    async def resume(self, ctx: commands.Context):
        ctx.voice_client.resume()
        await ctx.send("Resume")

    @resume.error
    async def resume_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't resume because of an internal error"
        )

    @commands.command()
    async def volume(self, ctx: commands.Context, *, volume: int):
        if not ctx.voice_client.is_playing():
            return await ctx.send("Nothing being played at the moment")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume} %")

    @volume.error
    async def volume_handler(self, ctx: commands.Context, what):
        logger.error(what)
        await ctx.send(
            "Couldn't stop because of an internal error"
        )

    @commands.command()
    async def queue(self, ctx: commands.Context):
        if self.current_player_ is None:
            await ctx.send("Music queue is empty")
            return

        queue_lines = ["1) {0}: Currently playing".format(self.current_player_.title)]

        for i, player in enumerate(self.songs_queue_.queue):
            queue_lines.append("{0}) {1}".format(i + 2, player.title))

        await ctx.send("\n".join(queue_lines))

    @commands.command()
    async def skip(self, ctx: commands.Context):
        ctx.voice_client.stop()
        await ctx.send("Skipped")

    @commands.command()
    async def clear(self, ctx:commands.Context):
        while not self.songs_queue_.empty():
            ctx.voice_client.stop()

        if self.current_player_:
            ctx.voice_client.stop()

        await ctx.send("Cleared queue")


def setup(bot: SealgullClient, args):
    bot.add_cog(YTPlayer(bot, args))