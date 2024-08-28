from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = '7217501846:AAF0*...*'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    physical_activity = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью")



@dp.message_handler(text="Calories")
async def set_age(message):
    await message.answer("Введите свой возраст: ")
    await UserState.age.set()


@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост: ")
    await UserState.growth.set()


@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес: ")
    await UserState.weight.set()


@dp.message_handler(state= UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer("Введите свой пол(М,Ж): ")
    await UserState.gender.set()


@dp.message_handler(state= UserState.gender)
async def set_physical_activity(message, state):
    await state.update_data(gender=message.text)
    await message.answer(f"Выберите свой уровень активности(цифра):\n"
                         f"1. У вас нет физических нагрузок и сидячая работа\n"
                         f"2. Вы совершаете небольшие пробежки или делаете легкую гимнастику 1–3 раза в неделю\n"
                         f"3. Вы занимаетесь спортом со средними нагрузками 3–5 раз в неделю\n"
                         f"4. Вы полноценно тренируетесь 6–7 раз в неделю\n"
                         f"5. Ваша работа связана с физическим трудом, вы тренируетесь 2 раза в день"
                         f" и включаете в программу тренировок силовые упражнения")
    await UserState.physical_activity.set()


@dp.message_handler()
async def all_message(message):
    await message.answer("Отправь мне слово 'Calories', чтобы сделать рассчет")


@dp.message_handler(state= UserState.physical_activity)
async def send_calories(message, state):
    await state.update_data(physical_activity=message.text)
    data = await state.get_data()
    total_calories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']), 2)
    if data['gender'].upper() == 'Ж':
        total_calories_activity = total_calories - 161
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в состоянии покоя для нормального функционирования:"
                             f"{total_calories_activity}")
    else:
        total_calories_activity = total_calories + 5
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в состоянии покоя для нормального функционирования:"
                             f"{total_calories_activity}")
    if int(data['physical_activity']) == 1:
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в соответствии, с выбранным уровнем активности:"
                             f"{total_calories_activity * 1.2}")
    elif int(data['physical_activity']) == 2:
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в соответствии, с выбранным уровнем активности:"
                             f"{total_calories_activity * 1.375}")
    elif int(data['physical_activity']) == 3:
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в соответствии, с выбранным уровнем активности:"
                             f"{total_calories_activity * 1.55}")
    elif int(data['physical_activity']) == 4:
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в соответствии, с выбранным уровнем активности:"
                             f"{total_calories_activity * 1.725}")

    elif int(data['physical_activity']) == 5:
        await message.answer(f"Количество энергии необходимое твоему организму"
                             f" в соответствии, с выбранным уровнем активности:"
                             f"{total_calories_activity * 1.9}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

