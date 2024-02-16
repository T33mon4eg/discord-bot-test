from typing import List

import disnake
from disnake.ext import commands
import sqlite3

connection = sqlite3.connect('birthdays.db')
cursor = connection.cursor()


class Menu(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")

        self._update_state()

    def _update_state(self) -> None:
        self.first_page.disabled = self.prev_page.disabled = self.index == 0
        self.last_page.disabled = self.next_page.disabled = self.index == len(self.embeds) - 1

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index = 0
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
    async def next_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index = len(self.embeds) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)



@commands.slash_command()
async def showallbdays(inter: disnake.ApplicationCommandInteraction):
    """Вывести весь список дней рождений"""
    cursor.execute("SELECT user_mention, birthdate FROM birthdays ORDER BY birthdate")
    # Получаем данные
    db_data = cursor.fetchall()

    # Разбиваем данные на списки по 10 записей
    chunked_data = [db_data[i:i + 10] for i in range(0, len(db_data), 10)]

    # Создаем список эмбедов на основе данных из БД
    embeds = []
    for i, chunk in enumerate(chunked_data):
        embed = disnake.Embed(
            title=f"**Все дни рождения**",
            description="\n".join([f"{index + 1 + i * 10}. {user} - `{date}`" for index, (user, date) in enumerate(chunk)]),
            colour=disnake.Colour.random(),
        )
        embed.set_thumbnail(inter.guild.icon)
        embeds.append(embed)

    # Отправляем первый эмбед с кнопками, также передаем список эмбедов в класс Menu
    await inter.response.send_message(embed=embeds[0], view=Menu(embeds))


def setup(bot):
    bot.add_slash_command(showallbdays)