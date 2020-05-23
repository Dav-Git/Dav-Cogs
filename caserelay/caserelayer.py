from redbot.core import modlog, commands, checks
import discord


class CaseRelayer(commands.Cog):
    """CaseRelayer"""

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def relay(self, ctx, case_no: int, user: discord.Member):
        try:
            case = await modlog.get_case(case_no, ctx.guild, self.bot)
        except RuntimeError:
            await ctx.send("That case does not exist for that server.")
            return
        embed = await case.message_content(embed=True)
        await embed.remove_field(1)
        try:
            await user.send(embed=embed)
            await ctx.send(embed=embed)
            await ctx.send(f"Case has been relayed to {user.name}#{user.discriminator}.")
        except:
            await ctx.send("Something went wrong.")
