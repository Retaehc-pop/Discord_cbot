import platform
import random

import aiohttp
import discord

from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime
from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="serverinfo",
        description="Get information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0xEEEEEE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(name="ping", description="Check if the bot is alive.",)
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive. If it is, it will reply with the latency.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xEEEEEE,
        )
        await context.send(embed=embed)
        
    @commands.hybrid_command(name="donate", description="one-time contribution")
    async def _donate(self, context: Context) -> None:
        """
        If you want to support the development of this bot, you can do so by donating to the developer.
        """
        embed = discord.Embed(
            title="Cbot",
            description=
            """
            If you enjoy using thi bot, please consider donating to keep it online and performing well!
            [Paypal](https://www.paypal.com/paypalme/retaehcpop) 
            """,
            color=0xEEEEEE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(name="invite", description="Get the invite link of the bot to be able to invite it.",)
    @checks.not_blacklisted()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
            color=0xD75BF4,
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)


    @commands.hybrid_command(name="today",description="get today date and fun fact")
    @checks.not_blacklisted()
    async def _today(self, context: Context) -> None:
        """
        get today date and fun fact"
        """
        month = datetime.now().month
        date = datetime.now().day
        year = datetime.now().year
        async with context.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://byabbe.se/on-this-day/{month}/{date}/events.json") as request:
                    if request.status == 200:
                        data = await request.json()
                        events = data['events']
                        chosen_event = random.choice(events)
                        embed = discord.Embed(title=f":calendar:{date}/{month}/{year}",color=0xEEEEEE)
                        embed.add_field(name=f"{year-int(chosen_event['year'])} years ago",
                                        value=f"""
                                        {chosen_event['description']}
                                        [Source]({chosen_event['wikipedia'][0]['wikipedia']})
                                        """)
                    else:
                        embed = discord.Embed(
                            title="Error!",
                            description="There is something wrong with the API, please try again later",
                            color=0xE02B2B,
                        )
                    await context.send(embed=embed)
                
                
    @commands.hybrid_command(name="bitcoin",description="Get the current price of bitcoin.")
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            ) as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript"
                    )  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0xEEEEEE,
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
