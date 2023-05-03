import disnake
from disnake.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def clear(self, interaction, amount: int):
        """Команда очистки сообщений"""
        embed = disnake.Embed(title='Удаление', description=f'Удалено {amount} сообщений', colour=0x00ff00)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(Clear(bot))