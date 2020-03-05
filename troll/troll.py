from redbot.core import commands


class Troll(commands.Cog):
    @commands.command()
    async def troll(self, ctx, a: int):
        for i in range(a):
            await ctx.send("LULULULULULULULULULULULULULULULULULULULULULULULULULULU{}".format(i))
