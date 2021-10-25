import json

from aiomcrcon import Client
from aiomcrcon.errors import IncorrectPasswordError, RCONConnectionError
from discord import Embed
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

_ = Translator("McWhitelister", __file__)


@cog_i18n(_)
class McWhitelister(commands.Cog):
    __version__ = "2.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        data = await self.config.all_guilds()
        for guild_id in data:
            if str(user_id) in data[guild_id]["players"]:
                path = data[guild_id]["path_to_server"]
                with open(path) as json_file:
                    file = json.load(json_file)
                for e in file:
                    if e["uuid"] == data[guild_id]["players"][str(user_id)]["uuid"]:
                        del file[file.index(e)]
                        with open("{}whitelist.json".format(path), "w") as json_file:
                            json.dump(file, json_file, indent=4)
                del data[guild_id]["players"][str(user_id)]
                await self.config.guild_from_id(guild_id).players.set(data[guild_id]["players"])

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=110320200153)
        default_guild = {"players": {}, "path_to_server": "", "rcon": ("localhost", "25575", "")}
        self.config.register_guild(**default_guild)
        self.config.register_global(notification=0)
        self.bot = bot

    async def initialize(self):
        await self.bot.wait_until_red_ready()
        await self._send_pending_owner_notifications(self.bot)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        "Remove member from whitelist when leaving guild"
        p_in_conf = await self.config.guild(member.guild).players()
        host, port, passw = await self.config.guild(member.guild).rcon()
        if str(member.id) in p_in_conf:
            async with Client(host, port, passw) as client:
                await client.send_cmd(
                    "whitelist remove {}".format(p_in_conf[str(member.id)]["name"])
                )
            del p_in_conf[str(member.id)]
            await self.config.guild(member.guild).players.set(p_in_conf)

    @commands.group()
    async def whitelister(self, ctx):
        """MCWhitelister commands"""
        pass

    @commands.guildowner()
    @whitelister.command()
    async def setup(self, ctx, host: str, port: int, *, password: str):
        """Set up MCWhitelister.

        `host`: The IP/URL of your minecraft server.
        `port`: Your server's RCON port. (The default is 25575)
        `password`: The RCON password.
        RCON needs to be enabled and set up in your `server.properties` file.
        More information is available [here](https://minecraft.fandom.com/wiki/Server.properties)"""
        await ctx.message.delete()
        await self.config.guild(ctx.guild).rcon.set((host, port, password))
        try:
            async with Client(host, port, password) as c:
                await c.send_cmd("help")
        except RCONConnectionError:
            await ctx.send(_("Could not connect to server."))
        except IncorrectPasswordError:
            await ctx.send(_("Incorrect password."))
        else:
            await ctx.send(_("Server credentials saved."))

    @whitelister.command(name="add")
    async def hinzufuegen(self, ctx, name: str):
        """Add yourself to the whitelist."""
        p_in_conf = await self.config.guild(ctx.guild).players()
        host, port, passw = await self.config.guild(ctx.guild).rcon()
        p_in_conf[ctx.author.id] = {
            "name": name,
        }
        await self.config.guild(ctx.guild).players.set(p_in_conf)
        async with Client(host, port, passw) as c:
            resp = await c.send_cmd(f"whitelist add {name}", 30)
        await ctx.send(resp[0])

    @commands.admin()
    @whitelister.command()
    async def addmin(self, ctx, name: str):
        """Add someone else to the whitelist manually.\n\nThey will not be removed automatically when leaving the guild."""
        host, port, passw = await self.config.guild(ctx.guild).rcon()
        async with Client(host, port, passw) as c:
            resp = await c.send_cmd(f"whitelist add {name}", 30)
        await ctx.send(resp[0])

    @commands.admin()
    @whitelister.command()
    async def adminremove(self, ctx, name: str):
        """Remove someone else from the whitelist manually.\n\nThis might not be reflected correctly in `[p]whitelister list`."""
        host, port, passw = await self.config.guild(ctx.guild).rcon()
        async with Client(host, port, passw) as c:
            resp = await c.send_cmd(f"whitelist remove {name}", 30)
        await ctx.send(resp[0])

    @whitelister.command()
    async def remove(self, ctx):
        """Remove yourself from the whitelist."""
        p_in_conf = await self.config.guild(ctx.guild).players()
        host, port, passw = await self.config.guild(ctx.guild).rcon()
        if str(ctx.author.id) in p_in_conf:
            async with Client(host, port, passw) as c:
                resp = await c.send_cmd(
                    "whitelist remove {}".format(p_in_conf[str(ctx.author.id)]["name"])
                )
            del p_in_conf[str(ctx.author.id)]
            await self.config.guild(ctx.guild).players.set(p_in_conf)
            await ctx.send(resp[0])
        else:
            await ctx.send(_("You are not whitelisted using MCWhitelister."))

    @commands.admin()
    @whitelister.command(name="list")
    async def liste(self, ctx):
        """See who is whitelisted on your server."""
        host, port, passw = await self.config.guild(ctx.guild).rcon()
        async with Client(host, port, passw) as c:
            resp = await c.send_cmd("whitelist list")
        await ctx.send(resp[0] if len(resp[0]) < 1900 else resp[0][:1900] + "...")
        p_in_config = await self.config.guild(ctx.guild).players()
        outstr = []
        if len(p_in_config) == 0:
            await ctx.send(_("Nobody was whitelisted using whitelister yet."))
            return
        for e in p_in_config:
            outstr.append(
                "{} | {} \n".format(ctx.guild.get_member(int(e)).mention, p_in_config[e]["name"])
            )
        pages = list(pagify("\n".join(outstr), page_length=1024))
        rendered = []
        for page in pages:
            emb = Embed(title=_("Whitelisted with whitelister:"))
            emb.add_field(name=_("Whitelisted"), value=page)
            rendered.append(emb)
        await menu(ctx, rendered, controls=DEFAULT_CONTROLS, timeout=60.0)

    @commands.guildowner()
    @commands.command()
    async def mccommand(self, ctx, *, command):
        """Run a command on the Minecraft server.\n\n**NO VALIDATION is performed on your inputs.**"""
        host, port, passw = await self.config.guild(ctx.guild).rcon()
        async with Client(host, port, passw) as c:
            resp = await c.send_cmd(command)
        await ctx.send(resp[0])

    async def _send_pending_owner_notifications(self, bot):
        if await self.config.notification() == 0:
            await bot.send_to_owners(
                "MCWhitelister: With version 2.0.0 MCWhitelister has migrated to RCON. You will have to **set up your server connection**. More information available with `[p]whitelister setup`."
            )
            await self.config.notification.set(1)
