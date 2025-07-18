import nextcord
from nextcord import Embed, Colour, Interaction
from nextcord.ui import View, Select, Button, Modal, TextInput, select, button

class UI:
    """Класс для удобного создания UI-элементов."""
    
    # ========== Эмбеды ==========
    @staticmethod
    def success_embed(description: str, title: str = None) -> Embed:
        """Создает зеленый эмбед для успешных действий."""
        embed = Embed(description=f"✅ {description}", color=Colour.green())
        if title:
            embed.title = title
        return embed

    @staticmethod
    def error_embed(description: str, title: str = None) -> Embed:
        """Создает красный эмбед для ошибок."""
        embed = Embed(description=f"❌ {description}", color=Colour.red())
        if title:
            embed.title = title
        return embed

    @staticmethod
    def info_embed(title: str, description: str) -> Embed:
        """Создает синий информационный эмбед."""
        return Embed(
            title=title,
            description=description,
            color=Colour.blue()
        )

    # ========== Выпадающие меню ==========
    class DropdownView(View):
        """View с выпадающим меню."""
        def __init__(self, options: list, placeholder: str = "Выберите вариант", callback = None):
            super().__init__(timeout=30.0)
            self.callback_func = callback
            self.add_item(UI.Dropdown(options, placeholder))

    class Dropdown(Select):
        """Кастомное выпадающее меню."""
        def __init__(self, options: list, placeholder: str):
            select_options = [
                nextcord.SelectOption(label=opt[0], value=opt[1])
                for opt in options
            ]
            super().__init__(
                placeholder=placeholder,
                options=select_options,
                min_values=1,
                max_values=1
            )

        async def callback(self, interaction: Interaction):
            if self.view.callback_func:
                await self.view.callback_func(interaction, self.values[0])
            else:
                await interaction.response.send_message(
                    f"Вы выбрали: **{self.values[0]}**",
                    ephemeral=True
                )

    @staticmethod
    def create_dropdown(options: list, placeholder: str = "Выберите вариант", callback = None) -> DropdownView:
        """Создает View с выпадающим меню."""
        return UI.DropdownView(options, placeholder, callback)

    # ========== Кнопки ==========
    class ConfirmView(View):
        """View с кнопками подтверждения."""
        def __init__(self, callback):
            super().__init__(timeout=30.0)
            self.callback_func = callback

        @button(label="Да", style=nextcord.ButtonStyle.green)
        async def yes(self, button: Button, interaction: Interaction):
            await self.callback_func(interaction, True)
            self.stop()

        @button(label="Нет", style=nextcord.ButtonStyle.red)
        async def no(self, button: Button, interaction: Interaction):
            await self.callback_func(interaction, False)
            self.stop()

    @staticmethod
    def create_confirm(callback) -> ConfirmView:
        """Создает View с кнопками подтверждения."""
        return UI.ConfirmView(callback)

    @staticmethod
    def create_link_button(label: str, url: str) -> View:
        """Создает View с кнопкой-ссылкой."""
        view = View()
        view.add_item(Button(label=label, url=url))
        return view

    # ========== Модальные окна ==========
    class TextInputModal(Modal):
        """Модальное окно с текстовым полем."""
        def __init__(self, title: str, label: str, placeholder: str, callback = None):
            super().__init__(title=title, timeout=300)
            self.callback_func = callback
            self.input = TextInput(
                label=label,
                placeholder=placeholder,
                required=True
            )
            self.add_item(self.input)

        async def callback(self, interaction: Interaction):
            if self.callback_func:
                await self.callback_func(interaction, self.input.value)
            else:
                await interaction.response.send_message(
                    f"Вы ввели: **{self.input.value}**",
                    ephemeral=True
                )

    @staticmethod
    def create_modal(title: str, label: str, placeholder: str, callback = None) -> TextInputModal:
        """Создает модальное окно."""
        return UI.TextInputModal(title, label, placeholder, callback)