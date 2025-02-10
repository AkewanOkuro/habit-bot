from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from messages import TEXTS
import config

def main_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Создать привычку"),
        KeyboardButton("Список привычек"),
        KeyboardButton("Статистика")
    )

def frequency_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Ежедневно", callback_data="frequency_daily"),
        InlineKeyboardButton("Еженедельно", callback_data="frequency_weekly"),
        InlineKeyboardButton("Каждые X дней", callback_data="frequency_custom")
    )

def days_keyboard():
    return InlineKeyboardMarkup(row_width=3).add(
        *[InlineKeyboardButton(day, callback_data=f"day_{i}") 
        for i, day in enumerate(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])]
    )

def habit_actions(habit_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Название", callback_data=f"edit_name_{habit_id}"),
        InlineKeyboardButton("Напоминания", callback_data=f"edit_reminder_{habit_id}"),
        InlineKeyboardButton("Мотивация", callback_data=f"edit_motivation_{habit_id}"),
        InlineKeyboardButton("Удалить", callback_data=f"delete_habit_{habit_id}")
    )

def reminder_actions(habit_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Выполнил", callback_data=f"done_{habit_id}"),
        InlineKeyboardButton("💡 Мотивация", callback_data=f"motivate_{habit_id}"),
        InlineKeyboardButton("❌ Не выполнил", callback_data=f"missed_{habit_id}")
    )

def timezone_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for tz_name in config.TIMEZONES:
        keyboard.add(InlineKeyboardButton(tz_name, callback_data=f"tz_{tz_name}"))
    return keyboard
