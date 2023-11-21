"""
This is a echo bot.
It echoes any incoming text messages.
"""
import requests as requests
import logging
from aiogram.dispatcher.filters.builtin import Command
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6348206840:AAG6TSXl9tNsJVbYlS3O2S2Z-VdRBeT1GFs'
URL_PRODUCT = "http://127.0.0.1:8000/count-products/"
URL_CHANGE_STATUS = "http://127.0.0.1:8000/change_status/"
URL_SERVER = "https://azbo.uz/change_status/"
URL_SERVER_PRODUCT = "https://azbo.uz/count-products/"
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

chat_id = '663153232'


@dp.message_handler(Command('count'))
async def bot_help(message: types.Message):
    response = requests.request("GET", URL_SERVER_PRODUCT)
    if response.status_code == 200:
        await bot.send_message('663153232', f"Mahsulotlar soni: <b>{response.json().get('msg')}</b> ta", parse_mode='html')
    else:
        await bot.send_message('663153232', "Xatolik yuz berdi")


@dp.callback_query_handler()
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    chat_id = query.from_user.id
    text = answer_data.split('-')[0]
    id = answer_data.split('-')[1]
    await query.message.delete()
    if text == 'completed':
        data = {
            "status": "Completed",
            "id": id
        }
        response = requests.request("POST", URL_SERVER, data=data)
        if response.status_code == 200:
            await bot.send_message('663153232', "Buyurtma tasdiqlandi!")
        else:
            await bot.send_message('663153232', "Xatolik yuz berdi")

    elif text == 'canceled':
        data = {
            "status": "Canceled",
            "id": id
        }
        response = requests.request("POST", URL_SERVER, data=data)
        if response.status_code == 200:
            await bot.send_message('663153232', "Buyurtma bekor qilindi!")

        else:
            await bot.send_message('663153232', "Xatolik yuz berdi.")

    else:
        await bot.send_message('663153232', "Xatolik yuz berdi!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
