import discord
import requests
import aiohttp
import random
import config
import nekobot
from io import BytesIO
from discord.ext import commands

class Fun:
    def __init__(self, client):
        self.client = client

    async def __get_image(self, ctx, user=None):

        message = ctx.message

        if len(message.attachments) > 0:
            return message.attachments[0].url

        def check(m):
            return m.channel == message.channel and m.author == message.author

        try:
            await self.client.say("Send me an image!")
            x = await self.client.wait_for_message('message', check=check, timeout=15)
        except:
            return await self.client.say("Timed out...")

        if not len(x.attachments) >= 1:
            return await self.client.say("No images found.")

        return x.attachments[0].url

    def __embed_json(self, data, key="message"):
        em = discord.Embed(color=0xDEADBF)
        em.set_image(url=data[key])
        return em

    @commands.command(pass_context=True)
    async def joke(self, ctx):
        async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as cs:
            async with cs.get('https://icanhazdadjoke.com/') as r:
                res = await r.json()
        await self.client.say(f"**{res['joke']}**")

    @commands.command(pass_context=True)
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member = None):
        """Ship OwO"""
        if user2 is None:
            user2 = ctx.message.author

        if user1.avatar:
            user1url = "https://cdn.discordapp.com/avatars/%s/%s.png" % (user1.id, user1.avatar,)
        else:
            user1url = "https://cdn.discordapp.com/embed/avatars/1.png"
        if user2.avatar:
            user2url = "https://cdn.discordapp.com/avatars/%s/%s.png" % (user2.id, user2.avatar,)
        else:
            user2url = "https://cdn.discordapp.com/embed/avatars/1.png"

        self_length = len(user1.name)
        first_length = round(self_length / 2)
        first_half = user1.name[0:first_length]
        usr_length = len(user2.name)
        second_length = round(usr_length / 2)
        second_half = user2.name[second_length:]
        finalName = first_half + second_half

        score = random.randint(0, 100)
        filled_progbar = round(score / 100 * 10)
        counter_ = '█' * filled_progbar + '‍ ‍' * (10 - filled_progbar)

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekobot.xyz/api/imagegen?type=ship&user1=%s&user2=%s" % (user1url, user2url,)) as r:
                res = await r.json()

        em = discord.Embed(color=0xDEADBF)
        em.title = "%s ❤ %s" % (user1.name, user2.name,)
        em.description = f"**Love %**\n" \
                         f"`{counter_}` **{score}%**\n\n{finalName}"
        em.set_image(url=res["message"])

        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def whowouldwin(self, ctx: commands.Context, user1: discord.Member, user2: discord.Member = None):
        """Who would win"""
        if user2 is None:
            user2 = ctx.message.author
        user1url = user1.avatar_url
        user2url = user2.avatar_url

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekobot.xyz/api/imagegen?type=whowouldwin&user1=%s&user2=%s" % (user1url, user2url,)) as r:
                res = await r.json()

        await self.client.say(embed=self.__embed_json(res))

    @commands.command(pass_context=True)
    async def dong(self, ctx, *, user: discord.Member):
        """Detects user's dong length"""
        state = random.getstate()
        random.seed(user.id)
        dong = "8{}D".format("=" * random.randint(0, 30))
        random.setstate(state)
        em = discord.Embed(title="{}'s Dong Size".format(user), description="Size: " + dong, colour=0xda4800)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def kannagen(self, ctx, *, text: str):
        """Generate Kanna"""
        url = f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()

        await self.client.say(embed=self.__embed_json(res))

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()
        await self.client.say(f":cat: **Cute Kitties**")
        embed = discord.Embed(color=0xda4800)
        embed.description = f"Image Not Showing? [Click Here]({data['file']})"
        embed.set_image(url=f"{data['file']}")
        await self.client.say(embed=embed)
        
    @commands.command(pass_context=True)
    async def dog(self, ctx):
        response = requests.get('https://random.dog/woof.json')
        data = response.json()
        await self.client.say(f":dog: **Cute Doggies**")
        embed = discord.Embed(color=0xda4800)
        embed.description = f"Image Not Showing? [Click Here]({data['url']})"
        embed.set_image(url=f"{data['url']}")
        await self.client.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def kiss(self, ctx, user: discord.Member = None):
        response = requests.get("https://nekos.life/api/v2/img/kiss")
        data = response.json()
        data = response.json()
        if user is None:
            await self.client.say("You need to mention a user! (You don't wanna kiss yourself!)")
            return
        await self.client.say(f"**Awwww, you kissed {user}** :heart_exclamation: ")
        embed = discord.Embed(color=0xda4800)
        embed.description = f"Image not showing? [Click Here]({data['url']})"
        embed.set_image(url=f"{data['url']}")
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def cuddle(self, ctx, user: discord.Member = None):
        response = requests.get("https://nekos.life/api/v2/img/cuddle")
        data = response.json()
        data = response.json()
        if user is None:
            await self.client.say("You need to mention a user! (You don't wanna cuddle yourself!)")
            return
        await self.client.say(f"**Awwww, you cuddled {user}** :heart_exclamation: ")
        embed = discord.Embed(color=0xda4800)
        embed.description = f"Image not showing? [Click Here]({data['url']})"
        embed.set_image(url=f"{data['url']}")
        await self.client.say(embed=embed)
                        
    @commands.command(pass_context = True)
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.reddit.com/r/me_irl/random") as r:
                author = ctx.message.author
                data = await r.json()
                await self.client.say("**Take some memes ;D**")
                embed = discord.Embed(color=0xda4800)
                embed.set_image(url = data[0]["data"]["children"][0]["data"]["url"])

                await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Fun(client))
