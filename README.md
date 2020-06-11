<p align="center">
<a href="https://discord.gg/z6Nhqc5"><img src="https://discordapp.com/api/guilds/552178115175252005/embed.png"></a>
<a href="https://github.com/Rapptz/discord.py"><img src="https://img.shields.io/static/v1?label=Discord&message=py&color=blue&style=flat&logo=discord"></a>
<a href="https://github.com/Cog-Creators/Red-DiscordBot/tree/V3/develop"><img src="https://img.shields.io/static/v1?label=Red-DiscordBot&message=Cogs&color=red&style=for-the-badge"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/static/v1?label=Python&message=3.8.1&color=blue&style=flat&logo=python"></a>
<img src="https://img.shields.io/badge/code%20style-black-000000.svg"></p>
<p align="center"><img src="https://github.com/Dav-Git/Dav-Cogs/workflows/Lint%20Python/badge.svg">
<img src="https://img.shields.io/static/v1?label=PRs&message=Welcome&color=green&style=flat&logo=GitHub">
<img src="https://github.com/Dav-Git/Dav-Cogs/workflows/Black/badge.svg"></p>

# Dav-Cogs

Dav's cogs for Red. If you find a bug or want to request a feature, please [open an issue](https://github.com/Dav-Git/Dav-Cogs/issues/new) on github.

| Cog | Description |
| --- | ----------- |
| bday | <details><summary>Celebrate birthdays with a role and message.</summary>Set a birthday role and assign it to your members using a command. In combination with [Sinbad's scheduler](https://github.com/TrustyJAID/SinbadCogs) you can even automate the removal of the birthday role.</details> |
| botstatus | <details><summary>Set a bot status that stays on reboot.</summary>This cog will save your bot status settings (if you use the dedicated command) and apply them on bot startup or reboot.</details> |
| casereader | <details><summary>A different approach to ``[p]casesfor``</summary>For some users it might be inconvenient to have to click through a menu of cases when using the ``[p]casesfor`` command. Casereader sends a list of all cases linked to a user when the ``[p]read`` command is used.</details> |
| check | <details><summary>Mod-check a user.</summary>The ``[p]check`` command calls the commands ``[p]userinfo``, ``[p]read`` (if [casereader](https://github.com/Dav-Git/Dav-Cogs) is installed), ``[p]warnings`` (if casereader is not installed) and ``[p]listflag`` (if [flag](https://github.com/bobloy/Fox-V3/) is installed).</details> |
| exclusiveroles | <details><summary>Make roles "truly" exclusive.</summary>Allows you to set 2 roles exclusive to each other. That way, when a user is being assigned a new role, the old role which is exclusive with the new role will be removed.</details> |
| mcwhitelister | <details><summary>Sync a minecraft server whitelist with discord.</summary>Members of your discord can add themselves to the whitelist by running ``[p]whitelister add <minecraft_name>``. When they leave the discord their whitelist is automatically removed. Make sure that you add a ``/`` or ``\`` (depending on your OS) to the end of the path to your minecraft server.</details> |
| mover | Massmove members from one voicechannel to another. |
| nicknamer | <details><summary>Nicknaming tools.</summary>Allow your moderators to set a predefined nickname quickly, change a user's nickname using a command, freeze a user's nickname or temporarily change it for a predefined amount of time. Every action can also generate a modlog entry.</details> |
| prunecmd | Introduces a command to prune the member list. |
| supporter | <details><summary>A more advanced version of Ticketer.</summary>Allows for the creation of multiple support departments and asks the user which department should handle their ticket before ticket creation.<br>For most users Ticketer will be the better and easier option.</details> |
| ticketer | A command based ticket system. Run ``[p]ticketer`` and ``[p]ticket`` for help. | 

# Installation

To add these cogs to your RedBot, first add the repo by running\
`[p]repo add Dav-cogs https://github.com/Dav-Git/Dav-Cogs`

Then, install the cogs by running `[p]cog install Dav-cogs <name_of_cog>`

And load them with `[p]load <name_of_cog>`

# Support

Ping me (@Dav) in the [#support_othercogs](https://discordapp.com/channels/240154543684321280/240212783503900673) channel on the official [Cog support server](https://discord.gg/GET4DVk)\
Visit my own server for quicker responses: [Dav-Server](https://discord.gg/z6Nhqc5)\
E-Mail me dav@mail.stopdavabuse.de\
Cogs not listed above will **NOT** work on your bot.\
You can find other approved repos at the [Cogboard](https://cogboard.red/t/approved-repositories/210).

# Credits

Thanks to Draper for helping with exclusiveroles.

Also a big thank you to everyone in the coding channel on the support discord for your help along the way.

# Privacy

Some of my cogs store end user data. In the following list I try to name and explain all these instances of storing end-user data per cog. This list may not necessarily be 100 percent complete. It is designed for transparency reasons, not to give legal advice.

| Cog | Type of data stored | Reason for storing the data |
| --- | ------------------- | --------------------------- |
| botstatus | Custom status text | <details><summary>This info is stored to provide basic cog functionality.</summary><br/>``Custom status text`` : This info is stored so that the set text can be applied as the bot's status message on startup.</details> |
| forcenick | Nickname text | <details><summary>This info is stored to provide basic cog functionality.</summary><br/>``Nickname text`` : This info is stored so that the set nickname can be applied to a user on command usage.</details> |
| mcwhitelister | Discord-UUID<br/>Minecraft-Username<br/>Minecraft-UUID | <details><summary>This info is stored to provide basic cog functionality.</summary><br/> ``Discord-UUID`` : This info is stored to be able to remove a user's whitelist when they leave the discord server.<br/>``Minecraft-Username`` : This info is stored to be able to provide a list of currently whitelisted users.<br/>``Minecraft-UUID`` : This info is stored to add and remove the user from the minecraft server's whitelist file.</details> |

For questions, feel free to contact me on discord.
