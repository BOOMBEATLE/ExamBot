from config import bot, is_user_subscribed, channel
import asyncio
import telebot
import tester
import keyboards
import filework

@bot.message_handler(commands=['start'])
async def start(message):
    try:
        await start_process(message.chat.id)
    except telebot.apihelper.ApiTelegramException as e:
        print("ошибка")

async def start_process(chat_id):
    try:
        if chat_id not in tester.all_of_users:
            tester.all_of_users.setdefault(chat_id, {"user": "None", "stat": "None", "answer": 0, "true": 0, "try": 0, "contin_for": False})
            await filework.save_stats(tester.all_of_users)
        if chat_id in tester.users_in_test:
            if  tester.users_in_test[chat_id]:
                await bot.send_message(chat_id, "Вы уже начали тест. Пожалуйста, завершите его перед новым запуском!")
                return

        if await is_user_subscribed(chat_id, channel):
            await bot.send_message(chat_id, "Здравствуйте, вы запустили бота-экзаменатора.\nВведите ваш логин")
            tester.all_of_users[chat_id]["stat"] = "wait_foruser"
            await filework.save_stats(tester.all_of_users)
            await get_user()
        else: await bot.send_message(chat_id, f"Подпишись на <a href=\"https://t.me/{channel[1:]}\">канал</a>!", parse_mode="HTML")
    except telebot.apihelper.ApiTelegramException as e:
        print("ошибка")

@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    try:
        if await is_user_subscribed(call.from_user.id, channel):
            if(call.data == "yes" or call.data == "start"):
                await start_process(call.from_user.id)
            if(call.data == "no"):
                await bot.send_message(call.from_user.id, "Нажмите <Старт>, когда будете готовы пройти тест заново!", reply_markup=await keyboards.get_start_keyboard())
            if(call.data != "start" and call.data != "yes" and call.data != "no"):
                tester.all_of_users[call.from_user.id]["answer"] = int(call.data)
                tester.all_of_users[call.from_user.id]["contin_for"] = True
                await filework.save_stats(tester.all_of_users)
            chat_id = int(call.from_user.id)
            message_id = int(call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
        else:
            await bot.send_message(call.from_user.id, f"Подпишись на <a href=\"https://t.me/{channel[1:]}\">канал</a>!",
                            parse_mode="HTML")
    except telebot.apihelper.ApiTelegramException as e:
        print("ошибка")


async def get_user():
    @bot.message_handler(func=lambda message: tester.all_of_users[message.from_user.id]["stat"] == "wait_foruser")
    async def us_handler(message):
        try:
            if await is_user_subscribed(message.from_user.id, channel):
                tester.all_of_users[message.from_user.id]["user"] = message.text
                tester.all_of_users[message.from_user.id]["stat"] = "None"
                await filework.save_stats(tester.all_of_users)
                await bot.send_message(message.from_user.id, "Отлично, перейдём к тестированию!")
                await asyncio.sleep(3)
                tester.users_in_test[message.from_user.id] = True
                await tester.start_test(message)
            else:
                await bot.send_message(message.from_user.id, f"Подпишись на <a href=\"https://t.me/{channel[1:]}\">канал</a>!",
                                parse_mode="HTML")
        except telebot.apihelper.ApiTelegramException as e:
            print("ошибка")

async def set_commands():
    commands = [telebot.types.BotCommand("start", "Начать прохождение теста")]
    await bot.set_my_commands(commands)

async def main():
    await set_commands()
    tester.all_of_users = await filework.load_stats()
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())