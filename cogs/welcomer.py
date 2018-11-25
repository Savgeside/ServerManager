import discord
import json
import PIL
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import requests
from io import BytesIO
import random
from discord.ext import commands

class Welcomer:
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True)
    async def welcomer(self, ctx):
        if not ctx.invoked_subcommand:
            await self.client.say(f"<:xmark:514855937832386573> Pick a welcomer setting!")

    @welcomer.command(pass_context=True)
    async def message(self, ctx, *, welcomermsg):
        with open("data.json", "r") as f:
            welcome = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.manage_server:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Server**")
            return
        if not welcomermsg:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You need to state a welcome message!")
            return
        if not server.id in welcome:
            welcome[server.id] = {}
        if server.id in welcome:
            welcome[server.id]["welcome message"] = welcomermsg
            await self.client.say(f"<:check:514855967532384256>| Set welcomer message")
            await self.client.say(f"| **Welcome Message** - {welcomermsg}")
        with open("data.json", "w") as f:
            json.dump(welcome,f,indent=4)

    @welcomer.command(pass_context=True)
    async def channel(self, ctx, *, channel = None):
        with open("data.json", "r") as f:
            welcome = json.load(f)
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
        if not server.id in welcome:
            welcome[server.id] = {}
        if server.id in welcome:
            welcome[server.id]["welcome channel"] = channel
            await self.client.say(f"<:check:514855967532384256>| Set welcomer channel")
            await self.client.say(f"| **Welcome Channel** - {channel}")
        with open("data.json", "w") as f:
            json.dump(welcome,f,indent=4)

    async def on_member_join(self, member):
        with open('data.json', "r") as f:
            welcome = json.load(f)
        server = member.server
        if not server.id in welcome:
            welcome[server.id] = {}
        msg = welcome[server.id]["welcome message"].format(**{'member': member.mention, 'server': server.name, 'members': server.member_count})
        chan = welcome[server.id]["welcome channel"]
        if chan == "Not Set":
            return
        if msg == "Not Set":
            return
        channel = discord.utils.get(server.channels, name=chan)
        await self.client.send_message(channel, msg)


def setup(client):
    client.add_cog(Welcomer(client))