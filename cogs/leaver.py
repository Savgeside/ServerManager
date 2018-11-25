import discord
import json
from discord.ext import commands

class Leaver:
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True)
    async def leaver(self, ctx):
        if not ctx.invoked_subcommand:
            await self.client.say(f"<:xmark:514855937832386573> Pick a leaver setting!")

    @leaver.command(pass_context=True)
    async def message(self, ctx, *, leavemsg):
        with open("data.json", "r") as f:
            leave = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.manage_server:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Server**")
            return
        if not leavemsg:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to state a welcome message!")
            return
        if not server.id in leave:
            leave[server.id] = {}
        if server.id in leave:
            leave[server.id]["leave message"] = leavemsg
            await self.client.say(f"<:check:514855967532384256>| Set leaver message")
            await self.client.say(f"| **Leaver Message** - {leavemsg}")
        with open("data.json", "w") as f:
            json.dump(leave,f,indent=4)

    @leaver.command(pass_context=True)
    async def channel(self, ctx, *, channel = None):
        with open("data.json", "r") as f:
            leave = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.manage_server:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Server**")
            return
        chan = discord.utils.get(server.channels, name=channel)
        if channel is None:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to state a welcome channel!")
            return
        if chan is None:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| The channel you set is not found! Try again")
            return
        if not server.id in leave:
            leave[server.id] = {}
        if server.id in leave:
            leave[server.id]["leave channel"] = channel
            await self.client.say(f"<:check:514855967532384256>| Set leaver channel")
            await self.client.say(f"| **Leave Channel** - {channel}")
        with open("data.json", "w") as f:
            json.dump(leave,f,indent=4)

    async def on_member_remove(self, member):
        with open("data.json", "r") as f:
            leave = json.load(f)
        server = member.server
        if not server.id in leave:
            leave[server.id] = {}
        msg = leave[server.id]["leave message"].format(**{'member': member, 'server': server.name, 'members': server.member_count})
        chan = leave[server.id]["leave channel"]
        channel = discord.utils.get(server.channels, name=chan)
        if chan == "Not Set":
            return
        if msg == "Not Set":
            return
        await self.client.send_message(channel, msg)

def setup(client):
    client.add_cog(Leaver(client))