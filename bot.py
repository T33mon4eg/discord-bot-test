import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv


load_dotenv()

bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all()) #префикс - обращение к командам бота, help_command - если захотим переписать базовую команду /help, ИНТЕНТЫ?))

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready to work!')
    await bot.change_presence(
        activity=disnake.Activity(type=disnake.ActivityType.watching, name='за работой техподдержки'),
        status=disnake.Status.dnd)

bot.load_extensions('cogs') #расширение .py указывать не нужно
#Для загрузки всех когов из папки cogs можно использовать bot.load_extensions('cogs')

@bot.slash_command()
async def server(inter):
    """Информация о сервере"""
    await inter.response.send_message(
        f"Название сервера: {inter.guild.name}\nВсего участников: {inter.guild.member_count}"
    )

@bot.slash_command()
async def user(inter, user: disnake.Member):
    """Информация о пользоваетеле"""
    await inter.response.send_message(f"Ваш тег: {user.display_name}\nВаш ID: {user.id}", ephemeral=True)

@bot.command()
async def cute(inter):
    """uWu"""
    await inter.send('Ты милашка uWu')


TOKEN = os.environ['BOT_TOKEN']
bot.run(TOKEN)