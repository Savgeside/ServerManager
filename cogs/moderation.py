import discord
import json
import asyncio
from discord.ext import commands

class Moderation:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member = None, *, reason = None):
        try:
            author = ctx.message.author
            server = ctx.message.server
            if not author.server_permissions.kick_members:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Kick Members**")
                return
            if user == author:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You can't kick your self.")
                return
            if user is None:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to mention a user!")
                return
            if author.roles < user.roles:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| The user you have mentioned has a higher role rank than you!")
                return
            await self.client.kick(user)
            await self.client.say(f"|<:check:514855967532384256>| Kicked **{user}** for the reason of: *{reason}*")
        except discord.Forbidden:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| I am missing permissions for this command.")
    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            author = ctx.message.author
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| User not found")

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason = None):
        try:
            author = ctx.message.author
            server = ctx.message.server
            if not author.server_permissions.ban_members:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Ban Members**")
                return
            if user == author:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You can't ban your self.")
                return
            if user is None:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to mention a user!")
                return
            if author.roles < user.roles:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| The user you have mentioned has a higher role rank than you!")
                return
            await self.client.ban(user)
            await self.client.say(f"|<:check:514855967532384256>| Banned **{user}** for the reason of: *{reason}*")
        except discord.Forbidden:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| I am missing permissions for this command.")
    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            author = ctx.message.author
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| User not found")

    @commands.command(pass_context=True)
    async def softban(self, ctx, user: discord.Member = None, *, reason = None):
        try:
            author = ctx.message.author
            server = ctx.message.server
            if not author.server_permissions.ban_members:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Ban Members**")
                return
            if user == author:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You can't softban your self.")
                return
            if user is None:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to mention a user!")
                return
            if author.roles < user.roles:
                await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| The user you have mentioned has a higher role rank than you!")
                return
            await self.client.ban(user)
            await self.client.unban(server, user)
            await self.client.say(f"|<:check:514855967532384256>| Softbanned **{user}** for the reason of: *{reason}*")
        except discord.Forbidden:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| I am missing permissions for this command.")
    @softban.error
    async def softban_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            author = ctx.message.author
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| User not found")
    
    @commands.command(pass_context=True)
    async def warn(self, ctx, user: discord.Member = None, *, reason = None):
        with open("user.json", "r") as f:
            warning = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.mute_members:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Mute Members**")
            return
        if not user:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to mention a user!")
            return
        if user == author:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You can't warn your self.")
            return
        if author.roles < user.roles:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| The user you have mentioned has a higher role rank than you!")
            return
        if not server.id in warning:
            warning[server.id] = {}
        if not user.id in warning[server.id]:
            warning[server.id][user.id] = {"warnings": 0}
        if user.id in warning[server.id]:
            warning[server.id][user.id]["warnings"] += 1
            warns = warning[server.id][user.id]["warnings"]
            await self.client.say(f"|<:check:514855967532384256>| Warned **{user}** for the reason of: *{reason}*")
            await self.client.say(f"**{user}** Now has **{warns}** warnings.")
        with open("user.json", "w") as f:
            json.dump(warning,f,indent=4)
        with open("warnings.json", "r") as f:
            wan = json.load(f)
        if not server.id in wan:
            wan[server.id] = {}
        if not user.id in wan[server.id]:
            wan[server.id][user.id] = {"Warn Reasons": []}
        if user.id in wan[server.id]:
            wan[server.id][user.id]["Warn Reasons"].append(reason)
            await self.client.say(f"**{user}'s** warning reasons:")
        formatted = [f"warning {x+1}: {y}" for x,y in enumerate(wan[server.id][user.id]["Warn Reasons"])]
        await self.client.say(f"\n".join(formatted))
        with open("warnings.json", "w") as f:
            json.dump(wan,f,indent=4)

    @commands.command(pass_context=True)
    async def warnings(self, ctx, user: discord.Member = None):
        with open("user.json", "r") as f:
            warning = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.mute_members:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Mute Members**")
            return
        if not user:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to mention a user!")
            return
        if not server.id in warning:
            warning[server.id] = {}
        if not user.id in warning[server.id]:
            warning[server.id][user.id] = {"warnings": 0}
        if user.id in warning[server.id]:
            warns = warning[server.id][user.id]["warnings"]
            await self.client.say(f"**{user}** has **{warns}** warnings.")
        with open("warnings.json", "r") as f:
            wan = json.load(f)
        server = ctx.message.server
        if not server.id in wan:
            wan[server.id] = {}
        if not user.id in wan[server.id]:
            wan[server.id][user.id] = {"Warn Reasons": []}
        await self.client.say(f"**{user}'s** warning reasons:")
        formatted = [f"warning {x+1}: {y}" for x,y in enumerate(wan[server.id][user.id]["Warn Reasons"])]
        await self.client.say(f"\n".join(formatted))

    @commands.command(pass_context=True)
    async def lock(self, ctx):
        server = ctx.message.server
        channel = ctx.message.channel
        author = ctx.message.author
        if not author.server_permissions.manage_channels:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Channels**")
            return
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        await self.client.edit_channel_permissions(channel, server.default_role, overwrite)
        msg = await self.client.say(f"|<:check:514855967532384256>| **Locked down** the channel: {channel.mention}")
        await asyncio.sleep(5)
        await client.delete_message(msg)

    @commands.command(pass_context=True)
    async def unlock(self, ctx):
        server = ctx.message.server
        channel = ctx.message.channel
        author = ctx.message.author
        if not author.server_permissions.manage_channels:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Channels**")
            return
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        await self.client.edit_channel_permissions(channel, server.default_role, overwrite)
        msg = await self.client.say(f"|<:check:514855967532384256>| **Unlocked** the channel: {channel.mention}")
        await asyncio.sleep(5)
        await client.delete_message(msg)

        

def setup(client):
    client.add_cog(Moderation(client))
