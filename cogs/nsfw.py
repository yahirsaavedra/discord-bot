from discord.ext import commands

from bot import CENSURADO
from core.nsfw_core import *
from scripts.checks import is_nsfw, no_badword


class Nsfw:
    """
    NSFW cog
    """
    __slots__ = ['bot']

    def __init__(self, bot: CENSURADO):
        """
        Initialize the Nsfw class
        :param bot: the discord bot object
        """
        self.bot = bot

    async def __process_search(self, ctx, site: str, query: tuple):
        """
        Process a search request.
        :param ctx: the discord context.
        :param site: the site name.
        :param query: the search quries.
        """
        localize = self.bot.localize(ctx)
        if len(query) > 2 and site == 'danbooru':
            await self.bot.say(localize['two_term'])
            return
        dan = self.bot.config['API keys']['danbooru']
        res, tags = await get_lewd(
            self.bot.session_manager,
            site, query, localize,
            self.bot.tag_matcher,
            str(dan['username']),
            str(dan['key'])
        )
        await self.bot.say(res)
        if tags:
            await self.bot.tag_matcher.add_tags(site, tags)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.check(no_badword)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def danbooru(self, ctx, *query: str):
        """
        Danbooru search command
        :param ctx: the discord context
        :param query: the sarch queries
        """
        await self.__process_search(ctx, 'danbooru', query)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.check(no_badword)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def konachan(self, ctx, *query: str):
        await self.__process_search(ctx, 'konachan', query)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.check(no_badword)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def yandere(self, ctx, *query: str):
        """
        Yandere search command
        :param ctx: the discord context
        :param query: the sarch queries
        """
        await self.__process_search(ctx, 'yandere', query)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.check(no_badword)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def gelbooru(self, ctx, *query: str):
        """
        Gelbooru search command
        :param ctx: the discord context
        :param query: the sarch queries
        """
        await self.__process_search(ctx, 'gelbooru', query)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.check(no_badword)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def e621(self, ctx, *query: str):
        """
       e621 search command
       :param ctx: the discord context
       :param query: the sarch queries
       """
        await self.__process_search(ctx, 'e621', query)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.check(no_badword)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def rule34(self, ctx, *query: str):
        """
       rule34 search command
       :param ctx: the discord context
       :param query: the sarch queries
       """
        await self.__process_search(ctx, 'rule34', query)

    @commands.command(pass_context=True)
    @commands.check(is_nsfw)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.server)
    async def greenteaneko(self, ctx):
        """
        Find a random greenteaneko comic
        :param ctx: the discord context
        """
        res = await greenteaneko(
            self.bot.localize(ctx), self.bot.session_manager)
        await self.bot.say(res)
