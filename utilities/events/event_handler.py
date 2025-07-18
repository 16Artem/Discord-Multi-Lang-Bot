import nextcord
from nextcord.ext import commands
from utilities.ui.ui import UI
from utilities.locate.main import locale
from typing import Optional


class EventHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ui = UI

    async def on_ready(self) -> None:
        """Вызывается при готовности бота"""
        print(f'✅ Бот {self.bot.user} готов!')
        print(f'🆔 ID: {self.bot.user.id}')
        print(f'📊 Серверов: {len(self.bot.guilds)}')
        print(f'👥 Пользователей: {sum(g.member_count for g in self.bot.guilds)}')

        activity = nextcord.Game(name=f"?help | {len(self.bot.guilds)} серверов")
        await self.bot.change_presence(activity=activity)

    async def on_connect(self) -> None:
        """Вызывается при подключении к Discord"""
        print("🌐 Бот подключился к Discord")

    async def on_disconnect(self) -> None:
        """Вызывается при отключении от Discord"""
        print("⚠️ Бот отключился от Discord")

    async def on_resumed(self) -> None:
        """Вызывается при восстановлении соединения"""
        print("♻️ Сессия бота восстановлена")

    async def on_message(self, message: nextcord.Message) -> None:
        """Обрабатывает все сообщения"""
        if message.author.bot:
            return

        await self.bot.process_commands(message)

    async def on_message_delete(self, message: nextcord.Message) -> None:
        """Логирует удаление сообщений"""
        if message.author.bot:
            return

        log_msg = (
            f"🗑️ Сообщение удалено в #{message.channel.name}\n"
            f"👤 Автор: {message.author.display_name}\n"
            f"📝 Содержимое: {message.content[:100]}"
        )
        print(log_msg)

    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message) -> None:
        """Логирует редактирование сообщений"""
        if before.author.bot or before.content == after.content:
            return

        log_msg = (
            f"✏️ Сообщение отредактировано в #{before.channel.name}\n"
            f"👤 Автор: {before.author.display_name}\n"
            f"📝 Было: {before.content[:100]}\n"
            f"📝 Стало: {after.content[:100]}"
        )
        print(log_msg)

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Обрабатывает ошибки команд"""
        if isinstance(error, commands.CommandNotFound):
            return

        locale_code = getattr(ctx, 'locale_code', 'en')

        if isinstance(error, commands.MissingPermissions):
            msg = locale.get("error.missing_perms", locale_code)
        elif isinstance(error, commands.BotMissingPermissions):
            msg = locale.get("error.bot_missing_perms", locale_code)
        elif isinstance(error, commands.CommandOnCooldown):
            msg = locale.get("error.cooldown", locale_code, retry_after=round(error.retry_after))
        else:
            msg = locale.get("error.generic", locale_code, error=str(error))

        await ctx.send(embed=self.ui.error_embed(description=msg), delete_after=10)
        print(f"⚠️ Ошибка команды: {error}")

    async def on_member_join(self, member: nextcord.Member) -> None:
        """Приветствие новых участников"""
        print(f"👋 Участник присоединился: {member.display_name}")

        # Пример приветственного сообщения
        welcome_channel = nextcord.utils.get(member.guild.text_channels, name="welcome")
        if welcome_channel:
            msg = locale.get(
                "welcome.message",
                getattr(member.guild, 'locale_code', 'en'),
                user=member.mention
            )
            await welcome_channel.send(embed=self.ui.info_embed("Добро пожаловать!", msg))

    async def on_member_remove(self, member: nextcord.Member) -> None:
        """Логирует выход участника"""
        print(f"👋 Участник вышел: {member.display_name}")

    async def on_guild_join(self, guild: nextcord.Guild) -> None:
        """Действия при добавлении бота на сервер"""
        print(f"📥 Бот добавлен на сервер: {guild.name} (ID: {guild.id})")

        # Отправляем сообщение владельцу
        owner = guild.owner
        if owner:
            try:
                embed = self.ui.info_embed(
                    "Спасибо за добавление бота!",
                    "Используйте `?help` для списка команд.\n"
                    "Настройте бота под ваш сервер!"
                )
                await owner.send(embed=embed)
            except:
                pass

    async def on_guild_remove(self, guild: nextcord.Guild) -> None:
        """Логирует удаление бота с сервера"""
        print(f"📤 Бот удален с сервера: {guild.name} (ID: {guild.id})")

    async def on_member_ban(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """Логирует баны"""
        print(f"🔨 Пользователь забанен: {user.name} на сервере {guild.name}")

    async def on_member_unban(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """Логирует разбаны"""
        print(f"🔓 Пользователь разбанен: {user.name} на сервере {guild.name}")

    async def on_voice_state_update(
            self,
            member: nextcord.Member,
            before: nextcord.VoiceState,
            after: nextcord.VoiceState
    ) -> None:
        """Отслеживает изменения голосовых каналов"""
        if before.channel != after.channel:
            action = "подключился" if not before.channel else "перешел"
            channel = after.channel.name if after.channel else "неизвестный канал"
            print(f"🎤 {member.display_name} {action} в {channel}")

    async def on_reaction_add(
            self,
            reaction: nextcord.Reaction,
            user: nextcord.Member
    ) -> None:
        """Обрабатывает добавление реакций"""
        if user.bot:
            return

        print(f"👍 Реакция {reaction.emoji} добавлена к сообщению")

    async def on_reaction_remove(
            self,
            reaction: nextcord.Reaction,
            user: nextcord.Member
    ) -> None:
        """Обрабатывает удаление реакций"""
        if user.bot:
            return

        print(f"👎 Реакция {reaction.emoji} удалена с сообщения")


def setup(bot: commands.Bot) -> None:
    """Регистрирует все обработчики событий"""
    handler = EventHandler(bot)

    # Полный список событий
    events = [
        'on_ready',
        'on_connect',
        'on_disconnect',
        'on_resumed',
        'on_message',
        'on_message_delete',
        'on_message_edit',
        'on_command_error',
        'on_member_join',
        'on_member_remove',
        'on_guild_join',
        'on_guild_remove',
        'on_member_ban',
        'on_member_unban',
        'on_voice_state_update',
        'on_reaction_add',
        'on_reaction_remove',
    ]

    for event in events:
        bot.add_listener(getattr(handler, event))