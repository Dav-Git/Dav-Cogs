from redbot.core import commands


class HttpCat(commands.Cog):
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        return  # This Cog does not store EUD

    @commands.command()
    async def http(self, ctx, code: int):
        """Get info on HTTP status codes."""
        await ctx.send(f"http://http.cat/{code}")
