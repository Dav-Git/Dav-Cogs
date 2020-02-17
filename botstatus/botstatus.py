import discord
import asyncio
from redbot.core import commands, checks, Config


class Botstatus(commands.Cog):
    """Botstatus"""

    def __init__(self, bot):
        self.ready = False
        self.bot = bot
        self.config = Config.get_conf(self, identifier=30052000, force_registration=True)
        standard = {"status": (None, None, None)}
        self.config.register_global(**standard)
        self.ready = True

    def init(self):
        self.start_task = asyncio.create_task(self.fromconf())

    async def setfunc(self, sType, status, text):
        if sType == "game":
            t = discord.ActivityType.playing
        elif sType == "listening":
            t = discord.ActivityType.listening
        elif sType == "watching":
            t = discord.ActivityType.watching
        elif sType == "streaming":
            t = discord.ActivityType.streaming
        else:
            return
        if status == "online":
            s = discord.Status.online
        elif status == "idle":
            s = discord.Status.idle
        elif status == "dnd":
            s = discord.Status.dnd
        elif status == "offline":
            s = discord.Status.offline
        else:
            return
        activity = discord.Activity(name=text, type=t)
        await self.bot.change_presence(status=s, activity=activity)

    async def fromconf(self):
        await self.bot.wait_until_ready()
        value = await self.config.status()
        if value[0] and value[1] and value[2]:
            await self.setfunc(value[0], value[1], value[2])

    @commands.group()
    @checks.is_owner()
    async def botstatus(self, ctx):
        """Set a status that doesn't dissappear on reboot.
            Usage: [p]botstatus <type> <status> <text>"""
        pass

    @botstatus.group()
    async def game(self, ctx):
        """Usage: [p]botstatus game <status> <text>"""
        pass

    @game.command(name="online")
    async def g_online(self, ctx, text: str):
        await self.config.status.set(("game", "online", text))
        await self.setfunc("game", "online", text)
        await ctx.send(f"Status set to ``Online | Playing {text}``")

    @game.command(name="idle")
    async def g_idle(self, ctx, text: str):
        await self.config.status.set(("game", "idle", text))
        await self.setfunc("game", "idle", text)
        await ctx.send(f"Status set to ``Idle | Playing {text}``")

    @game.command(name="dnd")
    async def g_dnd(self, ctx, text: str):
        await self.config.status.set(("game", "dnd", text))
        await self.setfunc("game", "dnd", text)
        await ctx.send(f"Status set to ``DND | Playing {text}``")

    @game.command(name="offline")
    async def g_offline(self, ctx, text: str):
        await self.config.status.set(("game", "offline", text))
        await self.setfunc("game", "offline", text)
        await ctx.send(f"Status set to ``Offline | Playing {text}``")

    @botstatus.group()
    async def listening(self, ctx):
        """Usage: [p]botstatus listening <status> <text>"""
        pass

    @listening.command(name="online")
    async def l_online(self, ctx, text: str):
        await self.config.status.set(("listening", "online", text))
        await self.setfunc("listening", "online", text)
        await ctx.send(f"Status set to ``Online | Listening to {text}``")

    @listening.command(name="idle")
    async def l_idle(self, ctx, text: str):
        await self.config.status.set(("listening", "idle", text))
        await self.setfunc("listening", "idle", text)
        await ctx.send(f"Status set to ``Idle | Listening to {text}``")

    @listening.command(name="dnd")
    async def l_dnd(self, ctx, text: str):
        await self.config.status.set(("listening", "dnd", text))
        await self.setfunc("listening", "dnd", text)
        await ctx.send(f"Status set to ``DND | Listening to {text}``")

    @listening.command(name="offline")
    async def l_offline(self, ctx, text: str):
        await self.config.status.set(("listening", "offline", text))
        await self.setfunc("listening", "offline", text)
        await ctx.send(f"Status set to ``Offline | Listening to {text}``")

    @botstatus.group()
    async def watching(self, ctx):
        """Usage: [p]botstatus watching <status> <text>"""
        pass

    @watching.command(name="online")
    async def w_online(self, ctx, text: str):
        await self.config.status.set(("watching", "online", text))
        await self.setfunc("watching", "online", text)
        await ctx.send(f"Status set to ``Online | Watching {text}``")

    @watching.command(name="idle")
    async def w_idle(self, ctx, text: str):
        await self.config.status.set(("watching", "idle", text))
        await self.setfunc("watching", "idle", text)
        await ctx.send(f"Status set to ``Idle | Watching {text}``")

    @watching.command(name="dnd")
    async def w_dnd(self, ctx, text: str):
        await self.config.status.set(("watching", "dnd", text))
        await self.setfunc("watching", "dnd", text)
        await ctx.send(f"Status set to ``DND | Watching {text}``")

    @watching.command(name="offline")
    async def w_offline(self, ctx, text: str):
        await self.config.status.set(("watching", "offline", text))
        await self.setfunc("watching", "offline", text)
        await ctx.send(f"Status set to ``Offline | Watching {text}``")

    @botstatus.group()
    async def streaming(self, ctx):
        """Usage: [p]botstatus streaming <status> <text>"""
        pass

    @streaming.command(name="online")
    async def s_online(self, ctx, text: str):
        await self.config.status.set(("streaming", "online", text))
        await self.setfunc("streaming", "online", text)
        await ctx.send(f"Status set to ``Online | Streaming {text}``")

    @streaming.command(name="idle")
    async def s_idle(self, ctx, text: str):
        await self.config.status.set(("streaming", "idle", text))
        await self.setfunc("streaming", "idle", text)
        await ctx.send(f"Status set to ``Idle | Streaming {text}``")

    @streaming.command(name="dnd")
    async def s_dnd(self, ctx, text: str):
        await self.config.status.set(("streaming", "dnd", text))
        await self.setfunc("streaming", "dnd", text)
        await ctx.send(f"Status set to ``DND | Streaming {text}``")

    @streaming.command(name="offline")
    async def s_offline(self, ctx, text: str):
        await self.config.status.set(("streaming", "offline", text))
        await self.setfunc("streaming", "offline", text)
        await ctx.send(f"Status set to ``Offline | Streaming {text}``")

    @botstatus.command()
    async def clear(self, ctx):
        """Clear the saved botstatus and disable auto-setting on reboot."""
        await self.config.status.set((None, None, None))
        await ctx.send("Saved botstatus has been cleared.")
