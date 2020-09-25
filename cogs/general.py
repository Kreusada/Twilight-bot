import json
from copy import copy
from platform import python_version
from random import choice

import discord
from discord import __version__ as discord_version
from discord.ext import commands
from discord.utils import get
from Tools.twilight_tools import BasicUtils, EmbedCreator, guild_owner


class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.basicutils = BasicUtils(self)
        self.EmbedCreator = EmbedCreator(self)

    @commands.Cog.listener()
    async def on_ready(self):
        version = await self.basicutils.get_version()
        await self.client.change_presence(activity=discord.Game(name=".help | Version {version}".format(version=version)))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong.")

    @commands.command(help="Probably the most important command")
    async def about(self, ctx):
        with open("about.txt", "r") as f:
            about_message = f.read()

        embed = self.EmbedCreator.create(
            title="About Twilight",
            description=about_message, color=discord.Color.purple(),
            footer="Jojo#7791"
        )
        await ctx.send(embed=embed)

    @commands.group()
    async def version(self, ctx):
        if ctx.invoked_subcommand is None:
            version = await self.basicutils.get_version()
            await ctx.send("My version is {0}!".format(version))

    @version.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx, version: str = None):
        if version is not None:
            await self.basicutils.update_version(version)
            version = await self.basicutils.get_version()
            await self.client.change_presence(activity=discord.Game(name=">help | Version {version}".format(version=version)))
            await ctx.send("Updated version!")
        else:
            await ctx.send("Could not update version")

    @commands.command(name="check")
    async def _check(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        time = user.joined_at.strftime("%d %b %Y %H:%M")
        made = user.created_at.strftime("%d %b %Y %H:%M")
        embed = await self.embed.create(
            ctx, title="{0}'s join and creation times".format(
                user.display_name),
            color=ctx.author.color, footer="User join/creation dates")
        embed.add_field(
            name="Joined at",
            value=time, inline=False)
        embed.add_field(
            name="Account made at",
            value=made, inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx, user: discord.Member, *, command):
        """Sudo another user invoking a command.
        The prefix must not be entered.
        """
        msg = copy(ctx.message)
        msg.author = user
        msg.content = ctx.prefix + command

        ctx.bot.dispatch("message", msg)

    @commands.command()
    async def swear(self, ctx):
        await ctx.send("<@544974305445019651> quit swearing, sweet Celestia")

    @commands.command(name="signup", aliases=["sign", "su"])
    @commands.guild_only()
    @guild_owner()
    # @commands.has_permissions(administrator=True)
    async def sign_up(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel.id
        else:
            channel = channel.id

        with open('newsletter.json', 'r') as f:
            newsletter = json.load(f)
        if str(ctx.guild) not in newsletter.keys():
            newsletter[str(ctx.guild)] = int(channel)
            await ctx.send("You have now been signed up for newsletters!")
            with open('newsletter.json', 'w') as f:
                json.dump(newsletter, f, indent=4)
        else:
            await ctx.send("You have already been signed up for newsletters!")

    @commands.command(name="optout", aliases=["out", "oo", "opt"])
    @commands.has_permissions(administrator=True)
    async def opt_out(self, ctx):
        with open("newsletter.json", "r") as f:
            newsletter = json.load(f)
        if str(ctx.guild) in newsletter.keys():
            newsletter.pop(str(ctx.guild))
            await ctx.send("You have now been opted out of newsletters!")
            with open("newsletter.json", "w") as f:
                json.dump(newsletter, f, indent=4)
        else:
            await ctx.send("I could not find your guild in the newsletter catalog")

    @commands.command(aliases=["update", "news"], hidden=True)
    @commands.is_owner()
    async def newsletter(self, ctx, *, message: str = None):
        if message is None:
            await ctx.send("I cannot send an empty message :p")
        else:
            guilds = []
            failed_guilds = []
            with open("newsletter.json", "r") as f:
                newsletters = json.load(f)
            for guild in newsletters.keys():
                try:
                    guilds.append(guild)
                    channel = self.client.get_channel(newsletters[guild])
                    await channel.send(message)
                except:
                    failed_guilds.append(guild)
            message = "".join(guilds)
            fail_message = "".join(failed_guilds)
            await ctx.send("Sent these messages out to the following servers:\n{0}\nThese servers could not have the messages sent to\n{1}".format(message, fail_message))

    @commands.command()
    async def choose(self, ctx, *options):
        """**Choose between several options**
        Choose between two or more options

        *Yes I stole this from Red :p
        """
        if len(options) < 2:
            await ctx.send("Please input more than 1 options")
        else:
            await ctx.send(choice(options))

    @commands.command()
    async def about(self, ctx):
        jojo = self.client.get_user(544974305445019651)
        embed = await self.EmbedCreator.create(
            ctx,
            title="About Twilight",
            description="Twilight bot is a bot made by Jojo#7791 both as a fan creation/gift to the My Little Pony: Friendship is Magic community and a school project (kinda, I'm learning Python basically)\nIt is written in Python and is totally bug free... suuure.\nIf you have any questions don't be afraid to ask in the [support server!](https://discord.gg/9cxxJSp)\nThanks for checking out Twilight!",
            footer="About Twilight",
            footer_image=jojo.avatar_url)
        embed.add_field(
            name="Python Version",
            value=python_version(),
            inline=True
        )
        embed.add_field(
            name="Discord.py Version",
            value=discord_version,
            inline=True
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Get the bot invite link and the support server link."""

        embed = await self.EmbedCreator.create(ctx,
                                               title="Invite/Support server link",
                                               description="Get the [bot](https://discord.com/api/oauth2/authorize?client_id=734159757488685126&permissions=8&scope=bot)",
                                               footer="Twilight Bot invite link")
        embed.add_field(name="Support Server link",
                        value="Get the [link](https://discord.gg/9cxxJSp) to the support server")
        await self.BasicUtils.whisper(ctx, ctx.author, embed=embed)


def setup(client):
    client.add_cog(General(client))
