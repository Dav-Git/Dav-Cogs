from redbot.core import checks, commands
import discord
from typing import Optional


class FKCom(commands.Cog):
    @commands.command()
    @checks.mod()
    async def rp(self, ctx, user: Optional[discord.User]):
        await ctx.send(
            "Hey{}, it seems like you have asked a question about ARP (Aspirant Gaming). We are not affiliated with ARP at all and sadly can not provide any information to you. To receive an answer to your question, try {} or the Aspirant Gaming discord server.".format(
                " " + user.mention if user != None else "\u200b",
                ctx.guild.get_channel(478917077705555970).mention,
            )
        )

