import asyncio
from datetime import datetime
import datetime
import pytz
from distutils.command.config import config
from string import ascii_lowercase
import random
from config import Config
import disnake
from disnake.ext import commands

prefix = Config.prefix
token = Config.token
owner = Config.owner

utc_dt = datetime.datetime.utcnow()
vn_hours = pytz.timezone('Asia/Ho_Chi_Minh')
vn = f"{utc_dt.astimezone(vn_hours)}"

quez = [
    "con bo ko biet bay",
    "con meo thich bac ha",
    "con chim tha moi ve to",
    "gio dong lanh buot",
    "ban Lan thich boc dau",
    "be meo keu con cai nit",
    "sieu nhan Gao bien hinh thanh cong chua",
    "điền vào chỗ trống: cần cù thì bù __ __ "
]
answer = [
    "con bò không biết bay",
    "con mèo thích bạc hà",
    "con chim tha mồi về tổ",
    "gió đông lạnh buốt",
    "bạn lan thích bốc đầu",
    "bé mèo kêu còn cái nịt",
    "siêu nhân gao biến hình thành công chúa",
    "cần cù thì bù thông minh"
]

client = disnake.Client()

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=disnake.Intents.all())


client.setup = False
client.role_name = Config.verify_role
client.message_id = Config.message_id
client.channel_id = Config.channel
client.welcome_channel = Config.welcome_channel

@client.event
async def on_ready():
    print("Logged in as "+client.user.name)
    
@client.event
async def on_member_join(user):
    channel = client.get_channel(int(client.welcome_channel))
    embed= disnake.Embed(description=f"Chào mừng thành viên thứ {len(list(user.guild.members))}\n" , color=0xADD8E6 )
    embed.set_thumbnail(url= f"{user.avatar.url}")
    embed.set_author(name=f"{user.name} vừa tham gia", icon_url= f"{user.avatar.url}")
    embed.set_footer(text= f"{user.guild}", icon_url= f"{user.guild.icon.url}")
    embed.timestamp = datetime.datetime.now()

    await channel.send(embed=embed)


@client.event
async def on_member_remove(user):
    channel = client.get_channel(int(client.welcome_channel))
    embed= disnake.Embed(description=f"Nhóm còn {len(list(user.guild.members))} thành viên \n" , color=0xFFA500 )
    embed.set_thumbnail(url= f"{user.avatar.url}")
    embed.set_author(name=f"{user.name} vừa rời đi", icon_url= f"{user.avatar.url}")
    embed.set_footer(text= f"{user.guild}", icon_url= f"{user.guild.icon.url}")
    embed.timestamp = datetime.datetime.now()

    await channel.send(embed=embed)

@client.command()
async def setup(ctx):
    if ctx.author.id  == owner:
        try:
            message_id = int(client.message_id)
        except ValueError:
            return await ctx.send("Invalid Message ID passed")
        except Exception as e:
            raise e

        try:
            channel_id = int(client.channel_id)
        except ValueError:
            return await ctx.send("Invalid Channel ID passed")
        except Exception as e:
            raise e
        
        channel = client.get_channel(channel_id)
        
        if channel is None:
            return await ctx.send("Channel Not Found")
        
        message = await channel.fetch_message(message_id)
        
        if message is None:
            return await ctx.send("Message Not Found")
        
        await message.add_reaction("✅")
        await ctx.send("Setup Successful")
        
        client.setup = True
    else:
        pass

@client.event
async def on_message(message):
    if message.author == client.user or message.author == message.author.bot:
        return

    else:
        await client.process_commands(message)

    if (message.content.startswith(f'{prefix}huntme')):
        if message.author.id == owner:
            q = disnake.Embed(title='Xác thực người dùng ', description=f"`Vui lòng viết lại dòng dưới đây thành Tiếng Việt có dấu để tiếp tục\n `", color =0x9208ea)
            await message.channel.send(q)   
            

@client.event
async def on_raw_reaction_add(payload):
    if client.setup != True:
        return print(f"client is not setuped\nType {prefix}setup to setup the client")
    
    if payload.message_id == int(client.message_id):
        if str(payload.emoji) == "✅":
            guild = client.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = disnake.utils.get(guild.roles, name=client.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member.bot or member is None:
                return
            #Nhắn tin trực tiếp ,dm người dùng
            dmChannel = await member.send("Xin chào "+member.name)
            def check(message):
                return message.author == member and message.channel == dmChannel.channel
            #content = message.content.lower()
            #e = disnake.Embed(title='Xác thực người dùng '+member , description=f"Vui lòng viết lại dòng dưới đây thành Tiếng Việt có dấu để tiếp tục\n" )
            #async def askQuestion(question):
            i= random.randint(0,7)
            ques = quez[i]
            answ = answer[i]
            q =(f"**Thời gian 30s**. Vui lòng viết lại dòng dưới đây thành Tiếng Việt có dấu để tiếp tục\n `{ques}`")
    
            await member.send(q)
            print("Waiting for reply...")
            try:
                userReply = await client.wait_for('message', check=check,timeout= 30)
                userReply = userReply.content.lower()
                if userReply == answ:
                    #print (userReply)
                    try:
                        await member.add_roles(role)
                        await member.send('Đáp án chính xác, bạn có thể tiếp tục vào group')
                    except Exception as e:
                        await member.send('!Có lỗi xảy ra vui lòng liên hệ HarryNewYear để kiểm tra')
                        raise e
                elif userReply != answ:
                    #print (userReply)
                    await member.send('Sai đáp án vui lòng thử lại sau')
                else:
                    print (userReply)

            except asyncio.TimeoutError:
                await member.send("Bạn đã hết thời gian, vui lòng thử lại") 
            

@client.event
async def on_raw_reaction_remove(payload):
    if client.setup != True:
        return print(f"client is not setuped\nType {prefix}setup to setup the client")
    
    if payload.message_id == int(client.message_id):
        if str(payload.emoji) == "✅":
            guild = client.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = disnake.utils.get(guild.roles, name=client.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.remove_roles(role)
            except Exception as e:
                raise e

@client.command(aliases = ['message','nhan'])
async def dm (ctx, user:disnake.Member,* , message= None):
    if ctx.author.id == owner:
        if message != None:
            try:
                await user.send(message)
            except:
                await ctx.reply("Cant send message to "+user.name)
    else:
        pass
    
@client.command(name= "calc")
async def calc(ctx, t:int , a:int=None, b:int=None , c:int=None):
    if a is None:
            result_inf_default =int((t*60)/100) 
            result_car_default =int((t*10)/100)
            result_range_default =int((t*30)/100)
            embed= disnake.Embed(title="", description =f"**Bộ Binh**: {result_inf_default} \n**Lính Xe**: {result_car_default} \n**Cung Thủ**: {result_range_default}", color =0x9208ea)
            embed.add_field(name = f"Tổng:",value=f"{t}",inline= False)
            embed.set_footer(text="Đội hình Phương trận Mặc Định 60/10/30")
            await ctx.reply(embed=embed)
    if a and b and c is not None:
        if a+b+c ==100:
            result_inf =int((t*a)/100) 
            result_car =int((t*b)/100)
            result_range =int((t*c)/100)
            embed= disnake.Embed(title="", description =f"**Bộ Binh**: {result_inf} \n**Lính Xe**: {result_car} \n**Cung Thủ**: {result_range}", color =0x9208ea)
            embed.add_field( name= f"Tổng: ", value = f"{t}" , inline= False)
            embed.set_footer(text=f"Đội hình Phương trận {a}/{b}/{c} ")
            await ctx.reply(embed=embed)    
        else:
            await ctx.reply('``Syntax Error: 3 chỉ số cuối phải là phần trăm lính (Tổng 100%)``')
            
@client.command(aliases = ["Utc","utc","UTC"])
async def utctime(ctx):
    utc = datetime.datetime.strftime(utc_dt, '%d/%m/%Y %H:%M:%S' )
    #print (utc)
    await ctx.reply(f"Giờ UTC: {utc}\nGiờ ICT: {vn}")

client.run(token)
    
