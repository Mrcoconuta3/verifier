import disnake
from disnake.ext import commands
from disnake.errors import Forbidden
from config import Config


async def send_embed(ctx, embed):

    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """Shows this embed"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    # @commands.client_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Shows all modules of that client"""
        prefix = Config.prefix

        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(Config.owner).mention

            except AttributeError as e:
                owner = owner

            # starting to build embed
            emb = disnake.Embed(title='Commands and modules', color=disnake.Color.blue(),
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':smiley:\n')

            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.client.cogs:
                cogs_desc += f'`{cog}` {self.client.cogs[cog].__doc__}\n'

            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.client.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # setting information about author
            emb.add_field(name="About", value=f"Based on disnake.py.\n\
                                    This version of it is maintained by {owner}\n")
            emb.set_footer(text=f"Discord Bot "+self.client.user.name)

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.client.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = disnake.Embed(title=f'{cog} - Commands', description=self.client.cogs[cog].__doc__,
                                        color=disnake.Color.green())

                    # getting commands from cog
                    for command in self.client.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = disnake.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=disnake.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = disnake.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=disnake.Color.orange())

        else:
            emb = disnake.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                            "Would you please be so kind to report that issue to me on github?\n"
                                            "https://github.com/nonchris/disnake-fury/issues\n"
                                            "Thank you! ~Chris",
                                color=disnake.Color.red())

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(client):
    client.add_cog(Help(client))