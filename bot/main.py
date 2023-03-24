from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(token='5978476855:AAEUfYUTXPDGQsjLzGBmuf21fbz3hgKje7k')
url = 'http://127.0.0.1:8000/'
url_server = 'http://choko.uz/'
dp = Dispatcher(bot)

categoryMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data="Complated"),
            InlineKeyboardButton(text="❌ Qaytarish", callback_data="Censel"),
        ],
    ])


async def order_product(data):
    User = data[0]['user']
    # photo1 = url + data[0]['photo']
    media = []

    text = f"<b>Yangi Buyurtma</b> \n" \
           f"Telefon raqam: {User} \n" \

    for i in data:
        text += f"------------------------\n" \
                f"Product: {i['product']} \n" \
                f"Muddat: {i['variant']} oyga\n"
        media.append(types.InputMediaPhoto(
            media=url_server + i['photo']
        ))

    await bot.send_media_group(chat_id='739412274', media=media)
    await bot.send_message(chat_id='739412274', message=text, reply_markup=categoryMenu,
                            parse_mode='html')