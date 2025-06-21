from telebot.async_telebot import AsyncTeleBot
import telebot
import aiohttp
token = '7407893995:AAHIsydMGItTLkQNxjMWVNBw_xwicXzBrpc'
bot = AsyncTeleBot(token)
channel = "@FPandHSE"
owners = [525892421]
database = "databasexam.json"

async def is_user_subscribed(user_id, channel_id):
    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        status = chat_member.status

        if status == "administrator" or status == "creator" or status == "member":
            return True
        else: return False
    except telebot.apihelper.ApiTelegramException as e:
        if e.description == "User not found":
            return False
        else:
            print(f"Ошибка при проверке подписки: {e}")
            return False