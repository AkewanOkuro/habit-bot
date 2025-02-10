import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получить у @BotFather
DATABASE_URL = "sqlite:///habits.db"
MAX_HABITS = 10
TIMEZONES = {
    "Москва (+3)": "Europe/Moscow",
    "Калининград (+2)": "Europe/Kaliningrad",
    "Самара (+4)": "Europe/Samara",
    "Екатеринбург (+5)": "Asia/Yekaterinburg",
    "Новосибирск (+7)": "Asia/Novosibirsk"
}
