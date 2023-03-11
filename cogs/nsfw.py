from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
import aiohttp
import discord
import random

# Here we name the cog and create a new class for the cog.


class NSFW(commands.Cog, name="nsfw"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="nsfw", description="you know what it does")
    @commands.is_nsfw()
    @checks.not_blacklisted()
    async def _nsfw(self, context: Context, *, tag=''):
        await context.message.delete()
        choice = ['ahegao', 'anal', 'asian', 'ass', 'bdsm', 'boobs', 'creampie', 'cum', 'feet', 'gay', 'gif', 'hentai',
                  'insertion', 'lesbian', 'milf', 'penis', 'pussy', 'redhead', 'short', 'thigh', 'toys', 'subreddit', 'video', '']
        if tag not in choice:
            return await context.send(choice)
        if tag == '':
            tag = random.choice(choice)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api-popcord.vercel.app/img/nsfw?type={tag}") as request:
                if request.status == 200:
                    data = await request.json()
                    if tag == 'video':
                        return await context.send(data['url'])
                    embed = discord.Embed(title=tag, color=0xEEEEEE)
                    embed.set_image(url=data["url"])
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NSFW(bot))
