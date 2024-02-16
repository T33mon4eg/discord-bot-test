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
    """Информация о пользователе"""
    await inter.response.send_message(f"accentcolor: {user.accent_color}\n"
                                      f"accentcolour: {user.accent_colour}\n"
                                      f"avatar: {user.avatar.url}\n"
                                      f"banner: {user.banner}\n"
                                      f"bot: {user.bot}\n"
                                      f"color: {user.color}\n"
                                      f"colour: {user.colour}\n"
                                      f"created_at: {user.created_at}\n"
                                      f"defaultavatar: {user.default_avatar}\n"
                                      f"discriminator: {user.discriminator}\n"
                                      f"displayavatar: {user.display_avatar}\n"
                                      f"displayname: {user.display_name}\n"
                                      f"ID: {user.id}\n"
                                      f"mention: {user.mention}\n"
                                      f"name: {user.name}\n"
                                      f"publicflags: {user.public_flags}\n"
                                      f"system: {user.system}",
                                      ephemeral=True)

@bot.command()
async def cute(inter):
    """uWu"""
    await inter.send('Ты милашка uWu')


TOKEN = os.environ['BOT_TOKEN']
bot.run(TOKEN)