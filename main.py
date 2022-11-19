import asyncio
from datetime import datetime, timedelta
import datetime
import random
from config import Config , QA
import discord
from discord.ext import commands , tasks 
import pymongo
import os
from cogs.verification import Buttons

cluster = pymongo.MongoClient(os.getenv("Mongo_url"))

database = cluster["phong98"]
collection = database["verifycount"]

prefix = Config.prefix
owner = Config.owner
last_time = None

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=discord.Intents.all())
client.remove_command('help')

client.rm = False
client.setup = True
client.role_name = Config.verify_role
client.role_un = Config.role_un
client.message_id = Config.message_id
client.channel_id = Config.channel
client.welcome_channel = Config.welcome_channel
verify_log = Config.verify_log

reminder_channel = '923912095479767040'

@client.event
async def on_ready():
    print("Logged in as "+client.user.name)
    await client.change_presence(activity= discord.Game(f"{prefix}help|| Developer: Hárry#2958"))
    verify_channel = client.get_channel(int(client.channel_id))
    await verify_channel.send(view=Buttons(client))
                              
@client.event
async def on_message_edit(before, after):
    if before.author == client.user or before.author.bot:
        return
    channel = discord.utils.get(client.get_all_channels() ,name="nhật-ký")
    embed= discord.Embed(
        timestamp= datetime.datetime.now(),
        description=f"Tin nhắn của {before.author.name} đã được chỉnh sửa ở <#{before.channel.id}>.",
        color= 0xff8c00
    )

    embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.display_avatar.url)
    embed.set_footer(text=f"Author ID: {before.author.id} • Message ID: {before.id}")
    embed.add_field(name='Before:', value=before.content + "\u200b", inline=False)
    embed.add_field(name="After:", value=after.content + "\u200b", inline=False)
    if before.attachments:
        if len(before.attachments) == 1:
            file = before.attachments[0].url
            embed.set_image(url=f'{file}')
            await channel.send(embed= embed)
        else:
            i=0
            while (i < len(before.attachments)):
                file = before.attachments[i].url
                embed.set_image(url=f'{file}')
                await channel.send(embed=embed)
                i+=1
    else:
        await channel.send(embed= embed)

@client.event
async def on_message_delete(message):
    channel = discord.utils.get(client.get_all_channels() ,name="nhật-ký")
    if not message.attachments:
        embed= discord.Embed(
            title="Tin nhắn bị xoá",
            description=f"Tin nhắn của ``{message.author.name}`` | đã bị xoá ở <#{message.channel.id}>.",
            color= 0xFF0000 ,
            timestamp= datetime.datetime.now()
        )
        embed.set_author(name=f'{message.author}', icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f"Author ID: {message.author.id} • Message ID: {message.id}")
        embed.add_field(name='Nội dung', value=message.content+"\u200b", inline=False)

        await channel.send(embed= embed)

    if message.attachments:

        embed = discord.Embed(
            description=f"**Nội dung của ``{message.author.name}`` | bị xoá ở <#{message.channel.id}>**",
            timestamp = datetime.datetime.now(), color = 0xFF0000
            )
        embed.set_author(name=f"{message.author}", icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f"ID: {message.author.id} | Message ID: {message.id}")
        embed.add_field(name='Nội dung', value=message.content+"\u200b", inline=False)
        
        i=0
        while (i < len(message.attachments)):
                file = message.attachments[i].url
                embed.set_image(url=f'{file}')
                await channel.send(embed=embed)
                i+=1
    else:
        return    

@client.event
async def on_message(message):
    global last_time
    msg = message.content.lower()
    pingchannel = message.channel.id
    if message.author == client.user or message.author == message.author.bot:
        return
    else:
        await client.process_commands(message)
    if pingchannel == 936204379189567498:
        if message.author != client.user and message.author != message.author.bot:
            emoji = '\U0001F1FB\U0001F1F3'
            await message.add_reaction(emoji)
    if pingchannel == 923901039592226838:
        if last_time is None or  message.created_at - last_time > timedelta(seconds=15):
            last_time = message.created_at
            await message.channel.send(content = '<@&998128078217814117>' , delete_after = 2)
        
    if "cần cù bù" in msg:
        await message.channel.send("cần cù thì bù siêng năng\n                                      -Huấn Hoa Tử-")

    elif "monkey" in msg:
        await message.channel.send("Ummm... Monkey\n                                    -Master Oogway-") 
    elif "buồn" in msg:
        await message.channel.send("<:pepecry2:935791791846858782>")
    elif any(word in msg for word in QA.thic_word):
        await message.channel.send('🤣 ')
    elif any(word in msg for word in QA.miss_code):
        await message.channel.send("<:pepesign_concainit:924986455342870570>")
    else:
        pass  
            

@client.event
async def on_raw_reaction_add(payload):
    vff = client.get_channel(int(verify_log))
    if client.setup != True:
        return print(f"client is not setuped\nType {prefix}setup to setup the client")
    
    if payload.message_id == int(client.message_id):
        if str(payload.emoji) == "✅":
            guild = client.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=client.role_name)
                not_verify = discord.utils.get(guild.roles, name=client.role_un)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member.bot or member is None:
                return
            #Nhắn tin trực tiếp ,dm người dùng
            try:
                dmChannel = await member.send("Xin chào "+member.name)
            except:
                return print("I can't send message to this user")
            await vff.send(f"💠{member.name} is verifying")
            def check(message):
                return message.author == member and message.channel == dmChannel.channel
            
            i = random.randrange(0, (len(QA.answer))-1)
            ques = QA.quez[i]
            answ = QA.answer[i]
            q =(f"**Thời gian 25s**. Vui lòng viết lại dòng dưới đây thành Tiếng Việt có dấu để tiếp tục\n `{ques}`")
    
            await member.send(q)
            print(f"Waiting for reply of {member.name}...")
            if collection.count_documents({"userid":member.id}) == 0:
                collection.insert_one({"userid":member.id,"count":0})
            user_doc = collection.find_one({"userid":member.id})
        
            current_count = user_doc["count"]

            try:
                userReply = await client.wait_for('message', check=check,timeout= 25)
                userReply = userReply.content.lower()
                if answ in userReply :
                    if i == 24:
                        await member.send(file=discord.File('embankemdanhrang.jpg'))
                    if i == 25:
                        await member.send(file=discord.File('emchaodaica.jpg'))
                    print (userReply)
                    try:
                        await member.remove_roles(not_verify)
                        await member.add_roles(role)
                        await member.send('Đáp án chính xác, bạn có thể tiếp tục vào group')
                        await vff.send(f"✅{member.name} just verified")
                    except Exception as e:
                        await member.send('!Có lỗi xảy ra vui lòng liên hệ HarryNewYear để kiểm tra')
                        raise e
                elif userReply != answ:
                    print (userReply)
                    await member.send('Sai đáp án vui lòng thử lại sau')
                    new_count = current_count + 1
                    collection.update_one({"userid":member.id}, {"$set": {"count": new_count}}) 
                    
                    em_fail = discord.Embed(title = "Member", description = f"{member.mention} just failed the verification test | They now have {new_count} count!", color = 0xFF0000)
                    em_fail.set_thumbnail(url= member.display_avatar.url)
                    await vff.send(embed=em_fail)
                else:
                    print (userReply)

            except asyncio.TimeoutError:
                await member.send("Bạn đã hết thời gian, vui lòng thử lại") 
                new_count = current_count + 1
                collection.update_one({"userid":member.id}, {"$set": {"count": new_count}}) 
                
                em_timeout = discord.Embed(title = "Member", description = f"{member.mention} ran out of time in verification test | They now have {new_count} count!", color = 0xFF0000)
                em_timeout.set_thumbnail(url= member.display_avatar.url)
                await vff.send(embed=em_timeout)
            

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
                role = discord.utils.get(guild.roles, name=client.role_name)
                not_verify = discord.utils.get(guild.roles, name=client.role_un)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.add_roles(not_verify)
                await member.remove_roles(role)
            except Exception as e:
                raise e

@tasks.loop(seconds=4)
async def remindme():
    if client.rm != True:
        remindme.stop()
        print('Rm Stopped')
        return 
    utc = datetime.datetime.strftime(datetime.datetime.utcnow(), '%H:%M:%S' )
    uts = utc.split(':')
    #print(uts)
    if int(uts[0]) == 9 or int(uts[0]) == 15 or int(uts[0]) == 21 or int(uts[0]) == 3:
        #print('Hours check')
        if int(uts[1]) >= 58: 
            print("----It's time----")
            channel = client.get_channel(int(reminder_channel))
            await channel.send('<@&998128479038095390> Boss sẽ xuất hiện sau 2 phút nữa')
            await asyncio.sleep(120)
        else:
            #print('not now')
            pass
    else:
        #print('wait few hour')
        pass
    

@client.command()
@commands.is_owner()
async def reminding(ctx, value ):
    if value.lower() == 'enable' or value.lower() =='true':
        client.rm = True
        remindme.start()
        print('Reminder started')
        await ctx.reply('Thông báo đã được bật')
    elif value.lower() == 'disable' or value.lower() == 'false':
        client.rm = False
        remindme.stop()
        print('Reminder stopped')
        await ctx.reply('Thông báo đã được tắt')
    else:
        await ctx.reply("check again something isn't right")
    
@client.event
async def on_command_error(error):
    if isinstance(error, commands.CommandNotFound):
        pass

@client.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Load Cog: {filename[:-3]}")

client.run(os.getenv("token"))
    
