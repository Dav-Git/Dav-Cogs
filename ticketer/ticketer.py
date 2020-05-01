import discord
from typing import Optional
from datetime import datetime
from redbot.core import commands, checks, Config


class Ticketer(commands.Cog):
    """Ticketer"""

    def __init__(self):
        self.config = Config.get_conf(self, 200730042020, force_registration=True)
        default_guild = {
            "channel": None,
            "use_counter": False,
            "closed_category": None,
            "open_category": None,
            "current_ticket": 0,
            "role": None,
            "message": "Your ticket has been created. You can add information by typing in this channel. \n\nA member of the ticket-handling-team will be with you as soon as they can.",
            "active": [],
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    @checks.admin()
    async def ticketer(self, ctx):
        """All ticketer settings."""
        pass

    @ticketer.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the ticket-management channel."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Channel has been set to {channel.mention}.")

    @ticketer.command()
    async def role(self, ctx, role: discord.Role):
        """Set the role for ticket managers."""
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Ticket manager role has been set to {role.mention}.")

    @ticketer.group()
    async def category(self, ctx):
        """Set the categories for open and closed tickets."""

    @category.group()
    async def open(self, ctx, category: discord.CategoryChannel):
        """Set the category for open tickets."""
        await self.config.guild(ctx.guild).open_category.set(category.id)
        await ctx.send(f"Category for open tickets has been set to {category.mention}")

    @category.group()
    async def closed(self, ctx, category: discord.CategoryChannel):
        """Set the category for open tickets."""
        await self.config.guild(ctx.guild).closed_category.set(category.id)
        await ctx.send(f"Category for closed tickets has been set to {category.mention}")

    @ticketer.command()
    async def message(self, ctx, *, message: str):
        """Set the message that is shown at the start of each ticket channel."""
        await self.config.guild(ctx.guild).message.set(message)
        await ctx.send(f"The message has been set to ``{message}``.")

    @ticketer.command()
    async def counter(self, ctx, true_or_false: bool):
        """Toggle if the ticket channels should be named using a user's name and ID or counting upwards starting at 0."""
        await self.config.guild(ctx.guild).use_counter.set(true_or_false)
        await ctx.send(
            "The counter has been {}.".format("enabled" if true_or_false else "disabled")
        )

    @ticketer.command()
    async def quicksetup(self, ctx):
        settings = await self.config.guild(ctx.guild).all()
        if not settings["role"]:
            role = await ctx.guild.create_role(
                name="Ticketmanagers", hoist=True, mentionable=False, reason="Ticketer quicksetup"
            )
            await self.config.guild(ctx.guild).role.set(role.id)
            await ctx.send("Ticket-manager role created.")
        if not settings["open_category"]:
            category = await ctx.guild.create_category(
                name="Open-tickets", reason="Ticketer quicksetup"
            )
            await self.config.guild(ctx.guild).open_category.set(category.id)
            await ctx.send("Category for open tickets created.")
        if not settings["closed_category"]:
            category = await ctx.guild.create_category(
                name="Closed-tickets", reason="Ticketer quicksetup"
            )
            await self.config.guild(ctx.guild).closed_category.set(category.id)
            await ctx.send("Category for closed tickets created.")
        settings = await self.config.guild(ctx.guild).all()
        if not settings["channel"]:
            await ctx.send("Config queried for channel setup.")
            overwrite = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    embed_links=True,
                    attach_files=True,
                    manage_messages=True,
                ),
            }
            channel = await ctx.guild.create_text_channel(
                "ticket-management",
                overwrites=overwrite,
                category=ctx.guild.get_channel(settings["open_category"]),
                topic="Ticket management channel.",
                reason="Ticketer quicksetup",
            )
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send("Channel for ticket management created.")
        await ctx.send("Checking settings...")
        if await self._check_settings(ctx):
            await ctx.send("Quicksetup completed.")
        else:
            await ctx.send("Something went wrong...")

    @commands.group()
    async def ticket(self, ctx):
        """Manage a ticket."""
        pass

    @ticket.command()
    async def create(self, ctx, reason: Optional[str] = f"Ticket created at {datetime.utcnow}"):
        """Create a ticket."""
        if await self._check_settings(ctx):
            settings = await self.config.guild(ctx.guild).all()
            if settings["use_counter"]:
                name = f"ticket-{settings['current_ticket']}"
                await self.config.guild(ctx.guild).current_ticket.set(
                    settings["current_ticket"] + 1
                )
            else:
                name = f"{ctx.author.name}-{ctx.author.id}"
            if not discord.utils.find(lambda m: m.name == name, ctx.guild.channels):
                overwrite = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.author: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                    ),
                    ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                        manage_messages=True,
                    ),
                }
                ticketchannel = await ctx.guild.create_text_channel(
                    name,
                    overwrites=overwrite,
                    category=ctx.guild.get_channel(settings["open_category"]),
                    topic=reason,
                )
                await ticketchannel.send(settings["message"])
                embed = discord.Embed(
                    title=name, description=f"reason", timestamp=datetime.utcnow(),
                ).set_footer(text="Last updated at:")
                message = await ctx.guild.get_channel(settings["channel"]).send(embed=embed)
                async with self.config.guild(ctx.guild).active() as active:
                    active.append((ticketchannel.id, message.id))
            else:
                await ctx.send("You already have an open ticket.")
        else:
            await ctx.send("Please finish the setup process before creating a ticket.")

    async def _check_settings(self, ctx: commands.Context) -> bool:
        settings = await self.config.guild(ctx.guild).all()
        count = 0
        if settings["channel"]:
            count += 1
        else:
            await ctx.send("Management channel not set up yet.")
        if settings["closed_category"]:
            count += 1
        else:
            await ctx.send("Category for closed tickets not set up yet.")
        if settings["open_category"]:
            count += 1
        else:
            await ctx.send("Category for open tickets not set up yet.")
        if settings["role"]:
            count += 1
        else:
            await ctx.send("Ticket manager role not set up yet.")
        if count == 4:
            return True
        else:
            return False
