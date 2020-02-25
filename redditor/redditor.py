from praw import *
from discord import Embed
from discord.ext import tasks
from redbot.core import commands, checks, Config
from typing import Optional


class Redditor(commands.Cog):
    """Redditor cog"""

    def __init__(self, bot):
        """Maybe I need a docstring?"""
        self.config = Config.get_conf(self, identifier=13061977, force_registration=True)
        default_global = {
            "client_id": None,
            "client_secret": None,
            "user_agent": "Red-DiscordBot:redditor_cog:v0.2",
        }
        default_guild = {"autoreddit": False, "last": [], "update": {"sub": []}}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)
        self.reddit = None
        self.bot = bot

    async def start(self):
        """I make help not crash by being a helpful string"""
        # getting a reddit instance if credentials are set
        if await self.config.client_id() != None and await self.config.client_secret() != None:
            try:
                self.reddit = Reddit(
                    client_id=await self.config.client_id(),
                    client_secret=await self.config.client_secret(),
                    user_agent=await self.config.user_agent(),
                )
            except:
                pass
            # Also start the background tasks
            self.update_reddit_info.start()

    @tasks.loop(minutes=5)
    async def update_reddit_info(self):
        for guild in self.bot.guilds:
            async with self.config.guild(guild).all() as guild_settings:
                for e in guild_settings["update"]["sub"]:
                    for post in self.reddit.subreddit(e).hot(limit=50):
                        if post.id in await guild_settings["last"]:
                            pass
                        else:
                            guild_settings["last"].append(post.id)
                            embed = Embed(title=f"Hot on r/{e}")
                            embed.add_field(name="Title", value=post.title)
                            embed.add_field(name="Score", value=str(post.score))
                            embed.add_field(name="ID", value=post.id)
                            # Now send embed to channel specified in config

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

    @setreddit.command(name="help")
    async def reddithelp(self, ctx):
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

    @setreddit.group()
    async def autoreddit(self, ctx):
        """Automatically get reddit posts"""
        pass

    @autoreddit.command()
    async def enable(self, ctx):
        """Enable Autoreddit."""
        await self.config.guild.autoreddit().set(True)
        self.update_reddit_info.start()

    @autoreddit.command()
    async def disable(self, ctx):
        """Disable Autoreddit."""
        await self.config.autoreddit().guild.set(False)
        self.update_reddit_info.start()

    @commands.command()
    async def startreddit(self, ctx):
        """Connect to reddit after you have set the credentials."""

        if await self.config.client_id() != None and await self.config.client_secret() != None:
            c_ID = await self.config.client_id()
            c_SECRET = await self.config.client_secret()
            try:
                self.reddit = Reddit(
                    client_id=c_ID,
                    client_secret=c_SECRET,
                    user_agent=await self.config.user_agent(),
                )
            except:
                await ctx.send("An error occured. Try again later.")
        else:
            await ctx.send("You need to provide a ``client ID`` and a ``client secret`` first.")

    @commands.group()
    async def getreddit(self, ctx):
        """Ger some information from reddit."""
        pass

    @getreddit.group()
    async def sub(self, ctx):
        """Get posts from a subreddit."""
        pass

    @sub.command()
    async def hot(self, ctx, query: str, amount: Optional[int] = 10):
        """Get postst ordered by hot."""
        for post in self.reddit.subreddit(query).hot(limit=amount):
            e = Embed(title=f"Hot on r/{query}")
            e.add_field(name="Title", value=post.title)
            e.add_field(name="Score", value=str(post.score))
            e.add_field(name="ID", value=post.id)
            await ctx.send(embed=e)
