from praw import *
from discord import Embed
from redbot.core import commands, checks, Config


class Redditor(commands.Cog):
    """Redditor cog"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=13061977, force_registration=True)
        default_global = {
            "client_id": None,
            "client_secret": None,
            "user_agent": "Red-DiscordBot:redditor_cog:v0.1",
        }
        self.config.register_global(**default_global)

    @commands.group()
    @checks.is_owner()
    async def setreddit(self, ctx):
        """Set up your reddit cog."""
        pass

    @setreddit.command()
    async def id(self, ctx, client_id: str):
        """Set your application's client ID"""

        await self.config.client_id.set(client_id)
        await ctx.send("Client ID set.")

    @setreddit.command()
    async def secret(self, ctx, client_secret: str):
        """Set your application's client secret."""

        await self.config.client_secret.set(client_secret)
        await ctx.send("Client secret set.")

    @setreddit.command()
    async def help(self, ctx):
        """See how to set your reddit cog up."""

        step_one = "First, go to https://www.reddit.com/prefs/apps."
        step_one_two = "Create a ``script`` application."
        step_two = "You can set the ``redirect uri`` to ``https://localhost``."
        step_three = "Copy your client ID and run ``[p]redditset id <client_id>``."
        step_four = "Copy your client secret and run ``[p]redditset secret <client_secret>``."
        step_six = "Enjoy."
        e = Embed(title="Redditor setup instructions")
        e.add_field(name="1", value=step_one)
        e.add_field(name="2", value=step_one_two)
        e.add_field(name="3", value=step_two)
        e.add_field(name="4", value=step_three)
        e.add_field(name="5", value=step_four)
        e.add_field(name="6", value=step_six)
        await ctx.send(embed=e)
