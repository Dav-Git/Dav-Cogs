from redbot.core import commands, checks
import discord

class Check(commands.Cog):
  """Check"""
  def __init__(self):
    pass
  
  @commands.command()
  @checks.mod()
  async def check(self, ctx, user: discord.Member):
    ctx.assume_yes = True
    clist = ["userinfo", "names", "warnings"]
    for command_name in clist:
        command = ctx.bot.get_command(command_name)
        await ctx.invoke(command, user=user)
    try:  
      await ctx.invoke(ctx.bot.get_command("listflag") ,member=user)
    except:
      pass