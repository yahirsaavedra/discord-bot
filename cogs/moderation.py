from discord import Member
from discord.ext import commands

from bot import CENSURADO
from core.moderation_core import ban_kick, clean_msg, mute_unmute, warn_pardon
from data_controller.data_utils import get_modlog, get_prefix
from scripts.checks import has_manage_message, has_manage_role, is_admin


class Moderation:
    """
    The cog for Moderation commands
    """
    __slots__ = ['bot']

    def __init__(self, bot: CENSURADO):
        """
        Initialize the Moderation class
        :param bot: the bot
        """
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(is_admin)
    async def ban(self, ctx, member: Member, *args):
        """
        Throw down the ban hammer on someone
        :param ctx: the discord context
        :param member: the discord member
        :param args: if args[0] is an interger it will be resolved as
        delete_message_days, else delete_message_days will be 0
        """
        localize = self.bot.localize(ctx)
        bad_num_msg = localize['delete_message_days']
        no_reason = localize['pls_provide_reason']
        try:
            delete_message_days = int(args[0])
            args = args[1:]
        except ValueError:
            delete_message_days = 0
        except IndexError:
            await self.bot.say(no_reason)
            return
        if not args:
            await self.bot.say(no_reason)
        else:
            reason = ' '.join(args)
            if 0 <= delete_message_days <= 7:
                await ban_kick(
                    self.bot, ctx, member, reason, True, delete_message_days
                )
            else:
                await self.bot.say(bad_num_msg)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(is_admin)
    async def kick(self, ctx, member: Member, *reason):
        """
        Kick a member from the server
        :param ctx: the discord context object
        :param member: the member to be kicked
        :param reason: the kick reason
        """
        if not reason:
            localize = self.bot.localize(ctx)
            await self.bot.say(localize['pls_provide_reason'])
        else:
            await ban_kick(self.bot, ctx, member, ' '.join(reason), False)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(has_manage_message)
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.server)
    async def clean(self, ctx, number=None):
        """
        Clean amount between 1-99 of messages from the current channel
        :param ctx: the discord context object
        :param number: the amount of messages to be deleted
        """
        localize = self.bot.localize(ctx)
        bad_num_msg = localize['clean_message_bad_num']
        if number is None:
            await self.bot.say(bad_num_msg)
        else:
            try:
                await clean_msg(ctx, self.bot, int(number))
            except ValueError:
                await self.bot.say(bad_num_msg)

    async def __mute(self, ctx, is_mute, member, reason):
        """
        Helper method to mute/unmute a member.
        :param ctx: the context.
        :param is_mute: True to mute, False to unmute.
        :param member: the member.
        :param reason: the reason.
        """
        if not reason:
            localize = self.bot.localize(ctx)
            await self.bot.say(localize['pls_provide_reason'])
        else:
            await mute_unmute(ctx, self.bot, member, is_mute, ' '.join(reason))

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(has_manage_role)
    async def mute(self, ctx, member: Member, *reason):
        """
        Give a member the "Muted" role
        :param ctx: the discord context object
        :param member: the member to be muted
        """
        await self.__mute(ctx, True, member, reason)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(has_manage_role)
    async def unmute(self, ctx, member: Member, *reason):
        """
        Remove the "Muted" role from a member
        :param ctx: the discord context object
        :param member: the member to be unmuted
        """
        await self.__mute(ctx, False, member, reason)

    async def __warn(self, ctx, is_warn, member: Member, reason):
        """
        Helper method to warn/pardon someone.
        :param ctx: the context.
        :param is_warn: True to warn, False to pardon.
        :param member: the member.
        :param reason: the reason.
        """
        if not reason:
            localize = self.bot.localize(ctx)
            await self.bot.say(localize['pls_provide_reason'])
        else:
            await warn_pardon(self.bot, ctx, ' '.join(reason), member, is_warn)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(is_admin)
    async def warn(self, ctx, member: Member, *reason):
        """
        Warn someone
        :param ctx: the discord context object
        :param member: the member to be warned
        :param reason: the warn reason
        """
        await self.__warn(ctx, True, member, reason)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(is_admin)
    async def pardon(self, ctx, member: Member, *reason):
        """
        Warn someone
        :param ctx: the discord context object
        :param member: the member to be warned
        :param reason: the warn reason
        """
        await self.__warn(ctx, False, member, reason)

    @commands.group(pass_context=True, no_pm=True)
    @commands.check(is_admin)
    async def modlog(self, ctx):
        """
        Command group for modlog, if no sub command is invoked,
        the bot will display a generic message stating the list of modlogs
        :param ctx: the discord context
        """
        if ctx.invoked_subcommand is None:
            localize = self.bot.localize(ctx)
            modlog = await get_modlog(self.bot.data_manager, ctx.message.server)
            if modlog:
                await self.bot.say(
                    localize['mod_log_channel'].format(modlog.name))
            else:
                await self.bot.say(localize['mod_log_empty'])
            await self.bot.say(localize['mod_log_info'].format(
                get_prefix(self.bot, ctx.message)))

    async def __modify_modlog(self, ctx, is_set):
        """
        Helper method to set/remove the modlog.
        :param ctx: the discord context.
        :param is_set: True to set, False to remove
        """
        # FIXME Remove casting when library rewrite is finished
        localize = self.bot.localize(ctx)
        guild_id = int(ctx.message.server.id)
        channel = ctx.message.channel
        channel_id = int(channel.id)
        if is_set:
            await self.bot.data_manager.set_mod_log(guild_id, channel_id)
            key = 'mod_log_set'
        else:
            await self.bot.data_manager.set_mod_log(guild_id, None)
            key = 'mod_log_rm'
        await self.bot.say(localize[key].format(channel.name))

    @modlog.command(pass_context=True)
    async def set(self, ctx):
        """
        Set the current channel as a mod log channel
        :param ctx: the discord context
        """
        await self.__modify_modlog(ctx, True)

    @modlog.command(pass_context=True)
    async def remove(self, ctx):
        """
        Remove the current channel from mod log channels
        :param ctx: the discord context
        """
        await self.__modify_modlog(ctx, False)
