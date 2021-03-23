from redbot.core import commands


class HttpCat(commands.Cog):
    async def red_delete_data_for_user(self, *, requester, user_id):
        return  # This Cog does not store EUD

    @commands.command()
    async def http(self, ctx, code: int):
        """Get info on HTTP status codes."""
        await ctx.send(f"http://http.cat/{code}")