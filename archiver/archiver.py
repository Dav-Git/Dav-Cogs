from redbot.core import commands, Config
from .converter import StorageTypeConverter
from typing import Optional
from redbot.core.i18n import cog_i18n, Translator

_ = Translator("Archiver", __file__)


@cog_i18n(_)
class Archiver(commands.Cog):
    def red_delete_data_for_user(self, *, requester, user_id):
        return

    def __init__(self):
        self.config = Config.get_conf(self, 141120200025, force_registration=True)
        self.config.register_guild(default_storage_type="TXT", storage_location=None)

    @commands.command()
    async def archive(
        self, ctx, storage_type: Optional[StorageTypeConverter], messages: Optional[int] = None
    ):
        print("Command trigered")
        if not messages or messages > 100:
            await ctx.send(_("This might take a while."))
        if not storage_type:
            storage_type = await self.config.guild(ctx.guild).default_storage_type()
            print(storage_type)
        if storage_type == "JSON":
            file = await self._archive_txt(ctx.channel, messages)
        elif storage_type == "TXT":
            print("Storage type recognized.")
            await self._archive_json(ctx.channel, messages)
        else:
            await ctx.send(_("Something went wrong."))

    async def _archive_txt(self, channel, messages):
        print("Entered function")
        file = open("C:\\Users\\david\\Documents\\messages.txt", "w+")
        print("File opened")
        async with channel.typing():
            async for message in channel.history(limit=messages):
                print("writing message")
                file.write(f"{message.author.display_name}: {message.content}\n")

        file.close()
        print("File closed")

    async def _archive_json(self, channel, messages):
        pass