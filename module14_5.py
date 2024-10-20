import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import crud_functions

api = "7871699489:AAEN1AKsmNSngiu7XKcwcpPcTvptIkm-9IQ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


crud_functions.initiate_db()
products_list = crud_functions.get_all_products()

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Рассчитать", "Информация", "Купить", "Регистрация"]
keyboard.add(*[types.KeyboardButton(button) for button in buttons])

inline_keyboard = types.InlineKeyboardMarkup()
inline_keyboard.add(types.InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'))
inline_keyboard.add(types.InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'))

inline_buy_keyboard = types.InlineKeyboardMarkup()
products = [f'Product{i}' for i in range(1, 5)]
for product in products:
    inline_buy_keyboard.add(types.InlineKeyboardButton(text=product, callback_data='product_buying'))

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_keyboard)

@dp.message_handler(lambda message: message.text == 'Купить')
async def get_buying_list(message: types.Message):
    response = ""
    for i in range(1, 5):
        response += f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}\n'
        await message.answer_photo(photo=open(f'files/Product{i}.png', 'rb'))

@dp.message_handler(lambda message: message.text == 'Регистрация')
async def sign_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if not username.isalpha():
        await message.answer("Имя пользователя должно содержать только латинские буквы. Попробуйте снова:")
        return

    if crud_functions.is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')

    crud_functions.add_user(username, email, age)

    await message.answer("Регистрация завершена! Добро пожаловать!")
    await state.finish()

if __name__ == '__main__':

   executor.start_polling(dp, skip_updates=True)