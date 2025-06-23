import random
import allvarsandquest
import keyboards
from config import bot, owners, is_user_subscribed, channel
import requests
import telebot
import asyncio
import filework

users_in_test = {}
all_of_users ={}
image_url = ("https://images.steamusercontent.com/ugc/18301734"
             "91796467886/41C5DB2661FCEB9884AC5FE6E1B4CCF25A0CD"
             "A4C/?imw=512&amp;imh=460&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true")

async def start_test(message):
    try:
        if await is_user_subscribed(message.from_user.id, channel):
            random_ticket = random.randint(1, 4)
            for i in range(5):
                all_of_users[message.from_user.id]["contin_for"] = False
                await filework.save_stats(all_of_users)
                answers = "Варианты ответа:\n"

                await bot.send_message(message.from_user.id, f"<b>{allvarsandquest.vars[random_ticket - 1][f'var{random_ticket}'][f'вопрос{i + 1}']['текст']}</b>", parse_mode="HTML")
                await asyncio.sleep(1)
                sent_message = await bot.send_message(message.from_user.id,"<i>Пожалуйста прочитайте вопрос, после этого вам будут даны варианты ответа.</i>", parse_mode= "HTML")
                await asyncio.sleep(5)
                await bot.delete_message(message.from_user.id, sent_message.message_id)
                await asyncio.sleep(1)

                for j in range(len(
                        allvarsandquest.vars[random_ticket - 1][f"var{random_ticket}"][f"вопрос{i + 1}"]["ответы"])):
                    answers += f"{j+1}. {allvarsandquest.vars[random_ticket - 1][f'var{random_ticket}'][f'вопрос{i + 1}']['ответы'][j].capitalize()}.\n"

                await bot.send_message(message.from_user.id, answers, reply_markup= await keyboards.get_ans_keyboard(len(
                    allvarsandquest.vars[random_ticket - 1][f"var{random_ticket}"][f"вопрос{i + 1}"]["ответы"])))

                while(all_of_users[message.from_user.id]["contin_for"] != True):
                    await asyncio.sleep(1)

                if(all_of_users[message.from_user.id]["answer"] in allvarsandquest.vars[random_ticket - 1][f"var{random_ticket}"][f"вопрос{i + 1}"]["правильный_вариант"]):
                    all_of_users[message.from_user.id]["true"] += 1
                    await filework.save_stats(all_of_users)
                    await bot.send_message(message.from_user.id, "✅")
                    await bot.send_message(message.from_user.id, "Верно!")
                else:
                    await bot.send_message(message.from_user.id, "❌")
                    await bot.send_message(message.from_user.id, "Неверно!")
                await asyncio.sleep(4)

            if (all_of_users[message.from_user.id]["true"] < 4):
                await bot.send_message(message.from_user.id, "Извините, ваш результат неудовлетворительный. Пожалуйста, перепройдите тест!")
                all_of_users[message.from_user.id]["true"] = 0
                await bot.send_message(message.from_user.id, "Хотите пройти сейчас тест?", reply_markup=await keyboards.get_choose_keyboard())
                all_of_users[message.from_user.id]["try"] +=1
                await filework.save_stats(all_of_users)

            if(all_of_users[message.from_user.id]["true"] >= 4):
                response = requests.get(image_url, stream=True)
                image_data = response.raw.read()
                await bot.send_photo(message.from_user.id, image_data, caption="Вы прошли тест!")
                all_of_users[message.from_user.id]["try"] += 1
                await filework.save_stats(all_of_users)
                await send_info(all_of_users[message.from_user.id]["true"], all_of_users[message.from_user.id]["try"], all_of_users[message.from_user.id]["user"])
                all_of_users[message.from_user.id]["true"] = 0
                await filework.save_stats(all_of_users)
            users_in_test[message.from_user.id] = False
        else: await bot.send_message(message.from_user.id, f"Подпишись на <a href=\"https://t.me/{channel[1:]}\">канал</a>!",
                            parse_mode="HTML")
    except telebot.apihelper.ApiTelegramException as e:
        print("ошибка")

async def send_info(right_ans,tries, idshka):
    await bot.send_message(owners[0], f"Кто: {idshka}\nРезультат: {right_ans}/5\nПопытка: {tries}")




