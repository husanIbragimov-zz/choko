from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

token = '6348206840:AAG6TSXl9tNsJVbYlS3O2S2Z-VdRBeT1GFs'
url = 'http://127.0.0.1:8000/'
url_server = 'https://azbo.uz/'
bot = Bot(token=token)

dp = Dispatcher(bot)

chat = '663153232'


async def order_product(data):
    print(data)
    User = data[0]['user']
    order_id = data[0]['order']
    media = []
    categoryMenu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"completed-{order_id}"),
                InlineKeyboardButton(text="❌ Qaytarish", callback_data=f"canceled-{order_id}"),
            ],
        ])

    text = f"<b>Yangi Buyurtma</b> \n" \
           f"Telefon raqam: {User} \n" \

    for i in data:
        text += f"------------------------\n" \
                f"Mahsulot: {i['product']} \n" \
                f"Soni: {i['quantity']} ta\n" \
                f"Muddat: {i['variant']} oyga\n"

        # Replace 'photo_file_id_x' with actual file identifiers or URLs
        media.append(types.InputMediaPhoto(media=url_server + i['photo'][1:]))

    try:
        await bot.send_media_group(chat_id=chat, media=media)
        await bot.send_message(chat_id=chat, text=text, reply_markup=categoryMenu, parse_mode='html')
    except Exception as e:
        print(f"Failed to send message: {e}")

