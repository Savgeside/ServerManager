import discord
from io import BytesIO
import qrcode
import temp
from utils.chat_formatting import pagify
import json
import aiohttp
from urllib.parse import quote_plus
from discord.ext import commands
from colorthief import ColorThief

class General:
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def lmgtfy(self, ctx, *, search_terms: str):
        """Creates a lmgtfy link"""
        search_terms = search_terms.replace(" ", "+")
        await self.client.say("https://lmgtfy.com/?q={}".format(search_terms))


    @commands.command(pass_context=True, aliases=["perms"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def permissions(self, ctx, user: discord.Member = None, channel: str = None):
        """Get Permissions,
        Example Usage:
            n!permissions/n!perms @ReKT#0001 testing
        or
            n!permissions/n!perms ReKT#0001 #testing"""
        if user == None:
            user = ctx.message.author

        if channel == None:
            channel = ctx.message.channel
        else:
            channel = discord.utils.get(ctx.message.server.channels, name=channel)

        y = "✅"
        n = "❌"
        msg = ("Perms for %s in %s, ```\n") % (user.name.replace("@", "@\u200B"), channel.name.replace("@", "@\u200B"))

        try:
            perms = user.permissions_in(channel)
            for i in ["%s - %s" % (x[0], y if x[1] else n) for x in perms]:
                msg += "%s\n" % i
            msg += "\n```"
            await self.client.say(msg)
        except:
            await self.client.say("Problem getting that channel...")

    @commands.command(pass_context=True, aliases=['user'])
    async def userinfo(self, ctx, user: discord.Member = None):
        """Get a users info."""

        if not user:
            user = ctx.message.author
        try:
            playinggame = user.game
        except:
            playinggame = None
        server = ctx.message.server
        embed = discord.Embed(color=0xda4800)
        embed.set_author(name=user.name,
                         icon_url=user.avatar_url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Discriminator", value=user.discriminator)
        embed.add_field(name="Bot", value=str(user.bot))
        embed.add_field(name="Created", value=user.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Joined", value=user.joined_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Playing", value=playinggame)
        embed.add_field(name="Status", value=user.status)
        embed.add_field(name="Color", value=str(user.color))

        try:
            roles = [x.name for x in user.roles if x.name != "@everyone"]

            if roles:
                roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                           if x.name != "@everyone"].index)
                roles = ", ".join(roles)
            else:
                roles = "None"
            embed.add_field(name="Roles", value=roles)
        except:
            pass

        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def settings(self, ctx):
        with open("data.json", "r") as f:
            settings = json.load(f)
        server = ctx.message.server
        wmsg = settings[server.id]["welcome message"]
        lmsg = settings[server.id]["leave message"]
        wchan = settings[server.id]["welcome channel"]
        lchan = settings[server.id]["leave channel"]
        embed = discord.Embed(color=0xda4800)
        embed.add_field(name="» Welcome Message", value=wmsg)
        embed.add_field(name="» Leave Message", value=lmsg, inline=False)
        embed.add_field(name="» Welcome Channel", value=wchan)
        embed.add_field(name="» Leave Channel", value=lchan)
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def urban(self, ctx, *, search_terms: str, definition_number: int = 1):
        """Search Urban Dictionary"""

        def encode(s):
            return quote_plus(s, encoding='utf-8', errors='replace')
    
        channel_nsfw = await self.client.is_nsfw(ctx.message.channel)
        if not channel_nsfw:
            await self.client.say(f"Please move to an NSFW marked channel!")
            return
        search_terms = search_terms.split(" ")
        try:
            if len(search_terms) > 1:
                pos = int(search_terms[-1]) - 1
                search_terms = search_terms[:-1]
            else:
                pos = 0
            if pos not in range(0, 11):
                pos = 0
        except ValueError:
            pos = 0

        search_terms = "+".join([encode(s) for s in search_terms])
        url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    result = await r.json()
            if result["list"]:
                definition = result['list'][pos]['definition']
                example = result['list'][pos]['example']
                defs = len(result['list'])
                msg = ("**Definition #{} out of {}:\n**{}\n\n"
                       "**Example:\n**{}".format(pos + 1, defs, definition,
                                                 example))
                msg = pagify(msg, ["\n"])
                for page in msg:
                    await self.client.say("Check your DMs'!")
                    await self.client.send_message(ctx.message.author, page)
            else:
                await self.client.say("Your search terms gave no results.")
        except IndexError:
            await self.client.say("There is no definition #%s" % pos + 1)
    
    @commands.command(pass_context=True)
    async def animepic(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekobot.xyz/api/v2/image/animepic") as r:
                res = await r.json()
            image = res["message"]
            em = discord.Embed(color=0xda4800)
            msg = await self.client.say(embed=em.set_image(url=image))
            async with cs.get(image) as r:
                data = await r.read()
            em = discord.Embed(color=0xda4800)
            await self.client.edit_message(msg, embed=em.set_image(url=image))

    @commands.command(pass_context=True)
    async def coffee(self, ctx):
        """Coffee owo"""

        url = "https://coffee.alexflipnote.xyz/random.json"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
            em = discord.Embed(color=0xda4800)
            msg = await self.client.say("***Drinks Coffee*** :coffee: ", embed=em.set_image(url=res['file']))
            async with cs.get(res['file']) as r:
                data = await r.read()
            em = discord.Embed(color=0xda4800)
            await self.client.edit_message(msg, embed=em.set_image(url=res['file']))

    @commands.command(pass_context=True, aliases=['server'])
    async def serverinfo(self, ctx):
        """Display Server Info"""

        server = ctx.message.server

        verif = server.verification_level

        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])

        embed = discord.Embed(color=0xda4800)
        embed.add_field(name="Name", value=f"**{server.name}**\n({server.id})")
        embed.add_field(name="Owner", value=server.owner)
        embed.add_field(name="Online (Cached)", value=f"**{online}/{server.member_count}**")
        embed.add_field(name="Created at", value=server.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Channels", value=f"AFK Channel: **{server.afk_channel}**")
        embed.add_field(name="Roles", value=str(len(server.roles)))
        embed.add_field(name="Emojis", value=f"{len(server.emojis)}/100")
        embed.add_field(name="Region", value=str(server.region).title())
        embed.add_field(name="Security", value=f"Verification Level: **{verif}**\n")

        try:
            embed.set_thumbnail(url=server.icon_url)
        except:
            pass

        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def join(self, ctx, invite : discord.Invite):
        """Joins a server via invite."""
        if ctx.message.author.id == "481270883701358602":
            await self.client.accept_invite(invite)
            await self.client.say("Joined the server.")
        else:
            await self.client.say("**Owner only command.**")

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        if ctx.message.author.id == "481270883701358602":
            await self.client.say("Goodbye, I am leaving now.")
            await self.client.leave_server(server)
        else:
            await self.client.say("**Owner only command.**")
            
    @commands.command(pass_context=True)
    async def broadcast(self, ctx, *, msg):
        await self.client.delete_message(ctx.message)
        if ctx.message.author.id == "putyouridhere":
            for server in self.client.servers:
                for channel in server.channels:
                    try:
                        await self.client.send_message(channel, msg)
                    except Exception:
                        continue
                    else:
                        break
                        await self.client.whisper("**Message has been broadcasted!**")
        else:
            await self.client.say("**Sorry, only the bot owner may use this command.**")

def setup(client):
    client.add_cog(General(client))
