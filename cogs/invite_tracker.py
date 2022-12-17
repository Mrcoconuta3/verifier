import datetime
import discord
import asyncio
from discord.ext import commands
from config import Config


class invite_tracker(commands.Cog):
    """
    Keep track of your invites
    """
    def __init__(self, bot):
        self.bot = bot
        self.logs_channel = Config.welcome_channel
        self.version = "1.0.0"

        self.invites = {}
        bot.loop.create_task(self.load())

    async def load(self):
        await self.bot.wait_until_ready()
        # load the invites
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if int(member.guild.id) != int(Config.guild_id):
            return
        logs = self.bot.get_channel(int(self.logs_channel))
        eme = discord.Embed(description=f"Chào mừng thành viên thứ {len(list(member.guild.members))}", color=0x03d692)
        eme.set_author(name=str(member), icon_url=member.display_avatar.url)
        eme.set_thumbnail(url= f"{member.display_avatar.url}")
        eme.set_footer(text="ID: " + str(member.id))
        eme.timestamp = datetime.datetime.now()
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses < self.find_invite_by_code(invs_after, invite.code).uses:
                    eme.add_field(name="Used invite",
                                  value=f"Lời mời từ: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\nCode: `{invite.code}`\nSố lần sử dụng: ` {str(invite.uses)} `", inline=False)
        except:
            pass
        await logs.send(embed=eme)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logs = self.bot.get_channel(int(self.logs_channel))
        eme = discord.Embed(description=f"Vừa rời đi nhóm còn {len(list(member.guild.members))} thành viên", color=0xff0000, title=" ")
        eme.set_author(name=str(member), icon_url=member.display_avatar.url)
        eme.set_footer(text="ID: " + str(member.id))
        eme.timestamp = member.joined_at
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses > self.find_invite_by_code(invs_after, invite.code).uses:
                    eme.add_field(name="Used invite",
                                  value=f"Được mời bởi: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\nCode: `{invite.code}`\nSố lần sử dụng: ` {str(invite.uses)} `", inline=False)
        except:
            pass
        await logs.send(embed=eme)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            self.invites[guild.id] = await guild.invites()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.invites.pop(guild.id)
        except:
            pass


async def setup(client):
    await client.add_cog(invite_tracker(client))
