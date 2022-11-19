import discord
from discord.ui import* 
from discord.ext import commands
from datetime import datetime
import random, asyncio
from config import *

import time
        
verify_log = Config.verify_log
role_name = Config.verify_role
role_un = Config.role_un


async def send_log(channel, content, condition):
    if condition == True:
        return await channel.send(content)
    else:
        return await channel.send(embed=content)

class Modal(Modal, title='Xác thực'):
    def __init__(self, answ, ques, timetoend, channel , entry, not_entry):
        super().__init__(timeout= 120)
        self.time = timetoend
        self.channel = channel
        self.entry = entry
        self.stay = not_entry
        self.answ = answ
        self.ques = ques

        self.question = TextInput(
            label="Thời gian 25 giây ->Câu hỏi",
            max_length=1,
            placeholder=self.ques,
            required=False,
        )
        self.add_item(self.question)

        self.answer= TextInput(label='Vui lòng viết lại dòng trên bằng Tiếng Việt', style=discord.TextStyle.paragraph, placeholder="( ´◔ ω◔`)", required= True, min_length=4, max_length= 60)
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title= self.title,timestamp = datetime.now())
        embed.set_author(name = interaction.user , icon_url= interaction.user.avatar)
        textansw = f"{self.answer}"

        if int(time.time()) - self.time > 25:
            #Vượt quá thời gian cho phép
            em_timeout = discord.Embed(title = "Vượt quá thời gian", description = f"{interaction.user.mention}", color = 0xE47220)
            em_timeout.set_thumbnail(url= interaction.user.display_avatar.url)
            await send_log(self.channel, content= em_timeout, condition=False )
            return await interaction.response.send_message(f'{interaction.user.mention} Bạn đã hết thời gian trả lời câu hỏi. Vui lòng thử lại sau', ephemeral= True)
        
        elif self.answ in textansw.lower():
            #Đáp án dúng
            embed.description=f"**{self.answer}**\nĐáp án chính xác"
            embed.color= 0x45f248
            try:
                await interaction.user.remove_roles(self.stay)
                await interaction.user.add_roles(self.entry)
            except:
                pass
            
            await interaction.response.send_message(f'Thanks for your response',embed=embed, ephemeral=True, delete_after= 10)
            await send_log(self.channel, content= f"✅{interaction.user.name} vừa xác minh", condition=True )
        else:
            #Đáp án sai
            embed.description=f"**{self.answer}**\nĐáp án sai, vui lòng thử lại"
            embed.color= 0xFF0000
            await interaction.response.send_message(f'Thanks for your response',embed=embed, ephemeral=True)
            em_fail = discord.Embed(title = "Oops!", description = f"{interaction.user.mention} không xác minh thành công", color = 0xFF0000)
            em_fail.set_thumbnail(url= interaction.user.display_avatar.url)
            await send_log(self.channel, content=em_fail, condition= False)

    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:
        await interaction.response.send_message(f'Có lỗi xảy ra. Vui lòng thử lại', ephemeral= True)
        return await super().on_error(interaction, error)

    async def on_timeout(self) -> None:
        print('USER TIMEOUT!')
        return 

class Buttons(discord.ui.View):
    def __init__(self,client):
        super().__init__()
        self.client = client

    @discord.ui.button(label="Bắt đầu xác thực",style=discord.ButtonStyle.green)
    async def green_button(self,interaction:discord.Interaction, button:discord.Button):
        i = random.randrange(0, (len(QA.answer))-1)
        ques = QA.quez[i]
        answ = QA.answer[i]
        timetoend = int(time.time())
        vff = self.client.get_channel(int(verify_log))
        guild = interaction.guild
        try:
            verify = discord.utils.get(guild.roles, name=role_name)
            not_verify = discord.utils.get(guild.roles, name=role_un)
        except:
            return print("Role Not Found\nTerminating Process")

        await vff.send(f"💠{interaction.user.name} is verifying")
        await interaction.response.send_modal(Modal(answ, ques, timetoend, vff, verify, not_verify))

class verifys(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @commands.command(description="Send a verify button to the channel")
    @commands.has_permissions(administrator=True)
    async def verifybutton(self, ctx):
        await ctx.reply(view=Buttons(self.client))

async def setup(client):
    await client.add_cog(verifys(client))