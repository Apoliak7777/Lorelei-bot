import logging

#import os
import discord
from discord import app_commands
from discord.ext import commands

from utils.autocomplete import autocomplete_verify_modes
from utils.configmanager import gconfig
from utils.emoji import string2emoji
from utils.helpmanager import HelpManager

logger = logging.getLogger("verifysystem")

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener("on_reaction_add")
    async def on_react(self, reaction:discord.Reaction, user):
        #if user.bot:
        #    return

        # Example: Reaction role logic
        #guild = reaction.message.guild
        pass

    @app_commands.command(name="verify-system",description="No bots in the server")
    @app_commands.default_permissions(administrator=True)
    @app_commands.autocomplete(mode=autocomplete_verify_modes)
    async def verify_system(
        self,
        interaction: discord.Interaction,
        title: str,
        description:str,
        role:discord.Role,
        channel: discord.TextChannel,
        mode: str = "button",
    ):
        if mode == "emoji":
            await interaction.response.send_message(
                content="Selected Emoji / Reaction",
                ephemeral=True,
            )
            embed = discord.Embed(
                title=title,
                description=description,
            )
            message = await channel.send(
                embed=embed,
            )
            message.add_reaction(string2emoji("✅"))  # type: ignore # Add a reaction to the message
            gconfig.set(
                interaction.guild.id, # type: ignore
                str(channel.id)+"-verifyemoji",
                "role",
                role.id,
            )
        elif mode == "button":
            await interaction.response.send_message(
                content="Selected Button",
                ephemeral=True,
            )
            embed = discord.Embed(
                title=title,
                description=description,
            )
            await channel.send(
                embed=embed,
                view=self.verify_button(),
            )
            logger.debug(role.id)
            gconfig.set(
                interaction.guild.id, # type: ignore
                str(channel.id)+"-verifybutton",
                "role",
                role.id,
            )
        elif mode == "captcha":
            await interaction.response.send_message(
                content="In progress :3",
                ephemeral=True,
            )
            embed = discord.Embed(
                title=title,
                description=description,
            )
            await channel.send(
                embed=embed,
                view=self.verify_captcha(),
            )
        elif mode == "teams":
            await interaction.response.send_message(
                content="In progress :)",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                content="Wrong type!",
                ephemeral=True,
            )

    class verify_button(discord.ui.View):
        def __init__(self)-> None:
            super().__init__(timeout=None)

        @discord.ui.button(
            label="Verify",
            style = discord.ButtonStyle.blurple,
            custom_id="verify",
        )
        async def verify(self, interaction: discord.Interaction, button: discord.ui.button): # type: ignore # noqa: E501
            #await interaction.response.send_message(content="Clicked :3",ephemeral=True) # noqa: E501
            try:
                role = gconfig.get(
                    interaction.guild.id, # type: ignore
                    str(interaction.channel.id)+"-verifybutton", # type: ignore
                    "role",
                )
                if role is None:
                    await interaction.response.send_message("interaction failed: role is none")  # noqa: E501
                # Convert the string back to an integer and role
                role_id = int(role)
                role = interaction.guild.get_role(role_id) # type: ignore

                await interaction.user.add_roles(role) # type: ignore
                await interaction.response.send_message(
                    content="Verified!",
                    ephemeral=True,
                )
            except discord.errors.Forbidden:
                await interaction.response.send_message(
                    content="Insufficient Permissions",
                )
            except Exception as e:
                logger.error(str(e))

    class verify_teams(discord.ui.View):
        def __init__(self)-> None:
            super().__init__(timeout=None)
    class verify_captcha(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

async def setup(bot: commands.Bot):  # noqa: C901
    cog = VerifySystem(bot)
    await bot.add_cog(cog)
    bot.add_view(VerifySystem.verify_button())
    hm = HelpManager()
    hmhelp = hm.new_help(
        group_name="Admin",
        command_name="verifysystem",
        description="Manage the verification system.",
    )
    hmhelp.set_help_page(
        page=1,
        title="Verify System",
        description="This command allows you to set up a verification system in your server. You can choose between different modes such as button, emoji, captcha, or teams.",  # noqa: E501
    )
