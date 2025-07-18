# Discord-Multi-Lang-Bot
# Полная документация Discord бота

## Оглавление
1. [Введение](#введение)
2. [Установка и настройка](#установка-и-настройка)
3. [Архитектура проекта](#архитектура-проекта)
4. [Команды бота](#команды-бота)
5. [Система локализации](#система-локализации)
6. [UI компоненты](#ui-компоненты)
7. [Обработчики событий](#обработчики-событий)
8. [Разработка модулей](#разработка-модулей)
9. [Лицензия](#лицензия)
10. [Контрибьютинг](#контрибьютинг)

## Введение

Это многофункциональный Discord бот с модульной архитектурой, разработанный на Python с использованием библиотеки Nextcord. Бот предоставляет:

- 🛠 Инструменты модерации
- 🌍 Поддержку нескольких языков
- 🎨 Готовые UI компоненты
- 📊 Логирование событий
- 🔌 Легко расширяемую модульную систему

## Установка и настройка

### Требования
- Python 3.8+
- Nextcord 2.0+
- Git (опционально)

### Пошаговая установка

1. Клонирование репозитория:
```bash
git clone https://github.com/yourusername/your-bot.git
cd your-bot
```

2. Установка зависимостей:
```bash
pip install -r requirements.txt
```

3. Настройка конфигурации:
```bash
mkdir config
echo '{"token": "YOUR_BOT_TOKEN"}' > config/token.json
```

4. Запуск бота:
```bash
python run.py
```

### Конфигурационные файлы

- `config/token.json` - содержит токен бота
```json
{
  "token": "ваш_токен_бота"
}
```

## Архитектура проекта

```
discord-bot/
├── config/                 # Конфигурация
│   └── token.json          # Токен бота
├── languages/              # Локализации
│   ├── en.json            # Английский
│   └── ru.json            # Русский
├── modules/               # Модули бота
│   └── moderation/        # Модуль модерации
│       └── main.py        # Реализация команд
├── utilities/             # Вспомогательные системы
│   ├── events/            # Обработчики событий
│   ├── locate/            # Локализация
│   └── ui/                # UI компоненты
├── run.py                 # Основной файл
└── README.md              # Документация
```

## Команды бота

### Модерация
- `?clear [amount=5]` - Удаляет сообщения
  - Параметры:
    - `amount`: количество сообщений (1-100)
  - Требуемые права: `manage_messages`
  - Пример: `?clear 10`

### Тикеты
- `?setup_tickets` - Настройка системы тикетов
- `?add_support_role @role` - Добавление роли поддержки

## Система локализации

### Добавление нового языка

1. Создайте файл в `languages/` (например `fr.json`)
2. Скопируйте структуру из `en.json`
3. Добавьте переводы для всех ключей

### Использование в коде
```python
from utilities.locate.main import locale

message = locale.get(
    "welcome.message", 
    ctx.locale_code,
    user=member.mention
)
```

## UI компоненты

### Эмбеды
```python
UI.success_embed("Операция выполнена!")
UI.error_embed("Произошла ошибка")
UI.info_embed("Информация", "Подробное описание")
```

### Кнопки
```python
view = UI.create_confirm(callback_function)
await ctx.send("Подтвердите действие:", view=view)
```

### Выпадающие меню
```python
options = [("Опция 1", "val1"), ("Опция 2", "val2")]
view = UI.create_dropdown(options, "Выберите вариант", callback)
```

## Обработчики событий

Бот обрабатывает следующие события:
- 📨 Сообщения (отправка, редактирование, удаление)
- 👥 Действия участников (вход/выход, баны)
- 🔊 Изменения голосовых каналов
- ⚙️ Изменения на сервере

Пример добавления обработчика:
```python
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
```

## Разработка модулей

### Создание нового модуля

1. Создайте папку в `modules/` (например `welcome/`)
2. Создайте файл `main.py` с классом Cog:
```python
from nextcord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def welcome(self, ctx):
        await ctx.send("Добро пожаловать!")

def setup(bot):
    bot.add_cog(WelcomeCog(bot))
```

3. Подключите модуль в `run.py`:
```python
from modules.welcome.main import setup as welcome_setup

def setup_modules():
    welcome_setup(bot)
    # другие модули...
```

