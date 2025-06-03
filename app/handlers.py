import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.reply_buttons as kbr
import app.inline_buttons as kbi
from sources import src
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from parser import parser

class Key(StatesGroup):
    word = State()


router = Router()

@router.message(CommandStart()) 
async def start_handler(message: Message):
    await message.answer(f"Привет👋,{message.from_user.username} ,Чем могу быть полезен?", 
        reply_markup=kbr.unit)

@router.message(F.text == 'Начать поиск')  
async def key_word(message: Message, state: FSMContext):
    await message.answer('Введите ключевое слово:')
    await state.set_state(Key.word)

@router.message(Key.word)
async def channel_menu(message: Message, state: FSMContext):
    await state.update_data(keyword=message.text.strip())
    await message.answer('Выберите источник:', reply_markup=kbi.channels)

@router.callback_query(F.data.in_(src.keys()))
async def get_chan(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keyword = data.get('keyword', '')  
    channel_link = src[callback.data]
    await callback.answer("Идет поиск...")
    
    try:
        with ThreadPoolExecutor() as pool:
            result = await asyncio.get_event_loop().run_in_executor(
                pool, 
                parser, 
                channel_link,
                keyword 
            )
            
        if len(result) > 4000:  
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            for part in parts:
                await callback.message.answer(part)
                await asyncio.sleep(1)  
        else:
            await callback.message.answer(result)
            
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()