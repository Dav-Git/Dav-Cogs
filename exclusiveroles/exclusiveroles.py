import discord
from redbot.core import commands, checks, Config

class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2005200611566)
        default_guild = {"exclusives": []}
        self.config.register_guild(**default_guild)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            roles = await self.config.guild(after.guild).exclusives()
            for r in roles:
                if r[1] in after.roles:
                    if r[0] in after.roles:
                        try:
                            await after.remove_roles(r[1], reason="{} overwrites {}".format(r[0].name,r[1].name))
                        except:
                            raise Exception("Role not on user")
                        
    @commands.command()
    @checks.admin()
    async def exclusivenow(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. Removes the second role if both roles are present on a user. """
        
        if not isinstance(role1, discord.Role) or not isinstance(role2, discord.Role) :
            return await ctx.send("You need to provide at least 2 roles")
        
        else:
            await ctx.send("\n`Started...`\n")
            for user in ctx.guild.members:
                if role1 in user.roles:
                    if role2 in user.roles:
                        await user.remove_roles(role2)
            await ctx.send("\n`Completed.`\n")

    @commands.command()
    @checks.admin()
    async def setexclusive(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. Removes the second role if the first role is assigned to a user in the future. """
        
        async with self.config.guild(ctx.guild).exclusives() as conf:
            conf.append((role1.id, role2.id))
        await ctx.send("{} will now be overwritten by {}".format(role2.name, role1.name))
    
    @commands.command()
    @checks.admin()
    async def unexclusive(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 roles and removes their exclusivity"""
        
        async with self.config.guild(ctx.guild).exclusives() as conf:
            if (role1.id, role2.id) in conf:
                try:
                    conf.remove((role1.id, role2.id))
                    await ctx.send("{} will no longer be overwritten by {}".format(role2.name, role1.name))
                except:
                    await ctx.send("```An Error occured```")
            else:
                await ctx.send("{} and {} are not registered as exclusive roles".format(role1.name, role2.name))
    
    @commands.command()
    @checks.admin()
    async def listexclusives(self, ctx):
        """List all exclusive roles"""
        
        roles = await self.config.guild(ctx.guild).exclusives()
        embed = discord.Embed(title="Exclusivroles")
        text = ""
        if roles == []:
            text = "No exclusive roles set"
        else:
            mentions = []
            for r in roles:
                mentions.append("\n{} overwrites {}".format(
                ctx.guild.get_role(r[0]).mention,
                ctx.guild.get_role(r[1]).mention,
                ))
            text = '\n'.join(mentions)
        embed.add_field(name="All exclusive role pairs:", value=text)
        await ctx.send(embed=embed)
    
    @commands.command()
    @checks.admin()
    async def retroscan(self, ctx):
        """Scans the entire user list for roles that have been set as exclusive."""
        
        async with ctx.channel.typing():
            await ctx.send("``This may take a while...``")
            roles = await self.config.guild(ctx.guild).exclusives()
            for r in roles:
                r_new=(ctx.guild.get_role(r[0]), ctx.guild.get_role(r[1]))
                await ctx.send("``Starting with {} and {}``".format(r_new[0].name, r_new[1].name))
                for u in ctx.guild.members:
                    if r_new[0] in u.roles:
                        if r_new[1] in u.roles:
                            await u.remove_roles(r_new[1], reason="{} overwrites {}".format(r_new[0].name,r_new[1].name))
        await ctx.send("``Retroscan completed.``")
