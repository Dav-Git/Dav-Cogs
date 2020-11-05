import asyncio
from collections import defaultdict
from datetime import timedelta
from typing import Optional, List

import discord
from aiohttp import ClientSession
from redbot.core import commands, modlog
from redbot.core.i18n import cog_i18n, Translator

_ = Translator("ModLogStats", __file__)
UPDATE_DELAY = 0.3


@cog_i18n(_)
class ModLogStats(commands.Cog):
    def __init__(self):
        self.tasks = {}
        self.webhooks = defaultdict(lambda: None)

    def cog_unload(self):
        for guild_id in self.tasks:
            self.tasks[guild_id].cancel()
        for guild_id in self.webhooks:
            asyncio.create_task(self.webhooks[guild_id].delete(reason="Cog unload."))

    def red_delete_data_for_user(self, *, requester, user_id):
        return  # This cog stores no EUD

    @commands.bot_has_permissions(manage_webhooks=True)
    @commands.max_concurrency(1, commands.BucketType.guild, wait=False)
    @commands.command()
    async def modlogstats(self, ctx, *, time: Optional[commands.TimedeltaConverter] = None):
        """Get modlog stats for the timeframe specified."""
        message_id = await self._initialize_webhook_message(ctx.channel)
        self.tasks[ctx.guild.id] = asyncio.create_task(
            self._send_getting_cases_message(ctx.channel, message_id)
        )
        cases = await modlog.get_all_cases(ctx.guild, ctx.bot)
        self.tasks[ctx.guild.id].cancel()
        self.tasks[ctx.guild.id] = asyncio.create_task(
            self._send_processing_cases(ctx.channel, message_id, len(cases))
        )
        counts = defaultdict(int)
        min_date = 0
        for case in cases:
            if case.created_at > min_date:
                counts[case.action_type] = counts[case.action_type] + 1
        self.tasks[ctx.guild.id].cancel()
        em = discord.Embed(title="Results", description=counts)
        em.color = discord.Color.green()
        await self._edit_webhook_message_embeds(self.webhooks[ctx.guild.id].url, message_id, [em])

    async def _maybe_create_webhook(self, channel):
        if not self.webhooks[channel.guild.id]:
            self.webhooks[channel.guild.id] = await channel.create_webhook(
                name=_("Modlogstats"), reason=_("Modlogstats status message.")
            )

    async def _initialize_webhook_message(self, channel):
        await self._maybe_create_webhook(channel)
        em = discord.Embed(title="\u400b")
        message = await self.webhooks[channel.guild.id].send(embed=em)
        if not message:
            async for message in channel.history(limit=15, oldest_first=False):
                if message.author.id == self.webhooks[channel.guild.id].id:
                    message_id = message.id
                    break
        else:
            message_id = message.id
        return message_id

    async def _edit_webhook_message_embeds(self, url, message_id, embeds: List[discord.Embed]):
        async with ClientSession() as session:
            async with session.patch(
                f"{url}/messages/{message_id}",
                headers={"Content-Type": "application/json"},
                json={"embeds": [embed.to_dict() for embed in embeds]},
            ):
                pass

    async def _send_getting_cases_message(self, channel, message_id):
        url = self.webhooks[channel.guild.id].url
        em = discord.Embed()
        em.set_footer(text=_("This WILL take a while."))
        while True:
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Getting cases.")
            em.color = discord.Color(0xFFFF66)
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Getting cases..")
            em.color = discord.Color(0x000000)
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Getting cases...")
            em.color = discord.Color(0xFFFF66)
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Getting cases")
            em.color = discord.Color(0x000000)
            await self._edit_webhook_message_embeds(url, message_id, [em])

    async def _send_processing_cases(self, channel, message_id, amount_of_cases: int):
        url = self.webhooks[channel.guild.id].url
        em = discord.Embed()
        em.set_footer(text=_("This might take a while."))
        while True:
            em.title = _("Processing {cases} cases").format(cases=amount_of_cases)
            em.color = discord.Color.dark_green()
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Processing {cases} cases.").format(cases=amount_of_cases)
            em.color = discord.Color(0x000000)
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Processing {cases} cases..").format(cases=amount_of_cases)
            em.color = discord.Color.dark_green()
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)
            em.title = _("Processing {cases} cases...").format(cases=amount_of_cases)
            em.color = discord.Color(0x000000)
            await self._edit_webhook_message_embeds(url, message_id, [em])
            await asyncio.sleep(UPDATE_DELAY)