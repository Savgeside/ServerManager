import discord
import nekobot
import config
from discord.ext import commands

class NSFW:
    def __init__(self, client):
        self.client = client
        self.nekobot = nekobot.Client(loop=self.client.loop)

    @commands.command(pass_context=True)
    async def pgif(self, ctx):
        channel_nsfw = await self.client.is_nsfw(ctx.message.channel)
        if not channel_nsfw:
            await self.client.say(f"Please move to an **NSFW** marked channel!")
            return
        await self.client.say(f"**Here you go :wink:**")
        em = discord.Embed(color=0xda4800)
        em.set_image(url=await self.nekobot.image("pgif"))

        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def anal(self, ctx):
        channel_nsfw = await self.client.is_nsfw(ctx.message.channel)
        if not channel_nsfw:
            await self.client.say(f"Please move to an **NSFW** marked channel!")
            return
        await self.client.say(f"**Here you go :wink:**")
        embed = discord.Embed(color=0xda4800)
        embed.set_image(url=await self.nekobot.image("anal"))
        await self.client.say(embed=embed)

    @commands.command(pass_context=True, name="4k")
    async def _fourk(self, ctx):
        channel_nsfw = await self.client.is_nsfw(ctx.message.channel)
        if not channel_nsfw:
            await self.client.say(f"Please move to an **NSFW** marked channel!")
            return
        await self.client.say(f"**Here you go :wink:**")
        embed = discord.Embed(color=0xda4800)
        embed.set_image(url=await self.nekobot.image("4k"))
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def ass(self, ctx):
        channel_nsfw = await self.client.is_nsfw(ctx.message.channel)
        if not channel_nsfw:
            await self.client.say(f"Please move to an **NSFW** marked channel!")
            return
        await self.client.say(f"**Here you go :wink:**")
        embed = discord.Embed(color=0xda4800)
        embed.set_image(url=await self.nekobot.image("ass"))

        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gonewild(self, ctx):
        channel_nsfw = await self.client.is_nsfw(ctx.message.channel)
        if not channel_nsfw:
            await self.client.say(f"Please move to an **NSFW** marked channel!")
            return
        await self.client.say(f"**Here you go :wink:**")
        embed = discord.Embed(color=0xda4800)
        embed.set_image(url=await self.nekobot.image("gonewild"))

        await self.client.say(embed=embed)

def setup(client):
    client.add_cog(NSFW(client))