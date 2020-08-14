import discord, asyncio
from typing import Optional
from datetime import datetime
from redbot.core import commands, checks, Config, modlog
from redbot.core.utils.predicates import MessagePredicate


class Supporter(commands.Cog):
    """Supporter"""

    def __init__(self, bot):
        self.config = Config.get_conf(self, 124006052020, force_registration=True)
        self.bot = bot
        default_guild = {
            "channel": None,
            "use_counter": False,
            "closed_category": None,
            "open_category": None,
            "current_ticket": 0,
            "role": None,
            "message": "Your ticket has been created. You can add information by typing in this channel. \n\nA member of the ticket-handling-team will be with you as soon as they can.",
            "active": [],
            "modlog": True,
            "dept_msg": "Choose a support department by typing in this channel please.",
            "departments": [],
            "closed": [],
        }
        self.config.register_guild(**default_guild)

    @staticmethod
    async def register_casetypes():
        new_types = [
            {
                "name": "ticket_created",
                "default_setting": True,
                "image": "\N{BALLOT BOX WITH BALLOT}\N{VARIATION SELECTOR-16}",
                "case_str": "Ticket created",
            }
        ]
        await modlog.register_casetypes(new_types)

    @commands.group()
    @checks.admin()
    async def supporter(self, ctx):
        """All supporter settings."""
        pass

    @supporter.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the ticket-management channel."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Channel has been set to {channel.mention}.")

    @supporter.command()
    async def role(self, ctx, role: discord.Role):
        """Set the role for ticket managers."""
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Ticket manager role has been set to {role.mention}.")

    @supporter.group()
    async def category(self, ctx):
        """Set the categories for open and closed tickets."""

    @category.command()
    async def open(self, ctx, category: discord.CategoryChannel):
        """Set the category for open tickets."""
        await self.config.guild(ctx.guild).open_category.set(category.id)
        await ctx.send(f"Category for open tickets has been set to {category.mention}")

    @category.command()
    async def closed(self, ctx, category: discord.CategoryChannel):
        """Set the category for open tickets."""
        await self.config.guild(ctx.guild).closed_category.set(category.id)
        await ctx.send(f"Category for closed tickets has been set to {category.mention}")

    @supporter.command()
    async def message(self, ctx, *, message: str):
        """Set the message that is shown at the start of each ticket channel."""
        await self.config.guild(ctx.guild).message.set(message)
        await ctx.send(f"The message has been set to ``{message}``.")

    @supporter.command()
    async def counter(self, ctx, true_or_false: bool):
        """Toggle if the ticket channels should be named using a user's name and ID or counting upwards starting at 0."""
        await self.config.guild(ctx.guild).use_counter.set(true_or_false)
        await ctx.send(
            "The counter has been {}.".format("enabled" if true_or_false else "disabled")
        )

    @supporter.command()
    async def modlog(self, ctx, true_or_false: bool):
        """Decide if supporter should log to modlog."""
        await self.config.guild(ctx.guild).modlog.set(true_or_false)
        await ctx.send(
            "Logging to modlog has been {}.".format("enabled" if true_or_false else "disabled")
        )

    @supporter.command()
    async def deptmsg(self, ctx, message: str):
        """Set the message that prompts the user to choose a support department."""
        await self.config.guild(ctx.guild).dept_msg.set(message)
        await ctx.send(f"The message has been set to ``{message}``.")

    @supporter.group()
    async def department(self, ctx):
        """Manage support departments."""
        pass

    @department.command(name="add")
    async def dept_add(self, ctx, name: str, role: discord.Role):
        """Add a support department.\n\n Department names get saved in lowercase.\n2 Departments may not have the same name."""
        async with self.config.guild(ctx.guild).departments() as departments:
            departments.append((name.lower(), role.id))
        await ctx.send(f"Department {name} added with role ID: {role.id}")

    @department.command(name="remove")
    async def dept_rem(self, ctx, name: str):
        """Remove a support department."""
        depts = await self.config.guild(ctx.guild).departments()
        for e in depts:
            if name.lower() in e:
                depts.remove(e)
        await ctx.send(f"Removed {name}")

    @department.command(name="list")
    async def dept_list(self, ctx):
        for e in await self.config.guild(ctx.guild).departments():
            await ctx.send("List of available departments:")
            await ctx.send(f"{e[0]}")

    @supporter.command()
    async def quicksetup(self, ctx):
        """Quicksetup is not available in supporter.
        If you want a simple ticket handling system,
        use Ticketer instead."""

    @supporter.command()
    async def purge(self, ctx, are_you_sure: Optional[bool]):
        if are_you_sure:
            async with self.config.guild(ctx.guild).closed() as closed:
                for channel in closed:
                    try:
                        channel_obj = ctx.guild.get_channel(channel)
                        if channel_obj:
                            await channel_obj.delete(reason="Ticket purge")
                        closed.remove(channel)
                    except discord.Forbidden:
                        await ctx.send(
                            f"I could not delete channel ID {channel} because I don't have the required permissions."
                        )
                    except discord.NotFound:
                        closed.remove(channel)
                    except discord.HTTPException:
                        await ctx.send("Something went wrong. Aborting.")
                        return
        else:
            await ctx.send(
                f"This action will permanently delete all closed ticket channels.\nThis action is irreversible.\nConfirm with ``{ctx.clean_prefix}supporter purge true``"
            )

    @commands.group()
    async def ticket(self, ctx):
        """Manage a ticket."""
        pass

    @ticket.command(aliases=["open"])
    async def create(
        self, ctx, *, reason: Optional[str] = "No reason provided.",
    ):
        """Create a ticket."""
        if await self._check_settings(ctx):
            settings = await self.config.guild(ctx.guild).all()
            if settings["use_counter"]:
                name = f"ticket-{ctx.author.name}-{settings['current_ticket']}"
                await self.config.guild(ctx.guild).current_ticket.set(
                    settings["current_ticket"] + 1
                )
            else:
                name = f"{ctx.author.name}-{ctx.author.id}"
            found = False
            for channel in ctx.guild.channels:
                if channel.name == name.lower():
                    found = True
            if not found:
                await ctx.send(settings["dept_msg"], delete_after=60)
                try:
                    dept_msg = await self.bot.wait_for(
                        "message", check=MessagePredicate.same_context(ctx), timeout=60
                    )
                except asyncio.exceptions.TimeoutError:
                    await ctx.send("Response timed out.")
                    return
                dept_role = None
                for e in settings["departments"]:
                    if e[0] == dept_msg.content.lower():
                        dept_role = ctx.guild.get_role(e[1])
                if dept_role:
                    if settings["modlog"]:
                        await modlog.create_case(
                            ctx.bot,
                            ctx.guild,
                            ctx.message.created_at,
                            action_type="ticket_created",
                            user=ctx.author,
                            moderator=ctx.author,
                            reason=f"Department: {dept_msg.content.lower()}",
                        )
                    overwrite = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        ctx.author: discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            embed_links=True,
                            attach_files=True,
                        ),
                        dept_role: discord.PermissionOverwrite(
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
                    await ticketchannel.send(
                        f"This channel is visible to ``{dept_msg.content.lower()}``."
                    )
                    await ticketchannel.send(settings["message"])
                    await ticketchannel.send(
                        f'{ctx.author.name}#{ctx.author.discriminator}:"{reason}"'
                    )
                    embed = discord.Embed(
                        title=name, description=reason, timestamp=datetime.utcnow(),
                    ).set_footer(text="Last updated at:")
                    embed.add_field(name="Department", value=dept_role.mention)
                    message = await ctx.guild.get_channel(settings["channel"]).send(embed=embed)
                    async with self.config.guild(ctx.guild).active() as active:
                        active.append((ticketchannel.id, message.id, dept_role.id))
                    await dept_msg.delete()
                else:
                    await dept_msg.delete()
                    await ctx.send("Invalid department.\nValid options are:", delete_after=20)
                    for e in settings["departments"]:
                        await ctx.send(f"{e[0]}", delete_after=20)
            else:
                await ctx.send("You already have an open ticket.")
        else:
            await ctx.send("Please finish the setup process before creating a ticket.")

    @ticket.command()
    async def close(self, ctx):
        """Close a ticket."""
        settings = await self.config.guild(ctx.guild).all()
        active = settings["active"]
        success = False
        for ticket in active:
            if ctx.channel.id in ticket:
                new_embed = (
                    await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
                ).embeds[0]
                new_embed.add_field(
                    name=datetime.utcnow().strftime("%H:%m UTC"),
                    value=f"Ticket closed by {ctx.author.name}#{ctx.author.discriminator}",
                )
                new_embed.timestamp = datetime.utcnow()
                await (
                    await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
                ).edit(
                    embed=new_embed, delete_after=10,
                )
                await ctx.send(embed=new_embed)
                await ctx.send(
                    "This ticket can no longer be edited using Supporter.", delete_after=30
                )
                dept = ctx.guild.get_role(ticket[2])
                await ctx.channel.edit(
                    category=ctx.guild.get_channel(settings["closed_category"]),
                    name=f"{ctx.channel.name}-c-{datetime.utcnow().strftime('%B-%d-%Y-%H-%m')}",
                    overwrites={
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        dept: discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            embed_links=True,
                            attach_files=True,
                            manage_messages=True,
                        ),
                    },
                )
                await ctx.send("Ticket closed.")
                active.remove(ticket)
                async with self.config.guild(ctx.guild).closed() as closed:
                    closed.append(ticket[0])
                success = True
        if not success:
            await ctx.send("This is not a ticket channel.")
        await self.config.guild(ctx.guild).active.set(active)

    @ticket.command()
    @checks.mod()
    async def update(self, ctx, ticket: Optional[discord.TextChannel] = None, *, update: str):
        """Update a ticket. This is visible to all participants of the ticket."""
        if ticket is None:
            channel = ctx.channel
        else:
            channel = ticket
        settings = await self.config.guild(ctx.guild).all()
        active = settings["active"]
        for ticket in active:
            if channel.id in ticket:
                await channel.edit(
                    topic=f'{channel.topic}\n\n{ctx.author.name}#{ctx.author.discriminator}:"{update}"'
                )
                await ctx.send("Ticket updated.", delete_after=10)
            else:
                ctx.send(f"{channel.mention} is not a ticket channel.")

    @ticket.command()
    @checks.mod()
    async def note(self, ctx, ticket: discord.TextChannel, *, note: str):
        """Add a staff-only note to a ticket."""
        channel = ticket
        for ticket in await self.config.guild(ctx.guild).active():
            if channel.id in ticket:
                message = await ctx.guild.get_channel(
                    await self.config.guild(ctx.guild).channel()
                ).fetch_message(ticket[1])
                new_embed = message.embeds[0]
                new_embed.add_field(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}", value=note
                )
                new_embed.timestamp = datetime.utcnow()
                await message.edit(embed=new_embed)
                await ctx.send("Note added.", delete_after=10)
            else:
                await ctx.send("This is not a ticket channel.")

    @ticket.command()
    @checks.mod()
    async def transfer(
        self, ctx, ticket: Optional[discord.TextChannel] = None, *, department: str
    ):
        """Update a ticket. This is visible to all participants of the ticket."""
        if ticket is None:
            channel = ctx.channel
        else:
            channel = ticket
        department = department.lower()
        new_dept = None
        for ticket in await self.config.guild(ctx.guild).active():
            if channel.id in ticket:
                depts = await self.config.guild(ctx.guild).departments()
                await ctx.send(depts)
                for e in depts:
                    if department in e:
                        await ctx.send("Department found.")
                        new_dept = ctx.guild.get_role(e[1])
            else:
                await ctx.send("This is not a ticket channel.")
                return
        new_overwrites = channel.overwrites
        if new_dept:
            async with self.config.guild(ctx.guild).active() as active:
                count = 0
                for e in active:
                    if channel.id in e:
                        dept = ctx.guild.get_role(e[2])
                        new_overwrites.pop(dept)
                        new_overwrites[new_dept] = discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            embed_links=True,
                            attach_files=True,
                            manage_messages=True,
                        )
                        await channel.edit(overwrites=new_overwrites)
                        msgid = e[1]
                        active[count] = (channel.id, msgid, new_dept.id)
                        message = await ctx.guild.get_channel(
                            await self.config.guild(ctx.guild).channel()
                        ).fetch_message(e[1])
                        embed = message.embeds[0]
                        embed.add_field(
                            name=f"{ctx.author.name}#{ctx.author.discriminator}",
                            value=f"Transfered to {new_dept.mention}",
                        )
                        embed.timestamp = datetime.utcnow()
                        await message.edit(embed=embed)
                    count += 1
        else:
            await ctx.send("Invalid department.\nAvailable options:", delete_after=20)
            for i in depts:
                await ctx.send(f"{i[0]}", delete_after=10)
            return

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
