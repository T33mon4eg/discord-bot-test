import disnake
from disnake.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='/', help_command=None, intents=disnake.Intents.all()) #префикс - обращение к командам бота, help_command - если захотим переписать базовую команду /help, ИНТЕНТЫ?))

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready to work!')

bot.load_extension('cogs.ping') #расширение .py указывать не нужно
#Для загрузки всех когов из папки cogs можно использовать bot.load_extensions('cogs')

# @bot.slash_command(description='Пинг-понг')
# async def ping(inter):
#     await inter.response.send_message('Понг!')

@bot.slash_command()
async def server(inter):
    await inter.response.send_message(
        f"Название сервера: {inter.guild.name}\nВсего участников: {inter.guild.member_count}"
    )

@bot.slash_command()
async def user(inter):
    await inter.response.send_message(f"Ваш тег: {inter.author}\nВаш ID: {inter.author.id}")

@bot.slash_command()
async def cute(inter):
    await inter.response.send_message('Ты милашка uWu')

TOKEN = os.environ['BOT_TOKEN']
bot.run(TOKEN)