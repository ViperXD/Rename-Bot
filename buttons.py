from pyrogram.types import InlineKeyboardButton

class Button(object):
    START_BUTTONS = [[InlineKeyboardButton('โ Channel โ', url='https://telegram.me/VKPROJECTS'), InlineKeyboardButton('โ Group โ', url='https://telegram.me/VKP_BOTS'),],
                        [InlineKeyboardButton('๐กHelp', callback_data='help'), InlineKeyboardButton('๐About', callback_data='about')]]

    HELP_BUTTONS = [[InlineKeyboardButton('โ Channel โ', url='https://telegram.me/VKPROJECTS'), InlineKeyboardButton('โ Group โ', url='https://telegram.me/VKP_BOTS'),],
                        [InlineKeyboardButton('๐ Home', callback_data='home')]]
