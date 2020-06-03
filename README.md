[![support](https://discordapp.com/api/guilds/552178115175252005/embed.png)](https://discord.gg/z6Nhqc5)
[![E-mail](https://img.shields.io/static/v1?label=E-Mail&message=dav@mail.stopdavabuse.de&color=critical&logo=gmail)](mailto:dav@mail.stopdavabuse.de)
[![discord.py](https://img.shields.io/static/v1?label=Discord&message=py&color=blue&style=flat&logo=discord)](https://github.com/Rapptz/discord.py)
[![Red cogs](https://img.shields.io/static/v1?label=Red-DiscordBot&message=Cogs&color=red&style=for-the-badge)](https://github.com/Cog-Creators/Red-DiscordBot/tree/V3/develop)
[![python3.8](https://img.shields.io/static/v1?label=Python&message=3.8.1&color=blue&style=flat&logo=python)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Dav-Cogs

Dav's cogs for Red. If you find a bug or want to request a feature, please [open an issue](https://github.com/Dav-Git/Dav-Cogs/issues/new) on github.

| Cog | Description |
| --- | ----------- |
| bday | <details><summary>Celebrate birthdays with a role and message.</summary>Set a birthday role and assign it to your members using a command. In combination with [Sinbad's scheduler](https://github.com/TrustyJAID/SinbadCogs) you can even automate the removal of the birthday role.</details> |
| botstatus | <details><summary>Set a bot status that stays on reboot.</summary>This cog will save your bot status settings (if you use the dedicated command) and apply them on bot startup or reboot.</details> |
| casereader | <details><summary>A different approach to ``[p]casesfor``</summary>For some users it might be inconvenient to have to click through a menu of cases when using the ``[p]casesfor`` command. Casereader sends a list of all cases linked to a user when the ``[p]read`` command is used.</details> |
| check | <details><summary>Mod-check a user.</summary>The ``[p]check`` command calls the commands ``[p]userinfo``, ``[p]read`` (if [casereader](https://github.com/Dav-Git/Dav-Cogs) is installed), ``[p]warnings`` (if casereader is not installed) and ``[p]listflag`` (if [flag](https://github.com/bobloy/Fox-V3/) is installed).</details> |
| exclusiveroles | <details><summary>Make roles "truly" exclusive.</summary>Allows you to set 2 roles exclusive to each other. That way, when a user is being assigned a new role, the old role which is exclusive with the new role will be removed.</details> |
| forcenick | <details><summary>Forcibly change a user's nickname.</summary>Comes with the option of creating a modlog entry for these changes.</details> |
| mcwhitelister | <details><summary>Sync a minecraft server whitelist with discord.</summary>Members of your discord can add themselves to the whitelist by running ``[p]whitelister add <minecraft_name>``. When they leave the discord their whitelist is automatically removed. Make sure that you add a ``/`` or ``\`` (depending on your OS) to the end of the path to your minecraft server.</details> |
| prunecmd | Introduces a command to prune the member list. |
| supporter | <details><summary>A more advanced version of Ticketer.</summary>Allows for the creation of multiple support departments and asks the user which department should handle their ticket before ticket creation.<br>For most users Ticketer will be the better and easier option. |
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
| mcwhitelister | Unique discord user-id, minecraft username, minecraft UUID | <details><summary>This info is stored to provide basic cog functionality.</summary><br/> Discord-ID: This info is stored to be able to remove a user's whitelist when they leave the discord server.<br/>Minecraft username: This info is stored to be able to provide a list of currently whitelisted users.<br/>Minecraft UUID: This info is stored to add and remove the user from the minecraft server's whitelist file.</details> |

For questions, feel free to contact me on discord.
