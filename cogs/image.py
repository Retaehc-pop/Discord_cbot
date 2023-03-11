from discord.ext import commands
from discord.ext.commands import Context

import discord
import aiohttp
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Images(commands.Cog, name="image"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(name="cat", description="Random cat image.")
    @checks.not_blacklisted()
    async def _cat(self, context: Context) -> None:
        async with context.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://aws.random.cat/meow") as request:
                    if request.status == 200:
                        data = await request.json()
                        embed = discord.Embed(colour=0xEEEEEE)
                        embed.set_image(url=data['file'])
                    else:
                        embed = discord.Embed(
                            title="Error!",
                            description="There is something wrong with the API, please try again later",
                            color=0xE02B2B,
                        )
                    await context.send(embed=embed)
    
    @commands.hybrid_command(name="dog", description="Random dog image.")
    @checks.not_blacklisted()
    async def dog(self,  context: Context):
        async with context.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as request:
                    if request.status == 200:
                        data = await request.json()
                        embed = discord.Embed( colour=0xEEEEEE)
                        embed.set_image(url=data['url'])
                    else:
                        embed = discord.Embed(
                            title="Error!",
                            description="There is something wrong with the API, please try again later",
                            color=0xE02B2B,
                        )
                    await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Images(bot))
