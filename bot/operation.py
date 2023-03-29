"""
This is a echo bot.
It echoes any incoming text messages.
"""
import requests as requests
import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5978476855:AAEUfYUTXPDGQsjLzGBmuf21fbz3hgKje7k'
URL = "http://127.0.0.1:8000/change_status/"
URL_SERVER = "https://choko.uz/change_status/"
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

chat_id = '-1001906730536'


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
            await bot.send_message('-1001906730536', "Buyurtma tasdiqlandi!")
        else:
            await bot.send_message('-1001906730536', "Xatolik yuz berdi")

    elif text == 'canceled':
        data = {
            "status": "Canceled",
            "id": id
        }
        response = requests.request("POST", URL_SERVER, data=data)
        if response.status_code == 200:
            await bot.send_message('-1001906730536', "Buyurtma bekor qilindi!")

        else:
            await bot.send_message('-1001906730536', "Xatolik yuz berdi.")

    else:
        await bot.send_message('-1001906730536', "Xatolik yuz berdi!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
