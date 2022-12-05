import datetime
import discord
import asyncio
import re
from discord.ext import commands,tasks
import time

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}



class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


class Timer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reminding(self, ctx, channel:discord.TextChannel , *, times:TimeConverter = None):
        """Timer for the specified time- time in 2d 10h 3m 2s format ex:
        &reminding #channel 1d"""
        #try:
        #    channel = self.client.get_channel(channel)
        #except Exception as e:
        #    print(e)
        timem = int(time.time()) + int(times)
        await ctx.send(f'Time till mention: <t:{timem}:R>')
        if times:
            await asyncio.sleep(times)
            reason = '<@&998128479038095390> Bóng tối dưới lòng đất sẽ mở cửa sau ít phút'
            await channel.send(reason)

    #@commands.command()
    #@commands.has_permissions(administrator=True)
    #async def notification(self, ctx , channel:discord.TextChannel, time, *,text):
    #    """Thông báo theo giờ được chỉ định 
    #    time = hh:mm:ss"""
    #    if time:
    #        print(time)
    #        times = time.split(':')
    #        hours = times[0] , minutes = times[1], seconds= times[2]
    #        utc = datetime.datetime.strftime(datetime.datetime.utcnow()+ datetime.timedelta(hours=7), '%H:%M:%S' )
    #        uts = utc.split(':')
    #        if uts[0] == hours:
    #            if uts[1] == minutes:
    #                if seconds >= uts[2]:
    #                    await channel.send(text)
    #                    return
    #    else:
    #        await ctx.reply('thiếu thời gian')

async def setup(client):
    await client.add_cog(Timer(client))


