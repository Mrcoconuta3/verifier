from http import client
import disnake
from disnake.ext import commands
from config import Config

class sendmessage(commands.Cog):
    """Chỉ dành cho admin"""
    def __init__ (self, client):
        self.client = client
        
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, channel:disnake.TextChannel,* ,args='.'):
        """Chỉ dành cho admin"""
        if ctx.message.attachments:
            files=[await f.to_file() for f in ctx.message.attachments]
            try:
                await channel.send(args, files= files)
            except:
                await ctx.reply('Không thể gửi nội dung tệp tới: '+channel)

        else:
            try:
                await channel.send(args)
            except:
                await ctx.reply('Không thể gửi nội dung tới: '+channel)
    @say.error
    async def say_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Không thể gửi tin nhắn')

    @commands.command(category= "**Chỉ dành cho chủ sở hữu**")
    @commands.is_owner()
    async def dm (self,ctx, user:disnake.Member,  *,message= None):
        """Chỉ dành cho admin"""
        channel = await user.create_dm()
        def check(m):
            return m.channel.id == channel.id and m.author.id == user.id

        sent = False
        if message != None:
            if ctx.message.attachments:
                files=[await f.to_file() for f in ctx.message.attachments]
                try:
                    await channel.send(message, files= files)
                    sent = True
                except:
                    await ctx.reply('Không thể gửi nội dung tệp tới: '+user.name)
                    return

            else:
                try:
                    await channel.send(message)
                    sent = True
                except:
                    await ctx.send("Cant send message to "+user.name)
                    return

        else:
            if ctx.message.attachments:
                files=[await f.to_file() for f in ctx.message.attachments]
                try:
                    await channel.send(message, files= files)
                    sent = True
                except:
                    await ctx.reply('Không thể gửi nội dung tệp tới: '+user.name)
                    return

        if sent == True:
            await ctx.reply(f'Đã gửi nội dung tới {user.name}')

        msg = await self.client.wait_for('message', check = check, timeout = 86400)
        
        if msg:
            await ctx.send(f'Phản hồi từ {user.name} : {msg.content}')
            msg2 = await self.client.wait_for('message', check = check ,timeout = 120  )

            if msg2:
                await ctx.send(f'Phản hồi từ {user.name} : {msg2.content}')
                msg3 = await self.client.wait_for('message', check = check ,timeout = 120  )

                if msg3:
                    await ctx.send(f'Phản hồi từ {user.name} : {msg3.content}')
                    return

def setup(client):
    client.add_cog(sendmessage(client))
