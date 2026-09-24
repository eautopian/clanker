import discord
import datetime
from discord.ext import commands, tasks

SUCCESS_COLOUR = discord.Color.blurple()
BAD_COLOUR = discord.Color.red()

class Theming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_date = None
        self.update_theme.start()

    def cog_unload(self):
        self.update_theme.cancel()

    async def apply_theme(self):
        global SUCCESS_COLOUR, BAD_COLOUR

        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.date()
        month = now.month
        day = now.day

        if month == 4 and day == 1:
            SUCCESS_COLOUR = discord.Color.yellow()
            BAD_COLOUR = discord.Color.magenta()
            avatar_file = "assets/fools/avatar.png"
            banner_file = "assets/fools/banner.png"

        # elif month == 10:
        #     SUCCESS_COLOUR = discord.Color.orange()
        #     BAD_COLOUR = discord.Color.purple()
        #     avatar_file = "assets/halloween/avatar.png"
        #     banner_file = "assets/halloween/banner.png"

        # elif month == 12:
        #     SUCCESS_COLOUR = discord.Color.green()
        #     BAD_COLOUR = discord.Color.red()
        #     avatar_file = "assets/christmas/avatar.png"
        #     banner_file = "assets/christmas/banner.png"

        # elif month == 3:
        #     SUCCESS_COLOUR = discord.Color.green()
        #     BAD_COLOUR = discord.Color.pink()
        #     avatar_file = "assets/easter/avatar.png"
        #     banner_file = "assets/easter/banner.png"

        else:
            SUCCESS_COLOUR = discord.Color.blurple()
            BAD_COLOUR = discord.Color.red()
            avatar_file = "assets/default/avatar.png"
            banner_file = "assets/default/banner.png"

        if self.current_date == date:
            return

        self.current_date = date

        with open(avatar_file, "rb") as f:
            avatar = f.read()

        with open(banner_file, "rb") as f:
            banner = f.read()

        await self.bot.user.edit(avatar=avatar, banner=banner)

    @tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=datetime.timezone.utc))
    async def update_theme(self):
        await self.apply_theme()

    @update_theme.before_loop
    async def before_update_theme(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    cog = Theming(bot)
    await bot.add_cog(cog)
    await cog.apply_theme()