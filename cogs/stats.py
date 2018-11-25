import discord
import psutil
import string
import argparse, os, shlex, traceback, io, textwrap, asyncio, re
from contextlib import redirect_stdout
from discord.ext import commands

class Stats:
    def __init__(self, client):
        self.client = client
        self._last_result = None

    @commands.command(pass_context=True)
    async def botinfo(self, ctx):
        cpu_per = psutil.cpu_percent()
        cores = psutil.cpu_count()
        memory = psutil.virtual_memory().total >> 20
        mem_usage = psutil.virtual_memory().used >> 20
        storage_free = psutil.disk_usage('/').free >> 30
        users = len(set(self.client.get_all_members()))
        members = list(set(self.client.get_all_members()))
        online = len(set(filter(lambda m: not m.status == discord.Status.offline, members)))
        offline = len(set(filter(lambda m: m.status == discord.Status.offline, members)))
        dnd = len(set(filter(lambda m: m.status == discord.Status.dnd, members)))
        idle = len(set(filter(lambda m: m.status == discord.Status.idle, members)))
        embed = discord.Embed(color=0xda4800)
        embed.set_author(icon_url="https://cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png", name="ServerManager!")
        embed.add_field(name="ServerManager Information", value="MetalBot was coded in discord.py - async - 0.16.12 <:py:515983556951015434>")
        embed.add_field(name="» Cores", value=f"{cores}", inline=False)
        embed.add_field(name="» CPU%", value=f"{cpu_per}", inline=True)
        embed.add_field(name="» RAM Usage", value=f"{mem_usage}/{memory} MB ({int(memory - mem_usage)}MB Free)", inline=False)
        embed.add_field(name="» Storage", value=f"{storage_free} Free GB", inline=False)
        embed.add_field(name=f"» All Users [{users}]", value=f"Online - {online} \n Offline - {offline}\n Dnd - {dnd} \n Idle - {idle}")
        embed.add_field(name="» All Servers", value=len(self.client.servers), inline=False)
        embed.add_field(name="» Total Channels", value=len(set(self.client.get_all_channels())), inline=False)
        embed.add_field(name="» Servers", value=len(self.client.servers))
        await self.client.say(embed=embed)

    @commands.command()
    async def creds(self):
        embed = discord.Embed(color=0xda4800)
        embed.set_author(icon_url="https://cdn.discordapp.com/attachments/514225543881949215/515781228503236612/logo.png", name="ServerManager! Credits")
        embed.add_field(name="» Developer", value="Savage#5185")
        embed.add_field(name="» Helpers", value="Hamza#5938\nMysticCraft Playz#9749", inline=False)
        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Stats(client))