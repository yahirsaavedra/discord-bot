"""
Owner only commands
shard               ✕
shardinfo           ✕
editsettings        ✕
reload              ✕
restart             ✕
shutdown            ✕
blacklist           ✕
"""
from logging import WARN

from discord.ext import commands
from requests import get

from bot import CENSURADO
from core.owner_only_core import handle_eval, setavatar
from data_controller.data_utils import get_prefix
from scripts.checks import is_owner
from scripts.discord_functions import check_message_startwith, clense_prefix
from scripts.helpers import code_block


class OwnerOnly:
    """
    OwnerOnly commands
    """
    __slots__ = ['bot']

    def __init__(self, bot: CENSURADO):
        """
        Initialize the OwnerOnly class
        :param bot: the bot object
        """
        self.bot = bot

    async def on_message(self, message):
        """
        Events for reading messages
        :param message: the message
        """
        prefix = get_prefix(self.bot, message)
        token = str(self.bot.config['Bot']['token'])
        if check_message_startwith(self.bot, message, '{}eval'.format(prefix)):
            localize = self.bot.localize(message)
            # FIXME Remove casting after lib rewrite
            if int(message.author.id) in self.bot.config['Bot']['owners']:
                args = clense_prefix(message, '{}eval'.format(prefix))
                res, success = handle_eval(args)
                str_out = code_block(res, 'Python')
                header = localize['bash_success'] if success else localize[
                    'bash_fail']
                await self.bot.send_message(message.channel, header)
                for s in str_out:
                    s = s.replace(token, localize['lewd_token'])
                    await self.bot.send_message(message.channel, s)
            else:
                await self.bot.send_message(message.channel, localize[
                    'owner_only'])

    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def setavatar(self, ctx, url=None):
        """
        Set avatar of the bot
        :param ctx: the discord context
        :param url: the url to the picture
        """
        localize = self.bot.localize(ctx)
        if url is None:
            await self.bot.say(localize['avatar_fail'])
        else:
            try:
                avatar = get(url).content
                await setavatar(self.bot, localize, ctx.message.channel, avatar)
            except Exception as e:
                self.bot.logger.log(WARN, str(e))
                await self.bot.say(localize['avatar_fail'])

    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def shutdown(self, ctx):
        """
        Shutdown the bot process
        :param ctx: the discord context
        """
        localize = self.bot.localize(ctx)
        await self.bot.say(localize['shutdown'])
        await self.bot.logout()
        exit(0)
