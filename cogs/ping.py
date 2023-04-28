import disnake
from disnake.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Получить текущую задержку бота."""
        await inter.response.send_message(f'Понг! {round(self.bot.latency * 1000)}мс')

def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot)) # функция setup, чтобы disnake мог загружать ког, когда он будет добавлен в bot.py