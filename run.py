import nextcord
from nextcord.ext import commands
import json
import os

# Импорты утилит
from utilities.events.event_handler import setup as events_setup
from utilities.locate.main import locale
from utilities.ui.ui import UI

# Импорт модулей
from modules.moderation.main import setup as mod_setup

bot = commands.Bot(
    command_prefix='?',
    intents=nextcord.Intents.all(),
    case_insensitive=True
)

@bot.before_invoke
async def auto_detect_language(ctx):
    if not ctx.guild:
        await ctx.send("❌ Бот работает только на серверах!")
        raise commands.NoPrivateMessage()

    server_locale = str(ctx.guild.preferred_locale).lower()
    ctx.locale_code = 'ru' if 'ru' in server_locale else 'en'

def setup_utilities():
    events_setup(bot)
    print("Утилиты загружены")

def setup_modules():
    mod_setup(bot)
    print("Модули загружены")

@bot.event
async def on_ready():
    setup_utilities()
    setup_modules()
    print(f'Бот {bot.user} полностью готов к работе!')

# Запуск бота
os.makedirs("config", exist_ok=True)
try:
    with open('config/token.json') as f:
        bot.run(json.load(f)['token'])
except FileNotFoundError:
    print("Ошибка: файл config/token.json не найден!")
except json.JSONDecodeError:
    print("Ошибка: неверный формат token.json!")
except Exception as e:
    print(f"Неизвестная ошибка при запуске: {e}")