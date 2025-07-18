import json
from pathlib import Path


class LocaleManager:
    def __init__(self):
        self.languages = {}
        self._load_languages()

    def _load_languages(self):
        lang_dir = Path(__file__).parent / 'languages'
        lang_dir.mkdir(exist_ok=True)  # Создаем папку, если её нет

        for lang_file in lang_dir.glob('*.json'):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.languages[lang_code] = json.load(f)
            except json.JSONDecodeError:
                print(f"Ошибка в файле {lang_file}! Проверьте синтаксис JSON.")

    def get(self, key: str, lang_code: str, **kwargs) -> str:
        # Используем английский как fallback, если язык не найден
        lang_data = self.languages.get(lang_code, self.languages.get('en', {}))

        # Получаем сообщение или сообщение об ошибке
        message = lang_data.get(key, f"[Ключ '{key}' не найден для языка '{lang_code}']")

        # Форматируем, если есть kwargs
        try:
            return message.format(**kwargs) if kwargs else message
        except KeyError:
            return f"[Ошибка: неверные параметры для ключа '{key}']"


locale = LocaleManager()