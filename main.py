from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import config
from database import Session, User, Habit, Stats
import messages as msg
import keyboards as kb
from scheduler import scheduler, schedule_habit
from datetime import datetime, timedelta
import pytz
import re

# Инициализация бота
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Классы состояний FSM
class Form(StatesGroup):
    timezone = State()
    habit_name = State()
    frequency = State()
    days = State()
    interval = State()
    time = State()
    motivation = State()
    edit_name = State()
    edit_time = State()
    edit_frequency = State()

# ----------------- ОБРАБОТЧИКИ КОМАНД -----------------
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    session = Session()
    try:
        user = session.query(User).filter(User.chat_id == message.chat.id).first()
        if not user:
            await message.answer(msg.TEXTS['start'])
            await Form.timezone.set()
            await message.answer(msg.TEXTS['ask_timezone'], 
                                reply_markup=kb.timezone_keyboard())
        else:
            await message.answer(msg.TEXTS['main_menu'], 
                               reply_markup=kb.main_menu())
    finally:
        session.close()

# ----------------- СОЗДАНИЕ ПРИВЫЧКИ -----------------
@dp.message_handler(text="Создать привычку")
async def create_habit_start(message: types.Message):
    session = Session()
    try:
        user = session.query(User).filter(User.chat_id == message.chat.id).first()
        if not user:
            await message.answer("Сначала выполните /start")
            return
        
        habits_count = session.query(Habit).filter(Habit.user_id == user.id).count()
        if habits_count >= config.MAX_HABITS:
            await message.answer(msg.TEXTS['habit_limit'])
            return

        await Form.habit_name.set()
        await message.answer(msg.TEXTS['ask_habit_name'], 
                           reply_markup=types.ReplyKeyboardRemove())
    finally:
        session.close()

@dp.message_handler(state=Form.habit_name)
async def process_habit_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.answer(msg.TEXTS['ask_frequency'], 
                       reply_markup=kb.frequency_keyboard())

# Обработчик выбора частоты
@dp.callback_query_handler(lambda c: c.data.startswith('frequency'), state=Form.frequency)
async def process_frequency(callback: types.CallbackQuery, state: FSMContext):
    freq_type = callback.data.split('_')[1]
    async with state.proxy() as data:
        data['frequency'] = freq_type

    if freq_type == 'weekly':
        await Form.next()
        await callback.message.answer(msg.TEXTS['ask_days'], 
                                     reply_markup=kb.days_keyboard())
    elif freq_type == 'custom':
        await Form.interval.set()
        await callback.message.answer(msg.TEXTS['ask_interval'])
    else:
        await Form.time.set()
        await callback.message.answer(msg.TEXTS['ask_time'])
    
    await callback.answer()

# ----------------- ОБРАБОТКА ВРЕМЕНИ -----------------
@dp.message_handler(state=Form.time)
async def process_time(message: types.Message, state: FSMContext):
    if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message.text):
        await message.answer(msg.TEXTS['invalid_time'])
        return
    
    async with state.proxy() as data:
        data['time'] = message.text
    
    await Form.next()
    await message.answer(msg.TEXTS['ask_motivation'])

# ----------------- СОХРАНЕНИЕ ПРИВЫЧКИ -----------------
@dp.message_handler(state=Form.motivation, content_types=types.ContentTypes.ANY)
async def process_motivation(message: types.Message, state: FSMContext):
    session = Session()
    try:
        async with state.proxy() as data:
            # Сохранение в БД
            user = session.query(User).filter(User.chat_id == message.chat.id).first()
            habit = Habit(
                user_id=user.id,
                name=data['name'],
                frequency=data['frequency'],
                days=data.get('days', []),
                interval=data.get('interval', 1),
                time=data['time'],
                motivation_type=message.content_type,
                motivation_data=message.text if message.content_type == 'text' else 
                               message.voice.file_id if message.voice else 
                               message.video.file_id
            )
            session.add(habit)
            session.commit()
            
            # Планирование напоминаний
            await schedule_habit(habit, bot)
            
        await message.answer(msg.TEXTS['habit_created'], 
                           reply_markup=kb.main_menu())
    finally:
        session.close()
        await state.finish()

# ----------------- ЗАПУСК БОТА -----------------
if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
