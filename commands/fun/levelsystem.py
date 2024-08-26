import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

from utils.configmanager import gconfig


def profile_gen(interaction:discord.Interaction,bg:str):
    # Variables for customization
    background_image_path = bg  # Path to your background image
    font_color = (255, 255, 255)  # Font color (RGB)
    font_path = "data/fonts/Freedom.ttf"  # Path to your font file
    font_size = 50  # Font size for all texts
    fixed_size = (710, 800)  # Fixed size for the profile image

    # Texts and positions
    texts = [
        (interaction.user.name, (50, 50)),  # (text, (x, y) position)
        ("Level: {Lorem Ipsum}", (50, 150)),
        ("Hello, World!", (50, 250)),
    ]

    # Load and resize the background image
    if background_image_path.startswith("#"):
        background = Image.new('RGB', fixed_size, color=bg)
    else:
        background = Image.open(background_image_path)
        background = background.resize(fixed_size, Image.ANTIALIAS)

    # Draw each text on the background
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(font_path, font_size)

    for text, position in texts:
        draw.text(position, text, font=font, fill=font_color)

    # Save the image
    if interaction.guild.id:
        background.save(f".cache/{interaction.user.id}-{interaction.guild.id}.png")
        return ".cache/{interaction.user.id}-{interaction.guild.id}.png"
    else:
        background.save(f".cache/{interaction.user.id}.png")
        return ".cache/{interaction.user.id}.png"
class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="global-leaderboard",description="Level Leaderboard")
    async def global_leaderboard(self,interaction:discord.Interaction):
        pass

    @app_commands.command(name="leaderboard",description="Server Leaderboard")
    async def leaderboard(self, interaction:discord.Interaction):
        if gconfig.get(interaction.guild.id,""):
            pass

    @app_commands.command(name="profile",description="Your profile")
    async def profile(self,interaction: discord.Interaction, minimal:bool=True):
        if minimal:
            image = profile_gen(interaction=interaction,bg="data/prof-bgs/Default.png")  # noqa: E501
            embed = discord.Embed(title=f"Profile of {interaction.user.name}")
            file = discord.File(image, filename="profile.png")
            embed.set_image(url="attachment://profile.png")
            await interaction.response.send_message(embed=embed,file=file)
        else:
            await interaction.response.send_message("Not yet made", ephemeral=True)


async def setup(bot:commands.Bot):
    cog = LevelSystem(bot)
    await bot.add_cog(cog)
