from discord.ext import commands
import datetime
import pytz


class TimeZone(commands.Cog):
    """Get time zone """

    def __init__(self, client):
        self.client = client
        self.client.setup = True
    @commands.command(aliases = ["Utc","utc","UTC"])
    async def utctime(self, ctx):
        utc_dt = datetime.datetime.utcnow()
        utc = datetime.datetime.strftime(utc_dt, '%d/%m/%Y %H:%M:%S' )
        vn = datetime.datetime.strftime(utc_dt + datetime.timedelta(hours=7), '%d/%m/%Y %H:%M:%S' )
        #vn_timezone = utc_dt.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
        #vn = datetime.datetime.strftime(vn_timezone, '%d/%m/%Y %H:%M:%S' )
        timess = (
            f"Giờ UTC: {utc}\n"
            f"(Asia/Ho_Chi_Minh): {vn}\n"
        )
        await ctx.reply(f"{timess}")

    @commands.command(aliases = ["time","thoi gian"],help = "*>time <Country>* \nEx:`>time Asia/Ho_Chi_Minh`")
    async def timezone(self, ctx , *,args):

        utc_dt = datetime.datetime.utcnow()
        try:
            tz = datetime.datetime.strftime(utc_dt.astimezone(pytz.timezone(f'{args}')), '%d/%m/%Y %H:%M:%S')
            await ctx.reply(f"{tz}")

        except:
            await ctx.reply(f"Không tìm thấy múi giờ {args}")

async def setup(client):
    await client.add_cog(TimeZone(client))
