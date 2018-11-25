import discord
import random
import json
import os
from discord.ext import commands


client = commands.Bot(command_prefix=">")

owners = [
    "481270883701358602"
]

extensions = ["cogs.moderation", "cogs.stats", "cogs.triggers", "cogs.welcomer", "cogs.fun", "cogs.leaver", "cogs.general", "cogs.help", "cogs.nsfw"]
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

@client.event
async def on_ready():
    print("MetalBot, is ready!")
    servers = len(client.servers)
    await client.change_presence(game=discord.Game(name=f"for >help|In {servers} servers", type=3))

@client.command(pass_context=True)
async def reload(ctx, extension):
    author = ctx.message.author
    if author.id in owners:
        try:
            client.unload_extension(extension)
            client.load_extension(extension)
            await client.say(f"<a:loading:515738679478583307> Reloaded **{extension}**")
        except Exception as error:
            await client.say(f"<:xmark:514855937832386573> A error occured: **{error}**")
    else:
        await client.say(f"**{author}**, Sorry! This is an owner only command.")

@client.event
async def on_message(message):
    await client.process_commands(message)
    with open("triggers.json", "r") as f:
        trig = json.load(f)
    server = message.server
    if not server.id in trig:
        trig[server.id] = {}
    trigger = message.content
    output = trig[server.id].get(trigger)
    if output:
        await client.send_message(message.channel, output)

@client.event
async def on_server_join(server):
    servers = len(client.servers)
    await client.change_presence(game=discord.Game(name=f"for >help|In {servers} servers", type=3))
    with open("data.json", "r") as f:
        data = json.load(f)
    if not server.id in data:
        data[server.id] = {}
        data[server.id]["welcome message"] = "Not Set"
        data[server.id]["welcome channel"] = "Not Set"
        data[server.id]["leave message"] = "Not Set"
        data[server.id]["leave channel"] = "Not Set"
    with open("data.json", "w") as f:
        json.dump(data,f,indent=4)

@client.event
async def on_server_remove(server):
    servers = len(client.servers)
    await client.change_presence(game=discord.Game(name=f"for >help| In {servers} servers", type=3))

@client.event
async def is_nsfw(channel: discord.Channel):
    try:
        _gid = channel.server.id
    except AttributeError:
        return False
    data = await client.http.request(
        discord.http.Route(
            'GET', '/guilds/{guild_id}/channels', guild_id=_gid))
    channeldata = [d for d in data if d['id'] == channel.id][0]
    return channeldata['nsfw']

@client.event
async def send_stats():
    await bot.wait_until_ready()
    dbltoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUxNTczMzkwNjI3Njc0NTIyMyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTQzMTI5MTUyfQ.q5TI4MRZD4wLg7BdvzwRpm-UQRLGcpOj0gWHxAJ_1wc"
    url = "https://discordbots.org/api/bots/" + str(bot.user.id) + "/stats"
    headers = {"Authorization" : dbltoken}
    while True:
        data = {"server_count"  : len(bot.servers)}
        requests.post(url,data=data,headers=headers)
        await asyncio.sleep(10)
        
client.loop.create_task(send_stats())
client.run(os.environ['TOKEN'])
