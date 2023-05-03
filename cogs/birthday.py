import asyncio
import datetime
import os
import sqlite3

import disnake
from disnake.ext import commands, tasks
import giphy_client
from giphy_client.rest import ApiException


connection = sqlite3.connect('birthdays.db')
cursor = connection.cursor()

api_instance = giphy_client.DefaultApi()

api_key = os.environ['GIPHY_TOKEN']

channel_id = 1101119052488908891

class Birthday(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.birthday_check.start()
        cursor.execute("CREATE TABLE IF NOT EXISTS birthdays "
                       "(user_id INTEGER PRIMARY KEY, birthdate DATE, user_mention TEXT)")

    @commands.slash_command()
    async def set_birthday(self, ctx, user: disnake.Member, birthdate):
        """Записать в базу данных пользователя и его дату рождения в формате ДД.ММ.ГГГГ"""
        user_id = user.id
        user_mention = user.mention

        # парсим дату рождения из строки в формате ДД.ММ.ГГГГ
        try:
            birthdate_obj = datetime.datetime.strptime(birthdate, '%d.%m.%Y').date()
        except ValueError:
            await ctx.send("Неверный формат даты. Используйте формат ДД.ММ.ГГГГ (например 01.01.1900")
            return

        # сохраняем дату рождения в базу данных
        cursor.execute(
            "INSERT INTO birthdays (user_id, birthdate, user_mention) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET birthdate=excluded.birthdate",
            (user_id, birthdate_obj, user_mention))
        connection.commit()

        embed = disnake.Embed(title='Запись дня рождения',
                              description=f"Дата рождения {birthdate_obj} для пользователя {user.mention} сохранена.",
                              colour=user.colour)
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed, ephemeral=True)


    @commands.slash_command()
    async def check_all_bdays(self, inter):
        """Вывести полный список пользователей и их даты рождения"""
        cursor.execute("SELECT user_mention, birthdate FROM birthdays ORDER BY birthdate")
        full_list_bdays = cursor.fetchall()
        text = ''
        for _ in full_list_bdays:
            text += f'Пользователь {_[0]}, дата рождения {_[1]}\n'
        await inter.response.send_message(text)

    @tasks.loop(hours=24)
    async def birthday_check(self):
        cursor.execute("SELECT user_id FROM birthdays WHERE strftime('%m-%d', birthdate) == strftime('%m-%d', 'now')")
        all_result = cursor.fetchall()
        channel = self.bot.get_channel(channel_id)
        query = 'birthday'
        rating = 'g'
        if all_result != []:
            for _ in all_result:
                user_id = _[0]
                user = await self.bot.fetch_user(user_id)
                random_birthday_gif = api_instance.gifs_random_get(api_key, tag=query, rating=rating)
                gif_id = random_birthday_gif.data.id
                embed = disnake.Embed(title='🥳День рождения🥳',
                                      description=f"Сегодня празднует свой день рождения - {user.mention}",
                                      colour=0x00ff00 if user.banner else user.accent_color)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_image(url=f'https://media.giphy.com/media/{gif_id}/giphy.gif')
                await asyncio.sleep(5)
                await channel.send(embed=embed)

        # else:
        #     await channel.send('Никто сегодня не празднует день рождения :(')


    @birthday_check.before_loop
    async def before_birthday_check(self):
        await self.bot.wait_until_ready()

    @commands.slash_command()
    async def run_birthday_check(self, inter):
        """Запуск команды проверки дней рождений"""
        self.birthday_check.restart()
        await inter.response.send_message("Задача birthday_check запущена вручную")



def setup(bot):
    bot.add_cog(Birthday(bot))