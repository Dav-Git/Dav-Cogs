from redbot.core import commands, Config
from .converter import StorageTypeConverter
from typing import Optional


class Archiver(commands.Cog):
    def red_delete_data_for_user(self, *, requester, user_id):
        return

    def __init__(self):
        self.config = Config.get_conf(self, 141120200025, force_registration=True)
        self.config.register_guild(default_storage_type="TXT", storage_location=None)

    @commands.command()
    async def archive(self, ctx, messages: int, storage_type: Optional[StorageTypeConverter]):
        if not storage_type:
            storage_type = await self.config.guild(ctx.guild).default_storage_type()
        if storage_type == "JSON":
            file = await self._archive_txt(ctx.channel, messages)
        elif storage_type == "TXT":
            file = await self._archive_json(ctx.channel, messages)
        else:
            await ctx.send("Something went wrong.")