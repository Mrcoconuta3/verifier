import re
import time
import discord
from discord.ext import commands
from discord.ext.commands import Context 
from discord import app_commands

time_regex = re.compile("(?:(\d{1,5})(h|s|g|p|m|d))+?")
time_dict = {"h":3600, "s":1, "g":1, "p":60, "m":60, "d":86400}

def convert_sec(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hour:
        return "%dh%02dp%02d" % (hour, minutes, seconds)
    else:
        return "%02dp%02ds" % (minutes, seconds)

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError as e:
                print(e)
                raise commands.BadArgument("{} không hợp lệ! h/p/s/d là key hợp lệ!\nVD: 1h56p hoặc 2p20s".format(k))
            except ValueError as a:
                print(a)
                raise commands.BadArgument("{} Không phải con số!".format(v))
        return int(time)

def dumbass(yourtime, leadertime, rallytime=None):
    times = abs(yourtime - leadertime)
    counting_down = None
    time_min = convert_sec(times)
    
    if rallytime >= 1:
        time_till_rally_end = int((rallytime + leadertime) - yourtime)
        counting_down = int(time.time()) + time_till_rally_end

    if yourtime > leadertime: #Xuất quân khi thời gian rally còn x giây
        text = "<:wallstand:942371979502161931> Xuất quân khi Rally còn **{}**({}s)".format(time_min,times)
    else:
        if yourtime < leadertime: #Xuất quân khi rally còn x giây nữa đến mục tiêu 
            text = f"<a:walkingcat:1048898191405371433> Xuất quân khi Rally đã di chuyển được **{time_min}**({times}s) hoặc còn **{convert_sec(yourtime)}**({yourtime}s) nữa đến mục tiêu"
        elif yourtime == leadertime:
            text = f"<a:yee:1024242613596991548> Xuất quân lập tức khi Rally di chuyển"

    return text, counting_down

class calculator(commands.Cog, name="dumb"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command()
    async def sync(self,ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild= ctx.guild)#You can delete the part in the Parentheses for globally use
        await ctx.reply(f'Đã đồng bộ {len(fmt)} commands.')
    
    @commands.hybrid_command(
        name="rein",
        description="Tính toán thời gian để viện trợ"
    )
    @app_commands.describe(yourtime="Thời gian hành quân của bạn đến mục tiêu. VD:1p50s", theleadertime="Thời gian hành quân của kẻ địch/đồng minh tới mục tiêu. VD:2p10s", rallytime = "Thời gian Rally. VD:5p")
    @app_commands.guilds(923898426096222209) #Replace this with your guild id if you want to use this locally or Delete this line for Globally
    async def rein(self, context:Context, yourtime:TimeConverter, theleadertime:TimeConverter, rallytime:TimeConverter) -> None:
        time, counting = dumbass(yourtime, theleadertime, rallytime)
        embed = discord.Embed(description= f'{time}',color= 0xcdfffb)
        if counting:
            embed.add_field(name='**Đếm ngược**',value= f'<t:{counting}:R>' )
        await context.reply(embed = embed)
        print(rallytime)

async def setup(bot):
    await bot.add_cog(calculator(bot))