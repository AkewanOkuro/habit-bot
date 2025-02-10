from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from database import Session
from aiogram import Bot
import config
import pytz

scheduler = AsyncIOScheduler()

async def schedule_habit(habit, bot: Bot):
    session = Session()
    try:
        user = session.query(User).filter(User.id == habit.user_id).first()
        tz = pytz.timezone(user.timezone)
        
        # Расчет времени
        hour, minute = map(int, habit.time.split(':'))
        
        if habit.frequency == 'daily':
            trigger = CronTrigger(hour=hour, minute=minute, timezone=tz)
        elif habit.frequency == 'weekly':
            trigger = CronTrigger(
                day_of_week=','.join(map(str, habit.days)),
                hour=hour,
                minute=minute,
                timezone=tz
            )
        elif habit.frequency == 'custom':
            trigger = CronTrigger(
                day=f'*/{habit.interval}',
                hour=hour,
                minute=minute,
                timezone=tz
            )
        
        scheduler.add_job(
            send_reminder,
            trigger=trigger,
            args=(bot, habit.id),
            id=f"habit_{habit.id}",
            replace_existing=True
        )
    finally:
        session.close()

async def send_reminder(bot: Bot, habit_id):
    session = Session()
    try:
        habit = session.query(Habit).get(habit_id)
        if habit:
            kb = keyboards.reminder_actions(habit.id)
            await bot.send_message(
                chat_id=habit.user_id,
                text=TEXTS['reminder'].format(habit=habit.name),
                reply_markup=kb
            )
    finally:
        session.close()
