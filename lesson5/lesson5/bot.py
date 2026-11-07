from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datas import save_user
from datas import get_user_id

import os
from dotenv import load_dotenv


class Regstate(StatesGroup):
    name = State()
    phone_num = State()
    adress = State()
    age = State()

class ReklamaState(StatesGroup):
    text = State()
    photo = State()

load_dotenv()
api = os.getenv('API')
bot = Bot(api)
dp = Dispatcher()
admin_id = [5570471897,]


@dp.message(Command('start'))
async def send_salem(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'Salem - {message.from_user.first_name}')
    await message.answer('Введите ваше имя:')
    await state.set_state(Regstate.name)


@dp.message(Regstate.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите номер телефона:+998xxxxxxxxx')
    await state.set_state(Regstate.phone_num)


@dp.message(Regstate.phone_num)
async def get_phone(message: types.Message, state: FSMContext):
    nomer = message.text
    await state.update_data(phone_num=message.text)
    if  nomer.startswith('+998') and len(nomer)==13 and nomer[1:].isdigit() :#validation
        
        await message.answer('Введите адрес:')
        await state.set_state(Regstate.adress)
    else:
        await message.answer('Вы неправильно ввели номер. Повторите еще раз пж:')


@dp.message(Regstate.adress)
async def get_adress(message: types.Message, state: FSMContext):
    await state.update_data(adress=message.text)
    await message.answer('Введите возраст:')
    await state.set_state(Regstate.age)


@dp.message(Regstate.age)
async def get_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except (TypeError, ValueError):
        await message.answer('Возраст должен быть числом. Введите возраст:')
        return

    data = await state.get_data()
    name = data['name']
    phone_num = data.get('phone_num')
    adress = data.get('adress')
    username = message.from_user.username or 'without_username'
    user_id = message.from_user.id

    await save_user(name, phone_num, adress, age, user_id, username)
    await message.answer('Регистрация завершена!')
    await state.clear()





#for admin

@dp.message(Command('reklama'))
async def send_reklama(sms:types.Message,state:FSMContext):
    if sms.from_user.id in admin_id:
        await sms.answer(text='Reklama textin jiberin:')
        await state.set_state(ReklamaState.text)
@dp.message(ReklamaState.text)
async def save_text(sms:types.Message,state:FSMContext):
    await state.update_data(text=sms.text)
    await sms.answer(text='Suwret jiberin:')
    await state.set_state(ReklamaState.photo)
@dp.message(ReklamaState.photo)
async def save_photo(sms:types.Message,state:FSMContext):
    await state.update_data(suwret=sms.photo[0].file_id)
    await sms.answer(text='Boldi')
    reklama = await state.get_data()
    await state.clear()
    ids = await get_user_id()
    for i in ids:
            # print(i[0])#tuple
            await bot.send_photo(
                chat_id=i[0],
                caption=reklama['text'],
                photo=reklama['suwret']
            )

# @dp.message(Command('show_id'))
# async def show_id(sms:types.Message):
#     if sms.from_user.id in admin_id:
#         ids = await get_user_id()
#         for i in ids:
            # print(i[0])#tuple
    #         await bot.send_message(
    #             chat_id=i[0],
    #             text='Test'
    #         )
    # else:
        # await sms.answer(text='Sizde bul komandaga dostup joq')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())