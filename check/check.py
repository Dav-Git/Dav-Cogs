from redbot.core import commands, checks

class Check(commands.Cog):
  """Check"""
  def __init__(self):
    pass
  
  @commands.command()
  @checks.mod()
  async def check(self, ctx, a1):
    ctx.assume_yes = True
    clist = ["userinfo", "names", "warnings"]
    u = ctx.guild.get_member(int(a1))

    for command_name in clist:
        command = ctx.bot.get_command(command_name)
        await ctx.invoke(command, user=u)
    
    await ctx.invoke(ctx.bot.get_command("listflag") ,member=u)