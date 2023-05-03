import disnake
from disnake.ext import commands


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def embed(self, inter):
        embed = disnake.Embed(title="Заголовок", description="Описание", colour=0x00ff00)
        embed.add_field(name="Поле 1", value="Значение 1", inline=False)
        embed.add_field(name="Поле 2", value="Значение 2", inline=True)
        embed.set_footer(text="Футер")
        embed.set_author(name="Хэдер")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_image(url='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzJmYWEyMzVhMjkzMGM1NjYyNzJkODVhNzkyOTczMWE0NDk5NzNkMCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/85qFstrbnyYcFbcoWD/giphy.gif')
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Embed(bot))