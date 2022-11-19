import discord
from discord.ext import commands
from config import Config

prefix = Config.prefix

def replacement( a , b , c):
        a =str(a)
        b =str(b)
        c =str(c)

        a1=float(a.replace(',','.'))
        b1=float(b.replace(',','.'))
        c1=float(c.replace(',','.'))
        return a1,b1,c1

class calc(commands.Cog):
    """ Tính Toán Đội Hình"""
    def __init__(self, client):
        self.client = client
    
    @commands.command(name= "calc",category = "Lệnh có thể dùng" ,help = f'** Tính toán Đội hình **\n``{prefix}calc <Tổng> [%Bộ Binh] [%Lính Xe] [%Cung Thủ]``')
    async def calc(self, ctx, t:int , a:str=None, b:str=None , c:str=None):
        try:
            print (a,b,c)
            if a is None:
                result_inf_default =int((t*60)/100) 
                result_car_default =int((t*10)/100)
                result_range_default =int((t*30)/100)
                embed= discord.Embed(title="", description =f"**Bộ Binh**: {result_inf_default} \n**Lính Xe**: {result_car_default} \n**Cung Thủ**: {result_range_default}", color =0x9208ea)
                embed.add_field(name = f"Tổng:",value=f"{t}",inline= False)
                embed.set_footer(text="Đội hình Phương trận Mặc Định 60/10/30")
                await ctx.reply(embed=embed)
            if a and b and c is not None:
                a1, b1, c1 = replacement(a , b , c)
                if a1+b1+c1 ==100:
                    result_inf =int((t*a1)/100) 
                    result_car =int((t*b1)/100)
                    result_range =int((t*c1)/100)
                    embed= discord.Embed(title="", description =f"**Bộ Binh**: {result_inf} \n**Lính Xe**: {result_car} \n**Cung Thủ**: {result_range}", color =0x9208ea)
                    embed.add_field( name= f"Tổng: ", value = f"{t}" , inline= False)
                    embed.set_footer(text=f"Đội hình Phương trận {a1}/{b1}/{c1} ")
                    await ctx.reply(embed=embed)    
                else:
                    await ctx.reply('``Syntax Error: 3 chỉ số cuối phải là phần trăm lính (Tổng 100%)``')
        except:
            await ctx.reply('`Thiếu giá trị tổng hoặc không tìm thấy kết quả`')


async def setup(client):
    await client.add_cog(calc(client))
