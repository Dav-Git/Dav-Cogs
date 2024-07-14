<p align="center">
<a href="https://discord.gg/z6Nhqc5"><img src="https://discordapp.com/api/guilds/552178115175252005/embed.png"></a>
<a href="https://github.com/Rapptz/discord.py"><img src="https://img.shields.io/static/v1?label=Discord&message=py&color=blue&style=flat&logo=discord"></a>
<a href="https://github.com/Cog-Creators/Red-DiscordBot/tree/V3/develop"><img src="https://img.shields.io/static/v1?label=Red-DiscordBot&message=3.5&color=red&style=for-the-badge"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/static/v1?label=Python&message=3.10&color=blue&style=flat&logo=python"></a>
<img src="https://img.shields.io/badge/code%20style-black-000000.svg"></p>
<p align="center"><img src="https://github.com/Dav-Git/Dav-Cogs/workflows/Lint%20Python/badge.svg">
<img src="https://img.shields.io/static/v1?label=PRs&message=Welcome&color=green&style=flat&logo=GitHub">
<img src="https://github.com/Dav-Git/Dav-Cogs/workflows/Black/badge.svg"></p>


# Dav-Cogs

Dav's cogs for Red. If you find a bug or want to request a feature, please [open an issue](https://github.com/Dav-Git/Dav-Cogs/issues/new) on github.

| Cog | Description | 
| --- | ----------- | 
| altmarker | Mark a user's alt accounts as belonging together and get alerted when they join or leave. |
| anonreporter | Anonymous version of the core reports cog. |
| autoroler | Assign roles to users when they join. |
| botstatus | <details><summary>Set a bot status that stays on reboot.</summary>This cog will save your bot status settings (if you use the dedicated command) and apply them on bot startup or reboot.</details> |
| casereader | <details><summary>A different approach to ``[p]casesfor``</summary>For some users it might be inconvenient to have to click through a menu of cases when using the ``[p]casesfor`` command. Casereader sends a list of all cases linked to a user when the ``[p]read`` command is used.</details> |
| caserelayer | Send modlog cases to a user. |
| exclusiveroles | <details><summary>Make roles "truly" exclusive.</summary>Allows you to set 2 roles exclusive to each other. That way, when a user is being assigned a new role, the old role which is exclusive with the new role will be removed.</details> |
| httpcat | Get cute http kitties courtesy of [http.cat](https://http.cat) | 
| joinflag | Put a note on a user which will be displayed when they join your guild. |
| mcwhitelister | <details><summary>Sync a minecraft server whitelist with discord.</summary>Members of your discord can add themselves to the whitelist by running ``[p]whitelister add <minecraft_name>``. When they leave the discord their whitelist is automatically removed. This cog uses Minecraft RCON to communicate with your server.</details> |
| modlogstats | Find out how often each modlog casetype has been used in your modlog. This cog uses multithreading. Use at your own risk. |
| mover | Massmove members from one voicechannel to another. |
| nicknamer | <details><summary>Nicknaming tools.</summary>Allow your moderators to set a predefined nickname quickly, change a user's nickname using a command, freeze a user's nickname or temporarily change it for a predefined amount of time. Every action can also generate a modlog entry.</details> |
| prunecmd | Introduces a command to prune the member list. |
| rolesyncer | Sync roles within a guild |
| roomer | <details><summary>Automatic voicechannel generation and private voice and text channels.</summary><br>- Automated voicechannel creation<br>- Private voicechannels<br><br>- Private textchannels </details> |
| stickymember | <details><summary>Make a member sticky and have them keep all their roles, even when leaving your guild.</summary>Ever had a member leave and rejoin frequently so you had to give them back all their roles? Me neither, but someone else did. So I made this. Any member saved to the cog will retain all their roles when they rejoin the server.</details> |
| verifyer | <details><summary>Add a safety barrier to your discord server and require users to run a command before accessing the server.</summary>Before being able to access your server, users need to run the command ``[p]verify``. You can either achieve this by having a member role and revoking read/write access to all channels for @ everyone or by choosing to deny all permissions to a "Verification role". Members need to be able to type in a channel of your guild to be able to verify themselves. This could be a hidden channel. This cog requires setup with ``[p]verifyerset`` and relies on users having their DMs open for the bot.</details> |

# Installation

To add these cogs to your RedBot, first add the repo by running\
`[p]repo add Dav-cogs https://github.com/Dav-Git/Dav-Cogs`

Then, install the cogs by running `[p]cog install Dav-cogs <name_of_cog>`

And load them with `[p]load <name_of_cog>`

# Support

You can get support in the [#support_othercogs](https://discordapp.com/channels/240154543684321280/240212783503900673) channel on the official [Cog support server](https://discord.gg/GET4DVk)\
Visit my own server for quicker responses: [Dav-Server](https://discord.gg/z6Nhqc5)\
Cogs not listed above will **NOT** work on your bot.\
You can find other approved repos on the [Red Index](https://index.discord.red).

# Contributing

Want to help out with translating or developing these cogs?\
Please check [here](https://github.com/Dav-Git/Dav-Cogs/blob/master/TRANSLATING.md) for translation instructions and [here](https://github.com/Dav-Git/Dav-Cogs/blob/master/CONTRIBUTING.md) for contribution guidelines.
# Credits

Thanks to [Draper](https://github.com/Drapersniper) for helping with exclusiveroles. \
Thanks to [Jack](https://github.com/jack1142) for supplying the code used to pull the ``end_user_data_statement`` into the ``__init__.py``s. \
Also a big thank you to everyone in the coding channel on the support discord for your help along the way. 

# Privacy

Some of my cogs store end user data. \
You can find info on this data by using the ``[p]mydata 3rdparty`` command. \
\
For questions, feel free to contact me as described at the top.
