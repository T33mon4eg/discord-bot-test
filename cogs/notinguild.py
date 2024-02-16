import os

import disnake
from disnake.ext import commands, tasks
import sqlite3
import datetime

connection = sqlite3.connect('birthdays.db')
cursor = connection.cursor()


class NotInGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remove_inactive_users.start()

    @tasks.loop(hours=24)
    async def remove_inactive_users(self):
        cursor.execute("SELECT user_id FROM birthdays")
        all_users = cursor.fetchall()

        guild_id = os.environ['GUILD_ID']  # Замените на фактический идентификатор вашего сервера
        guild = self.bot.get_guild(guild_id)

        if guild:
            for user_data in all_users:
                user_id = user_data[0]  # Получаем первый элемент кортежа, который представляет user_id

                # Проверяем, есть ли пользователь с указанным user_id на сервере
                member = guild.get_member(user_id)

                if not member:
                    # Если пользователь не найден на сервере, удаляем запись из БД
                    cursor.execute("DELETE FROM birthdays WHERE user_id=?", (user_id,))
                    connection.commit()
                    print(f"Пользователь с ID {user_id} удалён из БД")

    @remove_inactive_users.before_loop
    async def before_remove_inactive_users(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(NotInGuild(bot))

