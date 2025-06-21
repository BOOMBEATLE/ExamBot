from telebot import types
import allvarsandquest

async def get_ans_keyboard(count_but):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(f"{i+1}", callback_data=f"{i+1}") for i in range(count_but)]
    keyboard.add(*buttons)
    return keyboard

async def get_choose_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Да", callback_data="yes"),
                 types.InlineKeyboardButton("Нет", callback_data="no"))
    return keyboard

async def get_start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Старт", callback_data="start"))
    return keyboard