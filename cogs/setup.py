import random
import disnake
import asyncio
from disnake.ext import commands
from config import Config , QA


prefix= Config.prefix

class Setup(commands.Cog):
    """Setup verification to given channel_id and message_id"""

    def __init__(self, client):
        self.client = client
        self.client.setup = True
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"ReactionRoles ready.")

    @commands.is_owner()
    @commands.command(help = f'Setup the verification for users `[ {prefix}setup ]`\n**Only available for owner**')
    async def setup(self, ctx):
        try:
            message_id = int(Config.message_id)
        except ValueError:
            return  ctx.send("Invalid Message ID passed")
        except Exception as e:
            raise e

        try:
            channel_id = int(Config.channel)
        except ValueError:
            return  ctx.send("Invalid Channel ID passed")
        except Exception as e:
            raise e
        
        channel = self.client.get_channel(channel_id)
        
        if channel is None:
            return  ctx.send("Channel Not Found")
        
        message =  channel.fetch_message(message_id)
        
        if message is None:
            return  ctx.send("Message Not Found")
        
        await message.add_reaction("✅")
        await ctx.send("Setup Successful")
        
        self.client.setup = True

class verify(commands.Cog):
    def __init__(self, client):
        self.client = client
            
    @commands.command(help= f'``Enable or Disable verification [{prefix}verify enable/disable ]``')
    @commands.is_owner()
    async def verify(self,ctx, args):
        if args == "disable":
            self.client.setup = False
            await ctx.reply("Successfully disable verification")
        elif args == "enable":
            self.client.setup = True
            await ctx.reply("Successfully enable verification")
        else:
            await ctx.reply("Only 2 options available on **verify** command ``enable/disable``")

def setup(client):
    client.add_cog(Setup(client))
    client.add_cog(verify(client))
