import discord
import json
from discord.ext import commands

class Triggers:
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True)
    async def trigger(self, ctx):
        if not ctx.invoked_subcommand:
            await self.client.say(f"<:xmark:514855937832386573> You need to make a custom trigger or delete it!")

    @trigger.command(pass_context=True)
    async def add(self, ctx, trigger: str = None, *, output: str = None):
        with open("triggers.json", "r") as f:
            added = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.manage_server:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Server**")
            return
        if trigger is None:
            await self.client.say(f"**{author}** |<:xmark:514855937832386573>| Please state a trigger!")
            return
        if output is None:
            await self.client.say(f"**{author}** |<:xmark:514855937832386573>| Please state a output!")
            return
        if not server.id in added:
            added[server.id] = {}
        if server.id in added:
            added[server.id][trigger] = output
            await self.client.say(f"<:check:514855967532384256>| Trigger Added")
            await self.client.say(f"| **Trigger** - {trigger}")
            await self.client.say(f"| **Output** - {output}")
        with open("triggers.json", "w") as f:
            json.dump(added,f,indent=4)

    @trigger.command(pass_context=True)
    async def delete(self, ctx, trigger: str):
        with open("triggers.json", "r") as f:
            delete = json.load(f)
        server = ctx.message.server
        author = ctx.message.author
        if not author.server_permissions.manage_server:
            await self.client.say(f"**{author}**, |<:xmark:514855937832386573>| You do not have the correct permissions!\nCorrect Permissions: **Manage Server**")
            return
        if trigger is None:
            await self.client.say(f"**{author}** |<:xmark:514855937832386573>| Please state a trigger!")
            return
        if not trigger in delete[server.id].keys():
            await self.client.say(f"**{author}** |<:xmark:514855937832386573>| Trigger not found!")
            return
        if not server.id in delete:
            delete[server.id] = {}
        if server.id in delete:
            del delete[server.id][trigger]
            await self.client.say("<:check:514855967532384256>| Trigger Deleted")
            await self.client.say(f"| **Trigger** - {trigger}")
        with open("triggers.json", "w") as f:
            json.dump(delete,f,indent=4)

    @trigger.command(pass_context=True)
    async def list(self, ctx):
        with open("triggers.json", "r") as f:
            trigs = json.load(f)
        server = ctx.message.server
        if not server.id in trigs:
            trigs[server.id] = {}
        if server.id in trigs:
            formatted = [f"{x+1} | **{y}**" for x,y in enumerate(trigs[server.id].keys())]
            await self.client.say(f"**Triggers for {server.name}**")
            await self.client.say("\n".join(formatted))

    
def setup(client):
    client.add_cog(Triggers(client))
