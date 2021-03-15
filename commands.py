import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import time
import os
import sqlite3
import asyncio

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from buttons import Button
from script import script

import pyrogram

from pyrogram import Client as FayasNoushad
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from plugins.rename import rename

@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    await bot.send_message(chat_id=update.chat.id, text=script.START_TEXT.format(update.from_user.mention), parse_mode="html", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(Button.START_BUTTONS), reply_to_message_id=update.message_id)


@FayasNoushad.on_message(filters.command(["help"]))
async def help(bot, update):
    await bot.send_message(chat_id=update.chat.id, text=script.HELP_USER, parse_mode="html", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(Button.HELP_BUTTONS), reply_to_message_id=update.message_id)

    
@FayasNoushad.on_message(filters.private & (filters.audio | filters.document | filters.animation | filters.video | filters.voice | filters.video_note))
async def rename_cb(bot, update):
    if Config.UPDATE_CHANNEL:
        try:
          user = await bot.get_chat_member(Config.UPDATE_CHANNEL, update.chat.id)
          if user.status == "kicked":
            await update.reply_text(text=script.BANNED_USER_TEXT)
            return
        except UserNotParticipant:
          await update.reply_text(text=script.FORCE_SUBSCRIBE_TEXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="😎 Join Channel 😎", url=f"https://telegram.me/{Config.UPDATE_CHANNEL}")]]))
          return
        except Exception:
          await update.reply_text(text=script.SOMETHING_WRONG)
          return
    if update.from_user.id not in Config.AUTH_USERS:
        if str(update.from_user.id) in Config.ADL_BOT_RQ:
            current_time = time.time()
            previous_time = Config.ADL_BOT_RQ[str(update.from_user.id)]
            process_max_timeout = round(Config.PROCESS_MAX_TIMEOUT/60)
            present_time = round(Config.PROCESS_MAX_TIMEOUT-(current_time - previous_time))
            Config.ADL_BOT_RQ[str(update.from_user.id)] = time.time()
            if round(current_time - previous_time) < Config.PROCESS_MAX_TIMEOUT:
                await bot.send_message(chat_id=update.chat.id, text=script.FREE_USER_LIMIT_Q_SZE.format(process_max_timeout, present_time), disable_web_page_preview=True, parse_mode="html", reply_to_message_id=update.message_id)
                return
        else:
            Config.ADL_BOT_RQ[str(update.from_user.id)] = time.time()
    file = update.media
    try:
        filename = file.file_name
    except:
        filename = "Not Available"
    
    await bot.send_message(
        chat_id=update.chat.id,
        text="<b>File Name</b> : <code>{}</code> \n\nSelect the desired option below 😇".format(filename),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="📝 RENAME 📝", callback_data="rename")],
                                                [InlineKeyboardButton(text="✖️ CANCEL ✖️", callback_data="cancel")]]),
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

@FayasNoushad.on_message(filters.private & filters.reply & filters.text)
async def cus_name(bot, message):
    if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        asyncio.create_task(rename(bot, message))
    else:
        print('No media present')

async def force_name(bot, message):
    await bot.send_message(
        message.reply_to_message.from_user.id,
        "Enter new name for media with file type\n\nExample :- <code>sample.mkv | media</code>",
        reply_to_message_id=message.reply_to_message.message_id,
        reply_markup=ForceReply(True)
    )
