import discord
from discord.ext import commands


class Help:
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.group(pass_context=True)
    async def help(self, ctx):
        if not ctx.invoked_subcommand:
            embed = discord.Embed(color=0xda4800)
            embed.add_field(name="ServerManager Help Guide", value=":tada: You can see each of the features by doing: **>help <command group>**")
            embed.add_field(name=":tools:| Moderation", value="Type **>help moderation** too see these commands!")
            embed.add_field(name=":speech_left:| General", value="Type **>help general** too see these commands!")
            embed.add_field(name=":signal_strength:| Bot Stats", value="Type **>help botstats** too see these commands!")
            embed.add_field(name=":paperclip:| Triggers", value="Type **>help triggers** too see these commands!")
            embed.add_field(name=":wave:| Welcomer", value="Type **>help welcomer** too see these commands!")
            embed.add_field(name=":spy:| Leaver", value="Type **>help leaver** too see these commands!")
            embed.add_field(name=":tada:| Fun", value="Type **>help fun** too see the commands!", inline=False)
            embed.add_field(name=":wink:| NSFW", value="Type **>help nsfw** too see the commands!")
            await self.client.say(embed=embed)

    @help.command()
    async def moderation(self):
        msg = """
        The Moderation Help Guide: This shows you all of the commands for moderation

        `>kick @User (reason)` - You can kick the user with a reason
        `>ban @User (reason)` - You can ban the user with a reason
        `>softban @User (reason)` - You can softban the user (bans the user then unbans)
        `>warn @User <reasoning>` - You warn the user with reasons
        `>warnings @User` - Shows current warnings, and reasons for them
         `>lock` - Locksdown the channel you are in (@everyone role can't type there)
        `>unlock` - Unlocks the channel you are in (@everyone role can type now)

        More Commands in the future:
        1. Setting your mute role/You can now mute people (coming very soon)
        2. Purge/Clear the chat (coming very very soon)
        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name="Moderation Help Guide", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def general(self):
        msg = """
        General Help Guide: You can now use some fun commnads/general

        ``>animepic`` - Shows you a random anime picture
        ``>coffee`` - Shows you a coffe(thanks to NekoBot)
        ``>lmgtfy`` - Create your own lmgtfy link
       `` >permissions @user <channel>`` - Shows you the current permissions for a user in the channel
        ``>serverinfo`` - Shows you the server info
        ``>urban <word>`` <definition-num> - Shows you the urban definition of a word(in dms)
        ``>userinfo @User`` - Shows the users info
        ``>settings`` - Shows all of the current config settings

        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name="General Help Guide", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def botstats(self):
        msg = """
        Botstats help guide: You can see all of the Bot Stats here

        ``>botinfo`` - Shows all of the info for the bot (only discord's API)
        ``>creds`` - Shows the credits for the other developers
        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name="Botstats Help Guide", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def triggers(self):
        msg = """
        Triggers help guide: You can now create your own triggers!

        ``>trigger add <trigger> <output to trigger>`` - Allows you to make a trigger like this:


        ``
        Me: hi
        ServerManager: Hey there
        ``

        ``>trigger delete <trigger>`` - Deletes the trigger
        ``>trigger list`` - Shows all of the current server triggers
        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name="Triggers Help Guide", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def welcomer(self):
        msg = """
        Welcomer help guide: You can now make your own welcomer messages!

        ``>welcomer message <message>`` - Creates the welcomer message
        ``>welcomer channel <channel>`` - Allows you to set the channel were the message will go

        **VARIABLES**

        {user} - Mentions the user
        {server} - Shows the current server name
        {members} - Shows the current server member count

        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name="Welcomer Help Guide", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def leaver(self):
        msg = """
        Leaver help guide: You can now make your own leaver messages!

        ``>leaver message <message>`` - Creates the leaver message
        ``>leaver channel <channel>`` - Allows you to set the channel were the message will go

        **VARIABLES**

        {user} - Shows the users name like this: ServerManager#4486
        {server} - Shows the current server name
        {members} - Shows the current server member count

        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name="Leaver Help Guide", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def fun(self):
        msg = """
        Fun Guide Help: You can use fun commands!

        ``>dog`` - See a random dog
        ``>cat`` - See a random cat
        ``>cuddle @user`` - Cuddle a User
        ``>kiss @user`` - Kiss a user
        ``>ship @User @User`` - See those two love birds love for eachother
        ``>whowouldwin @User @User`` - Who would win?
        ``>joke`` - Random Jokes
        ``>kannagen <text>`` - Generate Kanna (thanks NekoBot)
        ``>dong @user`` - Measure a users dong :wink:
        ``>meme`` - Random meme generator
        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name=" Fun Guide Help", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

    @help.command()
    async def nsfw(self):
        msg = """
        NSFW help guide: You can use NSFW commands :wink:

        ``>pgif`` - Random porn gif
        ``>4k`` - Random 4k Image
        ``>ass`` - Random Ass Image
        ``>gonewild`` - Gone Wild :wink:
        ``>anal`` - Shows you an anal image or gif

        """
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name=" NSFW Guide Help", icon_url="https://images-ext-1.discordapp.net/external/mmLgh6YyQhJwZ6g-zo-2OcNHi7usqn5DoE_3dzGwI1k/https/cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png")
        embed.description = msg
        await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Help(client))
