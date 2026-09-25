import discord
import datetime
from discord.ext import commands, tasks

THEMES = {
    "halloween": {
        "success": discord.Color.orange(),
        "fail": discord.Color.purple(),
        "avatar": "assets/halloween/avatar.png",
        "banner": "assets/halloween/banner.png",
    },
    "fools": {
        "success": discord.Color.yellow(),
        "fail": discord.Color.magenta(),
        "avatar": "assets/fools/avatar.png",
        "banner": "assets/fools/banner.png",
    },
    "christmas": {
        "success": discord.Color.green(),
        "fail": discord.Color.red(),
        "avatar": "assets/christmas/avatar.png",
        "banner": "assets/christmas/banner.png",
    },
    "easter": {
        "success": discord.Color.green(),
        "fail": discord.Color.pink(),
        "avatar": "assets/easter/avatar.png",
        "banner": "assets/easter/banner.png",
    },
    "default": {
        "success": discord.Color.blurple(),
        "fail": discord.Color.red(),
        "avatar": "assets/default/avatar.png",
        "banner": "assets/default/banner.png",
    },
}

def get_theme():
    now = datetime.datetime.now(datetime.timezone.utc)

    if now.month == 4 and now.day == 1:
        return "fools"
    elif now.month == 10:
        return "halloween"
    elif now.month == 12:
        return "christmas"
    elif now.month == 3:
        return "easter"

    return "default"

cached_theme = get_theme()

def get_success_colour():
    return THEMES[cached_theme]["success"]

def get_fail_colour():
    return THEMES[cached_theme]["fail"]

def get_avatar():
    return THEMES[cached_theme]["avatar"]

def get_banner():
    return THEMES[cached_theme]["banner"]

class Theming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_date = None
        self.update_theme.start()

    def cog_unload(self):
        self.update_theme.cancel()

    async def apply_theme(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.date()
        if self.current_date == date:
            return

        global cached_theme
        cached_theme = get_theme()

        self.current_date = date

        avatar_file = get_avatar()
        banner_file = get_banner()

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