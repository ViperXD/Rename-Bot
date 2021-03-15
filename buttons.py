from pyrogram.types import InlineKeyboardButton

class Button(object):
    START_BUTTONS = [[InlineKeyboardButton('⚙ Channel ⚙', url='https://telegram.me/VKPROJECTS'), InlineKeyboardButton('⚙ Group ⚙', url='https://telegram.me/VKP_BOTS'),],
                        [InlineKeyboardButton('⚙Help⚙', callback_data='help')]]

    HELP_BUTTONS = [[InlineKeyboardButton('⚙ Channel ⚙', url='https://telegram.me/VKPROJECTS'), InlineKeyboardButton('⚙ Group ⚙', url='https://telegram.me/VKP_BOTS'),],
                        [InlineKeyboardButton('⚜ Back to Home ⚜', callback_data='home')]]
